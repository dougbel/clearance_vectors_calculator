# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualize_trained_it.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1288, 830)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.vtk_widget = QVTKRenderWindowInteractor(self.centralwidget)
        self.vtk_widget.setGeometry(QtCore.QRect(390, 100, 871, 681))
        self.vtk_widget.setObjectName("vtk_widget")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(20, 80, 101, 16))
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setObjectName("label_6")
        self.l_trained = QtWidgets.QListWidget(self.centralwidget)
        self.l_trained.setGeometry(QtCore.QRect(20, 100, 351, 201))
        self.l_trained.setAlternatingRowColors(True)
        self.l_trained.setObjectName("l_trained")
        self.btn_view_training = QtWidgets.QPushButton(self.centralwidget)
        self.btn_view_training.setEnabled(False)
        self.btn_view_training.setGeometry(QtCore.QRect(1410, 250, 41, 22))
        self.btn_view_training.setObjectName("btn_view_training")
        self.line_descriptors = QtWidgets.QLineEdit(self.centralwidget)
        self.line_descriptors.setGeometry(QtCore.QRect(220, 40, 601, 23))
        self.line_descriptors.setText("")
        self.line_descriptors.setObjectName("line_descriptors")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(100, 40, 121, 23))
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setObjectName("label_5")
        self.btn_path = QtWidgets.QPushButton(self.centralwidget)
        self.btn_path.setGeometry(QtCore.QRect(820, 40, 101, 23))
        self.btn_path.setObjectName("btn_path")
        self.tree_train = QtWidgets.QTreeView(self.centralwidget)
        self.tree_train.setGeometry(QtCore.QRect(20, 310, 351, 471))
        self.tree_train.setAlternatingRowColors(True)
        self.tree_train.setAutoExpandDelay(-1)
        self.tree_train.setIndentation(10)
        self.tree_train.setItemsExpandable(True)
        self.tree_train.setObjectName("tree_train")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1288, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Vizualizing propagation"))
        self.label_6.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Trained</span></p></body></html>"))
        self.btn_view_training.setText(_translate("MainWindow", "Zoom"))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Descriptors path</span></p></body></html>"))
        self.btn_path.setText(_translate("MainWindow", "Browse"))

from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

