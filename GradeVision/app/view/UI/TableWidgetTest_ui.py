# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'a:\Main\CODE\GUI\GradeVision-Qt\GradeVision\app\view\UI\TableWidgetTest.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(868, 668)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.CardWidget = CardWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CardWidget.sizePolicy().hasHeightForWidth())
        self.CardWidget.setSizePolicy(sizePolicy)
        self.CardWidget.setMinimumSize(QtCore.QSize(0, 391))
        self.CardWidget.setObjectName("CardWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.CardWidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout.addWidget(self.CardWidget, 0, 0, 1, 1)
        self.CardWidget_2 = CardWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CardWidget_2.sizePolicy().hasHeightForWidth())
        self.CardWidget_2.setSizePolicy(sizePolicy)
        self.CardWidget_2.setMinimumSize(QtCore.QSize(0, 255))
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.CardWidget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addWidget(self.CardWidget_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
from qfluentwidgets import CardWidget
