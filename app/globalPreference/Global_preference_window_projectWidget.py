# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WORK\Programming\sal_pipeline\ui\Global_preference_window_projectWidget.ui'
#
# Created: Mon Nov 27 01:41:42 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2.QtUiTools import *
	from PySide2 import __version__

except ImportError:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from PySide import __version__


class Ui_Form(QWidget):

	def __init__ (self, parent=None):
		super( Ui_Form, self ).__init__(parent)

		self.setupUi()
		# self.show()
		
	def setupUi(self):
		self.setObjectName("widget")
		self.resize(620, 153)
		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.setObjectName("verticalLayout")
		self.groupBox = QGroupBox(self)
		self.groupBox.setTitle("")
		self.groupBox.setObjectName("groupBox")
		self.formLayout = QFormLayout(self.groupBox)
		self.formLayout.setObjectName("formLayout")
		self.label = QLabel(self.groupBox)
		self.label.setObjectName("label")
		self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)
		self.lineEdit_projectName = QLineEdit(self.groupBox)
		self.lineEdit_projectName.setObjectName("lineEdit_projectName")
		self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_projectName)
		self.label_2 = QLabel(self.groupBox)
		self.label_2.setObjectName("label_2")
		self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
		self.label_3 = QLabel(self.groupBox)
		self.label_3.setObjectName("label_3")
		self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
		self.checkBox_active = QCheckBox(self.groupBox)
		self.checkBox_active.setObjectName("checkBox_active")
		self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.checkBox_active)
		self.lineEdit_projectCode = QLineEdit(self.groupBox)
		self.lineEdit_projectCode.setObjectName("lineEdit_projectCode")
		self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_projectCode)
		self.lineEdit_projectPath = QLineEdit(self.groupBox)
		self.lineEdit_projectPath.setObjectName("lineEdit_projectPath")
		self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_projectPath)
		self.verticalLayout.addWidget(self.groupBox)

		self.retranslateUi()
		self.setTabOrder(self.lineEdit_projectName, self.lineEdit_projectCode)
		self.setTabOrder(self.lineEdit_projectCode, self.lineEdit_projectPath)
		self.setTabOrder(self.lineEdit_projectPath, self.checkBox_active)

	def retranslateUi(self):
		self.label.setText(QApplication.translate("widget", "Project name :"))
		self.label_2.setText(QApplication.translate("widget", "Project code  :"))
		self.label_3.setText(QApplication.translate("widget", "Project path  :"))
		self.checkBox_active.setText(QApplication.translate("widget", "Active"))

		self.lineEdit_projectPath.textChanged.connect(self.slashChanged)

	def slashChanged(self,text):
		self.setProjectPath(text.replace("\\",'/'))

	def setProjectName(self,text):
		self.lineEdit_projectName.setText(text)

	def setProjectCode(self,text):
		self.lineEdit_projectCode.setText(text)

	def setProjectPath(self,text):
		self.lineEdit_projectPath.setText(text)

