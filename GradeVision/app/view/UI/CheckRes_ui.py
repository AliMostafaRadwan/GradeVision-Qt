# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'a:\Main\CODE\GUI\GradeVision-Qt\GradeVision\app\view\UI\CheckRes.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1168, 805)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.CardWidget = CardWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CardWidget.sizePolicy().hasHeightForWidth())
        self.CardWidget.setSizePolicy(sizePolicy)
        self.CardWidget.setObjectName("CardWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.CardWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.image_label = QtWidgets.QLabel(self.CardWidget)
        self.image_label.setText("")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.gridLayout_3.addWidget(self.image_label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CardWidget, 3, 1, 1, 1)
        self.TitleLabel = TitleLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.SearchLineEdit = SearchLineEdit(Form)
        self.SearchLineEdit.setObjectName("SearchLineEdit")
        self.gridLayout.addWidget(self.SearchLineEdit, 2, 0, 1, 2)
        self.CardWidget_2 = CardWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CardWidget_2.sizePolicy().hasHeightForWidth())
        self.CardWidget_2.setSizePolicy(sizePolicy)
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.CardWidget_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TableWidget = TableWidget(self.CardWidget_2)
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setColumnCount(0)
        self.TableWidget.setRowCount(0)
        self.gridLayout_2.addWidget(self.TableWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CardWidget_2, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TitleLabel.setText(_translate("Form", "Checking Student Results "))
from qmaterialwidgets import CardWidget, SearchLineEdit, TableWidget, TitleLabel
