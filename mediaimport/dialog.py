# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(604, 353)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.mediaDir = QtWidgets.QLineEdit(Form)
        self.mediaDir.setEnabled(False)
        self.mediaDir.setObjectName("mediaDir")
        self.horizontalLayout_2.addWidget(self.mediaDir)
        self.browse = QtWidgets.QPushButton(Form)
        self.browse.setObjectName("browse")
        self.horizontalLayout_2.addWidget(self.browse)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.modelList = QtWidgets.QListWidget(Form)
        self.modelList.setObjectName("modelList")
        self.gridLayout.addWidget(self.modelList, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 3, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 3, 1, 1)
        self.fieldMapGrid = QtWidgets.QGridLayout()
        self.fieldMapGrid.setObjectName("fieldMapGrid")
        self.gridLayout.addLayout(self.fieldMapGrid, 2, 3, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Media Import"))
        self.label_3.setText(_translate("Form", "Media directory: "))
        self.browse.setText(_translate("Form", "Browse"))
        self.label_2.setText(_translate("Form", "Map fields"))
        self.label.setText(_translate("Form", "Select note type"))

