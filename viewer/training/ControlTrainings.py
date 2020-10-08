import glob
import json
import os
import sys

import vtk
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from vedo import Plotter

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

        vp = Plotter(qtWidget=self.ui.vtk_widget, bg="white")
        vp.show([], axes=0)


    def start(self):
        self.MainWindow.show()
        sys.exit(self.app.exec_())


    def click_set_dir(self, line, element):
        file_name = str(QFileDialog.getExistingDirectory(self.MainWindow, "Select " + element + " path"))
        if file_name:
            line.setText(file_name)

    def json_training_files_with_path(self):
        filepath_json_propagation_data = os.path.join(self.path_iter, "propagation_data.json")
        files = glob.glob(os.path.join(self.path_iter, '*.json'))
        filepath_json_train_data = [json_file for json_file in files if json_file != filepath_json_propagation_data][0]
        return filepath_json_train_data, filepath_json_propagation_data

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

            json_training_file, json_propagation_file = self.json_training_files_with_path()

            with open(json_training_file) as f:
                self.train_data = json.load(f)
            train_model.load(self.train_data)

            self.ui.tree_train.header().resizeSection(0, 200)
            self.ui.tree_train.expandAll()

            self.update_vtk_interaction()

    def update_vtk_interaction(self):
        env_file, obj_file, ibs_file = self.__iter_meshes_files()
        vp = Plotter(qtWidget=self.ui.vtk_widget, bg="white", title="el mero mero")
        vp.load(env_file).c((.7, .7, .7)).alpha(.6)
        vp.load(obj_file).c((0, 1, 0)).alpha(.78)
        vp.load(ibs_file).c((0, 0, 1)).alpha(.39)
        vp.show(axes=1)


    def __iter_meshes_files(self):

        env_file = os.path.join(self.path_iter,
                                self.train_data['affordance_name'] + '_' + self.train_data[
                                    'obj_name'] + '_environment.ply')
        obj_file = os.path.join(self.path_iter,
                                self.train_data['affordance_name'] + '_' + self.train_data[
                                    'obj_name'] + '_object.ply')
        ibs_file = os.path.join(self.path_iter,
                                self.train_data['affordance_name'] + '_' + self.train_data[
                                    'obj_name'] + '_ibs_mesh_segmented.ply')

        return env_file, obj_file, ibs_file