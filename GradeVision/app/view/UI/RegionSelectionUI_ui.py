# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'a:\Main\CODE\GUI\GradeVision-Qt\GradeVision\app\view\UI\RegionSelectionUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(743, 673)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.CardWidget = CardWidget(Form)
        self.CardWidget.setObjectName("CardWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.CardWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.TitleLabel = TitleLabel(self.CardWidget)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout_2.addWidget(self.TitleLabel, 1, 0, 1, 1)
        self.image_label = QtWidgets.QLabel(self.CardWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setText("")
        self.image_label.setObjectName("image_label")
        self.gridLayout_2.addWidget(self.image_label, 3, 0, 1, 1)
        self.CommandBar = CommandBar(self.CardWidget)
        self.CommandBar.setEnabled(True)
        self.CommandBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.CommandBar.setAutoFillBackground(False)
        self.CommandBar.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.World))
        self.CommandBar.setObjectName("CommandBar")
        self.gridLayout_2.addWidget(self.CommandBar, 2, 0, 1, 1, QtCore.Qt.AlignVCenter)
        self.gridLayout.addWidget(self.CardWidget, 0, 0, 1, 1)
        self.CardWidget_2 = CardWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CardWidget_2.sizePolicy().hasHeightForWidth())
        self.CardWidget_2.setSizePolicy(sizePolicy)
        self.CardWidget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.CardWidget_2.setMaximumSize(QtCore.QSize(16777215, 180))
        self.CardWidget_2.setObjectName("CardWidget_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.CardWidget_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.TableWidget = TableWidget(self.CardWidget_2)
        self.TableWidget.setObjectName("TableWidget")
        self.TableWidget.setColumnCount(0)
        self.TableWidget.setRowCount(0)
        self.gridLayout_3.addWidget(self.TableWidget, 1, 0, 1, 1)
        self.BodyLabel = BodyLabel(self.CardWidget_2)
        self.BodyLabel.setObjectName("BodyLabel")
        self.gridLayout_3.addWidget(self.BodyLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.CardWidget_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TitleLabel.setText(_translate("Form", "Select the region of interest(s)"))
        self.BodyLabel.setText(_translate("Form", "Enter the data:"))
from qfluentwidgets import BodyLabel, CardWidget, CommandBar, TableWidget, TitleLabel
