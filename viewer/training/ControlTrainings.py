import glob
import json
import os
import sys

import vedo
import vtk
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from vedo import Plotter, load, Text2D, Lines, Spheres, Point, Arrow

from it.testing.deglomerator import Deglomerator
from it_clearance.testing.deglomerator import DeglomeratorClearance
from it_clearance.utils import get_vtk_items_cv_pv
from thirdparty.QJsonModel.qjsonmodel import QJsonModel
from viewer.training.visualize_trained_it import Ui_MainWindow


class CtrlTrainingsVisualizer:

    def __init__(self):

        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.vtk_widget.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        # signals
        self.ui.btn_path.clicked.connect(lambda: self.click_set_dir(self.ui.line_descriptors, "descriptors"))
        self.ui.line_descriptors.textChanged.connect(
            lambda: self.update_list_interactions(self.ui.line_descriptors.text()))
        self.ui.l_trained.itemSelectionChanged.connect(self.update_visualized_interaction)
        self.ui.chk_view_normal_env.stateChanged.connect(self.change_view_normal_env)

        self.idx_iter = None
        self.path_iter = None
        self.base_name = None

        self.vp = Plotter(qtWidget=self.ui.vtk_widget, bg="white")
        self.vp.show([], axes=0)

        self.vedo_normal_env = None

    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def click_set_dir(self, line, element):
        file_name = str(QFileDialog.getExistingDirectory(self.MainWindow, "Select " + element + " path"))
        if file_name:
            line.setText(file_name)

    def change_view_normal_env(self):
        if not self.ui.chk_view_normal_env.isChecked():
            if self.vedo_normal_env is not None:
                self.vp.clear(self.vedo_normal_env)
        else:
            np_normal_env = np.asarray(list(map(float, self.train_data['trainer']["normal_env"].split(","))))
            self.vedo_normal_env = Arrow([0, 0, 0], 2 * np_normal_env, c="darkorange", s=0.001)
            self.vp.add(self.vedo_normal_env)

    def get_basenames(self):
        filepath_json_propagation_data = os.path.join(self.path_iter, "propagation_data.json")
        files = glob.glob(os.path.join(self.path_iter, '*.json'))
        filepath_json_train_data = [json_file for json_file in files if json_file != filepath_json_propagation_data][0]
        return os.path.splitext(filepath_json_train_data)[0]

    def update_list_interactions(self, path_descriptors):
        self.ui.l_trained.clear()
        interactions = os.listdir(path_descriptors)
        interactions.sort()
        for inter in interactions:
            self.ui.l_trained.addItem(inter)

    def update_visualized_interaction(self):
        self.idx_iter = None
        if len(self.ui.l_trained.selectedIndexes()) > 0:
            self.idx_iter = self.ui.l_trained.selectedIndexes()[0].row()
            self.path_iter = os.path.join(self.ui.line_descriptors.text(), self.ui.l_trained.currentItem().text())

            train_model = QJsonModel()
            self.ui.tree_train.setModel(train_model)

            base_name = self.get_basenames()

            json_training_file = base_name + '.json'
            with open(json_training_file) as f:
                self.train_data = json.load(f)
            train_model.load(self.train_data)

            self.ui.tree_train.header().resizeSection(0, 200)
            self.ui.tree_train.expandAll()

            self.update_vtk_interaction(base_name)
            self.change_view_normal_env()

    def update_vtk_interaction(self, base_name):
        old_camera = self.vp.camera

        # meshes
        env_file = base_name + '_environment.ply'
        obj_file = base_name + '_object.ply'
        ibs_file = base_name + '_ibs_mesh_segmented.ply'
        self.vp = Plotter(qtWidget=self.ui.vtk_widget, bg="white")
        self.vp.camera = old_camera
        l_to_plot = []

        txt = Text2D(self.ui.l_trained.currentItem().text(), pos="top-left",
                     bg='darkblue', c="lightgray", font='Arial', s=0.8, alpha=0.9)
        l_to_plot.append(txt)
        vedo_env = load(env_file).c((.7, .7, .7)).alpha(.6)
        vedo_obj = load(obj_file).c((0, 1, 0)).alpha(1)
        vedo_ibs = load(ibs_file).c((0, 0, 1)).alpha(.39)
        l_to_plot.append(vedo_env)
        l_to_plot.append(vedo_obj)
        l_to_plot.append(vedo_ibs)

        # vectors
        num_pv = self.train_data['trainer']['sampler']['sample_size']

        if 'cv_sampler' in self.train_data['trainer']:
            it_descriptor = DeglomeratorClearance(self.path_iter, self.train_data['affordance_name'],
                                                  self.train_data['obj_name'])
            num_cv = self.train_data['trainer']['cv_sampler']['sample_clearance_size']

            cv_points = it_descriptor.cv_points[0:num_cv]
            cv_vectors = it_descriptor.cv_vectors[0:num_cv]

            clearance_vectors = Lines(cv_points, cv_points + cv_vectors, c='yellow', alpha=1).lighting("plastic")
            cv_from = Spheres(cv_points, r=.004, c="yellow", alpha=1).lighting("plastic")
            l_to_plot.append(clearance_vectors)
            l_to_plot.append(cv_from)
            txt = Text2D("Provenance and Clearance vectors provided", pos="top-right", bg='darkgreen', c="lightgray",
                         font='Arial', justify='right', alpha=0.9)
            l_to_plot.append(txt)
        else:
            it_descriptor = Deglomerator(self.path_iter, self.train_data['affordance_name'],
                                         self.train_data['obj_name'])
            txt = Text2D("Only Provenance vectors provided", pos="top-right", bg='orangered', c="lightgray",
                         font='Arial', justify='right', alpha=0.9)

        l_to_plot.append(txt)
        pv_points = it_descriptor.pv_points[0:num_pv]
        pv_vectors = it_descriptor.pv_vectors[0:num_pv]
        provenance_vectors = Lines(pv_points, pv_points + pv_vectors, c='red', alpha=1).lighting("plastic")
        l_to_plot.append(provenance_vectors)

        l_to_plot.append(Point((0,0,0), c='darkorange'))

        self.vp.show(l_to_plot, axes=1)
