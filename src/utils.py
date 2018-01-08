# src/utils.py

# import pyside
try:
	from PySide2 import QtCore
	from PySide2 import QtGui
	from PySide2 import QtWidgets
	from PySide2 import QtUiTools
	from PySide2 import __version__ as QtVersion
	# import shiboken2

except ImportError:
	from PySide import QtCore
	from PySide import QtGui
	from PySide import QtUiTools
	from PySide import __version__ as QtVersion
	# import shiboken
  
import os, sys, zipfile

class windows(object):

	def __init__(self):
		pass

	def progressbar(self):
		pass

	def inputDialog(self, parent=None, title ='title', message='message?' ):
		'''  
			input dialog template

			@parent
			@title
			@message

			return : input message, False if cancle
		'''
		# if
		print ("Load : " + str(QtVersion))
		print (str(QtVersion).split('.')[0])

		if int( str(QtVersion).split('.')[0] ) < 2 :

			if parent == None:
				parent = QtGui.QWidget()

			text, ok = QtGui.QInputDialog.getText(parent, title, message)
			if ok:
				pass
			else:
				text = False
				print ('Cancle.')
		else :

			# Check open in maya
			try:
				import maya.cmds as cmds
			except ImportError:
				raise("Outside maya Skip.")
				return

			result = cmds.promptDialog(
				title= title,
				message= message,
				button=['OK', 'Cancel'],
				defaultButton='OK',
				cancelButton='Cancel',
				dismissString='Cancel')

			if result == 'OK':
				text = cmds.promptDialog(query=True, text=True)
			else :
				text = False

		return text

class IO:

	def isListEmpty(mylist):

		if mylist == []:
			return False
		else:
			return True
		# raise("Parameter must be LIST")

class utils(object):

	def __init__(self):
		pass

	def jsonLoader(self):
		pass

	def jsonDumper(self):
		pass

	def unzip(self, zipPath, dest):

		if not os.path.exists(zipPath):
			print ('Zip file not fould.')
			return

		if not os.path.exists(dest):
			print('Destination folder not exists.')
			return

		try:
			zfile = zipfile.ZipFile( zipPath )
			zfile.extractall( dest )
		except Exception as e:
			raise(e)

		return dest

	def captureViewport(self, outputdir, filename, ext = 'jpg' ):
		"""
			 capture viewport 2.0 DX 11 

			 var : @outputdir	: Output directory
				   @filename	: filename and extention
				   @ext 		: default 'jpg'

			 return: path (if success)
					 Flase[bool] (if false)
		"""

		path = outputdir + '/' + filename

		if not os.path.exists( outputdir) :
			print (outputdir + ' : not found.')
			return

		import maya.OpenMaya as openMaya
		import maya.OpenMayaUI as openMayaUI
		view 	= openMayaUI.M3dView.active3dView()
		width 	= view.portWidth()
		height 	= view.portHeight()
		image 	= openMaya.MImage()

		try:
			view.readColorBuffer(image, True)
			image.resize(448,252)
			image.writeToFile(path, ext)

			print ('Capture success : ' + path )
			return path
		except Exception as e:
			print ('cannot capture')

		return False

class redshiftUtils :

	def __init__(self):
		pass

	def redshiftUpdateActiveAovList(self):
		""" Update redshift aov list in render setting window
		"""
		import maya.mel as mel
		
		mel.eval("redshiftUpdateActiveAovList();")


if __name__ == '__main__':
	
	# Test inputDialog
	#
	# app = windows()
	# gui = QtGui.QWidget()
	# app.inputDialog(parent= gui)

	# Test zipfile
	#
	zipfilePath = "D:/WORK/Programming/sal_pipeline/data/shot_template.zip"
	dest = "D:/WORK/Pipeline_projectSetup/production/film/sq20/sh300"

	app = utils()
	result = app.unzip(zipPath=zipfilePath, dest=dest)
	print result