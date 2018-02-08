#
# ===== Maya Application template =====
# 

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as apiUI
#import shiboken

from functools import partial
import os, sys, subprocess, time, datetime, shutil

# ============ Will change to qt.py ============
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

# project libs import
from sal_pipeline.src import env
from sal_pipeline.src import utils
from sal_pipeline.src import log
reload(utils)
reload(env)
reload(log)

# tool libs import
import mayaGlobalPublisher_core 
reload(mayaGlobalPublisher_core)

core = mayaGlobalPublisher_core.mayaGlobalPublisher_core()
getEnv 	= env.getEnv()
modulepath = getEnv.modulePath()

logger = log.logger("globalPublisher")
logger = logger.getLogger()

__app_version__ = '1.1'
# V0.1
# V0.2.0 : support Export GPU, Bounding box, Scene assembly
# V0.3.0 : Add texture step
# V1.0.0 : Add logger
# V1.1.0 : Add config file, Fix hero file create.
# V1.2.0 : Add save increment Optionbox, Add RS proxy optionbox

try:
	myInfo = env.getInfo()
	myInfo.get_task()
except IndexError :
	e_msg = "## This file is not in pipeline. please check your file. ##\n"
	print('_'*64)
	logger.error(e_msg)

	raise IOError(e_msg)

# Read from config file : config/renderSetting.json
config = getEnv.get_appConfig("globalPublish")

class mayaGlobalPublisher( QMainWindow ):

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		_uiFilename_ = 'Maya_GlobalPublish.ui'
		_uiFilePath_ = modulepath + '/ui/' + _uiFilename_		

		# Check is ui file exists?
		if not os.path.isfile( _uiFilePath_ ):
			cmds.error( 'File ui not found.' )

		# ---- LoadUI -----
		loader = QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QFile( _uiFilePath_ )
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		self.all_Geo_Option = config['geo_group']

		self.ui.setWindowTitle('Maya global publisher v.' + str(__app_version__))

		self._initUI()
		self._initConnect()
		self._setupOption_byTask()

		self.ui.show()

	def _initUI(self):
		self.ui.progressBar.hide()

		self.ui.lineEdit_publisher.setText( myInfo.getUsername() )
		self.ui.label_pubFileName.setText(  myInfo.get_pubName() )
		self.ui.label_filePath.setText( cmds.file(q=True, sn=True) )
		self.ui.label_dateTime.setText( str(time.strftime("%d/%m/%Y %H:%M %p",time.localtime())))

		# FUTURE : Query configyration from config file.
		self.ui.comboBox_pipelineStep.addItem("model")
		self.ui.comboBox_pipelineStep.addItem("rig")
		self.ui.comboBox_pipelineStep.addItem("texture")
		self.ui.comboBox_pipelineStep.addItem("set")

		# Get current task
		self._setCurrentTask()

		# capture viewport
		self.setThumbnail( core.captureViewport() )

	def _initConnect(self):
		self.ui.pushButton_cancel.clicked.connect(self.closeWindow)
		self.ui.pushButton_publish.clicked.connect(self._doPublish)

		self.ui.comboBox_pipelineStep.activated.connect(self._setupOption_byTask)
		# QObject.connect(self.ui.comboBox_pipelineStep, SIGNAL("currentIndexChanged(arg__1)"), self._setupOption_byTask)

	def setThumbnail(self, imagePath):

		if not os.path.exists(imagePath):
			imagePath = ''
			self.pixmap_Placeholder.setText(imagePath)
			return

		pixmap = QPixmap( imagePath )
		pixmap = pixmap.scaledToWidth(240)
		self.ui.label_imagePlaceHolder.setPixmap(pixmap)

	def _setCurrentTask(self):
		''' set current task to optionbox when app start up '''
		current_task = myInfo.get_task()

		try:
			currentIndx = self.ui.comboBox_pipelineStep.findText(current_task)
		except :
			print ( "Cannot set up current step : " +  current_task )
			return False

		self.ui.comboBox_pipelineStep.setCurrentIndex(currentIndx)

	def _setupOption_byTask(self):
		'''
		change TaskOption by task change
		'''
		step = self.ui.comboBox_pipelineStep.currentText()

		_model_option 	= config['option']['model']
		_texture_option	= config["option"]['texture']
		_rig_option		= config["option"]['rig']
		_set_option		= config["option"]['set']

		if not step :
			# get current step
			step = myInfo.get_task()

		logger.info( "current step : %s"%(step))

		# setup option

		if step == 'model':
			self._hideAllOption()
			# show option for model
			self._showOption(_model_option)

		elif step == 'rig' :
			self._hideAllOption()

		elif step == 'texture':
			self._hideAllOption()
			# show option for texture
			self._showOption(_texture_option)
		elif step == 'set':
			self._hideAllOption()
			# show option for texture
			self._showOption(_set_option)			

		else :
			self._hideAllOption()
			return False

	def _showOption(self, option_list):
		''' show option from given list '''
		for option_ui in option_list :
		 	eval( "self.ui.{option_ui}.show()".format( option_ui = option_ui ) )
		 	eval( "self.ui.{option_ui}.setCheckState(Qt.Checked)".format( option_ui = option_ui ) )

	def _hideAllOption(self):
		'''hide all option'''

		for option_ui in self.all_Geo_Option :
			eval( "self.ui.{option_ui}.hide()".format(option_ui = option_ui ) )
			eval( "self.ui.{option_ui}.setCheckState(Qt.Unchecked)".format( option_ui = option_ui ) )

	def _getCheckedOption(self):

		cache_option = []
		for step in config['geo_group'] :
			if self.isOptionCheck( step ):
				cache_option.append(step)

		return cache_option

	def _doPublish(self):
		''' publish file '''

		logger.info ("===== Publish Start =====")

		if not cmds.objExists("Geo_grp"):
			cmds.confirmDialog("Not have \"Geo_grp\"")
			return False

		# Setup progressbar============================
		_count_step = len(self._getCheckedOption())
		self.ui.progressBar.show()
		self.ui.progressBar.setRange( 0, 0)

		# START PUBLISH ================================
		self.ui.listWidget_allStatus.clear()

		# Check save state::
		is_modifiedFile = cmds.file(q=True, modified=True)

		# // When file have some change, Save in new version.
		if is_modifiedFile :

			#  save Increment
			if self.isOptionCheck("checkBox_incrementSave"):
				core.saveIncrement()
				self.update_Status("save increment.")

		# save to Hero file
		core.creat_HeroFile()
		self.update_Status("Create hero file.")
		self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

		# export Publish data via JSON
		core.export_pubData(task 	= myInfo.get_task(), 
							filename= myInfo.get_fileName(), 
							user 	= myInfo.getUsername(), 
							date 	= self.ui.label_dateTime.text(), 
							comment = self.ui.lineEdit_comment.text(),
							cache 	= self._getCheckedOption())
		self.update_Status("Create publish metadata.")

		# **** EXPORT PIPELINE CACHE ***
		self.ui.progressBar.setRange( 0, _count_step )

		# Export GPU
		if self.isOptionCheck("GPU_checkBox"):
			core.export_GPUCache()
			self.update_Status("Export GPU complete.")
			self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

		# Export BBox
		if self.isOptionCheck("boundingBox_checkBox"):
			core.export_objBBox()
			self.update_Status("Export Bounding box complete.")
			self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

		# Export Redshift proxy
		if self.isOptionCheck("RSProxy_checkBox"):
			core.export_RSProxy()
			self.update_Status("Create Redshift proxy complete.")
			self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)			

		# Export Scene Assembly
		if self.isOptionCheck("sceneAssembly_checkBox"):
			core.export_sceneAssembly()
			self.update_Status("Create Scene assembly complete.")
			self.ui.progressBar.setValue(self.ui.progressBar.value() + 1)

		self.update_Status("===== Publish complete =====")
		self.ui.progressBar.hide()

	def isOptionCheck(self, QcheckBox_uiName):
		'''return check stage'''

		try :
			is_checked = eval("self.ui.{option_ui}.checkState()".format(option_ui = QcheckBox_uiName))

		except AttributeError as e :
			# raise(e)
			logger.error (e)
			return False

		return is_checked

	def update_Status(self, message):
		item = QListWidgetItem(message)
		self.ui.listWidget_allStatus.addItem(item)
		QCoreApplication.processEvents()

		logger.info (message)

	def closeWindow(self):
		clearUI()

#####################################################################

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def getMayaWindow():
	"""
	Get the main Maya window as a QMainWindow instance
	@return: QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QWidget)

def clearUI():
	if cmds.window('sal_globalPublisher',exists=True):
		cmds.deleteUI('sal_globalPublisher')
		clearUI()

def run():
	clearUI()
	app = mayaGlobalPublisher( getMayaWindow() )
	# pass

if __name__ == '__main__':
	run()