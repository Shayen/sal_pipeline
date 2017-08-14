# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/WORK/Programming/sal_pipeline/ui/projectExplorer_FileWidget.ui'
#
# Created: Sun Aug 13 11:32:03 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

import os, sys
from PySide import QtCore, QtGui

class customWidgetFileExplorer( QtGui.QWidget ):

	def __init__ (self, parent=None):
		super( customWidgetFileExplorer, self ).__init__(parent)

		self.setupUi()
		# self.show()

	def setupUi(self):
		self.setObjectName("widget")
		self.resize(400, 73)
		self.horizontalLayout = QtGui.QHBoxLayout( self )
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pixmap_Placeholder = QtGui.QLabel( self )
		self.pixmap_Placeholder.setObjectName("pixmap_Placeholder")
		self.horizontalLayout.addWidget(self.pixmap_Placeholder)
		self.detail_formLayout = QtGui.QFormLayout()
		self.detail_formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
		self.detail_formLayout.setObjectName("detail_formLayout")
		self.label_Filename = QtGui.QLabel( self )
		self.label_Filename.setObjectName("label_Filename")
		self.detail_formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_Filename)
		self.fileName = QtGui.QLabel( self )
		self.fileName.setObjectName("fileName")
		self.detail_formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.fileName)
		self.label_datemod = QtGui.QLabel( self )
		self.label_datemod.setObjectName("label_datemod")
		self.detail_formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_datemod)
		self.DateMod = QtGui.QLabel( self )
		self.DateMod.setObjectName("DateMod")
		self.detail_formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.DateMod)
		self.label_comment = QtGui.QLabel( self )
		self.label_comment.setObjectName("label_comment")
		self.detail_formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_comment)
		self.comment = QtGui.QLabel( self )
		self.comment.setWordWrap(True)
		self.comment.setObjectName("comment")
		self.detail_formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comment)
		self.horizontalLayout.addLayout(self.detail_formLayout)
		self.action_comboBox = QtGui.QComboBox( self )
		self.action_comboBox.setEnabled(True)
		self.action_comboBox.setObjectName("action_comboBox")
		self.action_comboBox.addItem("")
		self.action_comboBox.addItem("")
		self.action_comboBox.addItem("")
		self.horizontalLayout.addWidget(self.action_comboBox)
		self.horizontalLayout.setStretch(1, 2)

		self.action_comboBox.setItemText(0, QtGui.QApplication.translate("widget", "Action", None, QtGui.QApplication.UnicodeUTF8))
		self.action_comboBox.setItemText(1, QtGui.QApplication.translate("widget", "Open folder", None, QtGui.QApplication.UnicodeUTF8))
		self.action_comboBox.setItemText(2, QtGui.QApplication.translate("widget", "Copy path", None, QtGui.QApplication.UnicodeUTF8))

		# self.setStyleSheet("background-color:red;")
		self.retranslateUi( )
		# QtCore.QMetaObject.connectSlotsByName( self )

	def retranslateUi(self):
		# form.setWindowTitle(QtGui.QApplication.translate("widget", "widget", None, QtGui.QApplication.UnicodeUTF8))
		# self.pixmap_Placeholder.setText(QtGui.QApplication.translate("widget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
		self.label_Filename.setText(QtGui.QApplication.translate("widget", "File name :", None, QtGui.QApplication.UnicodeUTF8))
		self.fileName.setText(QtGui.QApplication.translate("widget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
		self.label_datemod.setText(QtGui.QApplication.translate("widget", "Date modified :", None, QtGui.QApplication.UnicodeUTF8))
		self.DateMod.setText(QtGui.QApplication.translate("widget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
		self.label_comment.setText(QtGui.QApplication.translate("widget", "Comment :", None, QtGui.QApplication.UnicodeUTF8))
		self.comment.setText(QtGui.QApplication.translate("widget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
		# self.action_comboBox.setItemText(0, QtGui.QApplication.translate("widget", "Action", None, QtGui.QApplication.UnicodeUTF8))
		# self.action_comboBox.setItemText(1, QtGui.QApplication.translate("widget", "Open folder", None, QtGui.QApplication.UnicodeUTF8))
		# self.action_comboBox.setItemText(2, QtGui.QApplication.translate("widget", "Copy path", None, QtGui.QApplication.UnicodeUTF8))

	def setThumbnail(self, imagePath):

		if not os.path.exists(imagePath):
			imagePath = ''
			self.pixmap_Placeholder.setText(imagePath)
			return

		pixmap = QtGui.QPixmap( imagePath )
		pixmap = pixmap.scaledToWidth(84)
		self.pixmap_Placeholder.setPixmap(pixmap)

	def setFilename(self, filename):
		self.fileName.setText( filename )

	def setDateModified(self, datemod):
		self.DateMod.setText( datemod )

	def setComment(self, comment):
		self.comment.setText( comment )

	def setAction(self):
		pass

	# Return value 

	def filename(self, filename):
		return self.fileName.text( )

	def dateModified(self, datemod):
		return self.DateMod.text( )

	def comment(self, comment):
		return self.comment.text( )
		
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	# Form = QtGui.QWidget()
	ui = customWidgetFileExplorer()
	# ui.setupUi()
	# Form.show()
	sys.exit(app.exec_())

