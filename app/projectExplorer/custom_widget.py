# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:/WORK/Programming/sal_pipeline/ui/projectExplorer_FileWidget.ui'
#
# Created: Sun Aug 13 11:32:03 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

import os, sys

try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2.QtUiTools import *
	from PySide2 import __version__
	import shiboken2 as shiboken

except ImportError:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from PySide import __version__
	import shiboken

class customWidgetFileExplorer( QWidget ):

	def __init__ (self, parent=None):
		super( customWidgetFileExplorer, self ).__init__(parent)

		self.setupUi()
		# self.show()

	def setupUi(self):
		self.setObjectName("widget")
		self.resize(400, 73)
		self.horizontalLayout = QHBoxLayout( self )
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.pixmap_Placeholder = QLabel( self )
		self.pixmap_Placeholder.setObjectName("pixmap_Placeholder")
		self.horizontalLayout.addWidget(self.pixmap_Placeholder)
		self.detail_formLayout = QFormLayout()
		self.detail_formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
		self.detail_formLayout.setObjectName("detail_formLayout")
		self.label_Filename = QLabel( self )
		self.label_Filename.setObjectName("label_Filename")
		self.detail_formLayout.setWidget(0, QFormLayout.LabelRole, self.label_Filename)
		self.fileName = QLabel( self )
		self.fileName.setObjectName("fileName")
		self.detail_formLayout.setWidget(0, QFormLayout.FieldRole, self.fileName)
		self.label_datemod = QLabel( self )
		self.label_datemod.setObjectName("label_datemod")
		self.detail_formLayout.setWidget(1, QFormLayout.LabelRole, self.label_datemod)
		self.DateMod = QLabel( self )
		self.DateMod.setObjectName("DateMod")
		self.detail_formLayout.setWidget(1, QFormLayout.FieldRole, self.DateMod)
		self.label_comment = QLabel( self )
		self.label_comment.setObjectName("label_comment")
		self.detail_formLayout.setWidget(2, QFormLayout.LabelRole, self.label_comment)
		self.comment = QLabel( self )
		self.comment.setWordWrap(True)
		self.comment.setObjectName("comment")
		self.detail_formLayout.setWidget(2, QFormLayout.FieldRole, self.comment)
		self.horizontalLayout.addLayout(self.detail_formLayout)
		self.action_comboBox = QComboBox( self )
		self.action_comboBox.setEnabled(True)
		self.action_comboBox.setObjectName("action_comboBox")
		self.action_comboBox.addItem("")
		self.action_comboBox.addItem("")
		self.action_comboBox.addItem("")
		self.horizontalLayout.addWidget(self.action_comboBox)
		self.horizontalLayout.setStretch(1, 2)

		self.action_comboBox.setItemText(0, QApplication.translate("widget", "Action", None, QApplication.UnicodeUTF8))
		self.action_comboBox.setItemText(1, QApplication.translate("widget", "Open folder", None, QApplication.UnicodeUTF8))
		self.action_comboBox.setItemText(2, QApplication.translate("widget", "Copy path", None, QApplication.UnicodeUTF8))

		# self.setStyleSheet("background-color:red;")
		self.retranslateUi( )
		# QMetaObject.connectSlotsByName( self )

	def retranslateUi(self):
		# form.setWindowTitle(QApplication.translate("widget", "widget", None, QApplication.UnicodeUTF8))
		# self.pixmap_Placeholder.setText(QApplication.translate("widget", "TextLabel", None, QApplication.UnicodeUTF8))
		self.label_Filename.setText(QApplication.translate("widget", "File name :", None, QApplication.UnicodeUTF8))
		self.label_Filename.setStyleSheet("""font-weight: bold;""")

		self.fileName.setText(QApplication.translate("widget", "TextLabel", None, QApplication.UnicodeUTF8))
		self.fileName.setStyleSheet("""font-weight: bold;""")

		self.label_datemod.setText(QApplication.translate("widget", "Last Update :", None, QApplication.UnicodeUTF8))
		self.label_datemod.setStyleSheet("""font-weight: bold;""")
		
		self.DateMod.setText(QApplication.translate("widget", "TextLabel", None, QApplication.UnicodeUTF8))
		
		self.label_comment.setText(QApplication.translate("widget", "Comment :", None, QApplication.UnicodeUTF8))
		# self.label_comment.setStyleSheet("""font-weight: bold;""")
		self.comment.setText(QApplication.translate("widget", "TextLabel", None, QApplication.UnicodeUTF8))
		# self.action_comboBox.setItemText(0, QApplication.translate("widget", "Action", None, QApplication.UnicodeUTF8))
		# self.action_comboBox.setItemText(1, QApplication.translate("widget", "Open folder", None, QApplication.UnicodeUTF8))
		# self.action_comboBox.setItemText(2, QApplication.translate("widget", "Copy path", None, QApplication.UnicodeUTF8))

	def setThumbnail(self, imagePath):

		if not os.path.exists(imagePath):
			imagePath = ''
			self.pixmap_Placeholder.setText(imagePath)
			return

		pixmap = QPixmap( imagePath )
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
	app = QApplication(sys.argv)
	# Form = QWidget()
	ui = customWidgetFileExplorer()
	# ui.setupUi()
	# Form.show()
	sys.exit(app.exec_())

