import glob
import json
import os
import sys

import vtk
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from vedo import Plotter, load, Text2D

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
        self.ui.line_descriptors.textChanged.connect(lambda: self.update_list_interactions(self.ui.line_descriptors.text()))
        self.ui.l_trained.itemSelectionChanged.connect(self.update_visualized_interaction)

        self.idx_iter = None
        self.path_iter = None
        self.base_name = None

        self.vp = Plotter(qtWidget=self.ui.vtk_widget, bg="white")
        self.vp.show([], axes=0)


    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


    def click_set_dir(self, line, element):
        file_name = str(QFileDialog.getExistingDirectory(self.MainWindow, "Select " + element + " path"))
        if file_name:
            line.setText(file_name)

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

    def update_vtk_interaction(self, base_name):
        old_camera = self.vp.camera
        env_file = base_name + '_environment.ply'
        obj_file = base_name + '_object.ply'
        ibs_file = base_name + '_ibs_mesh_segmented.ply'
        self.vp = Plotter(qtWidget=self.ui.vtk_widget, bg="white")
        self.vp.camera = old_camera
        vedo_env = load(env_file).c((.7, .7, .7)).alpha(.6)
        vedo_obj = load(obj_file).c((0, 1, 0)).alpha(.78)
        vedo_ibs = load(ibs_file).c((0, 0, 1)).alpha(.39)
        txt = Text2D(self.ui.l_trained.currentItem().text(), pos="top-left", s=1, c='darkblue',
                     bg="white", font='ImpactLabel', justify='center')

        self.vp.show([vedo_env,vedo_obj, vedo_ibs, txt], axes=1)

