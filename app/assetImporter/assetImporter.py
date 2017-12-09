#
# ===== Maya Application template =====
# 

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as apiUI
import shiboken

from functools import partial
import os, sys, subprocess, time

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

from sal_pipeline.src import env
from sal_pipeline.src import utils
reload(utils)
reload(env)

getEnv 	= env.getEnv()
getInfo = env.getInfo()
modulepath = getEnv.modulePath()

__app_version__ = "0.1"
# V0.1

class mayaAssetImpoter( QMainWindow ):

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		_uiFilename_ = 'assetImporter.ui'
		_uiFilePath_ = modulepath + '/ui/' + _uiFilename_		

		self.currentProject = ""
		self.currentType	= ""

		self.import_asSAM  = "Scene assembly"
		self.import_asREF  = "Reference"
		self.import_method = [ self.import_asSAM, self.import_asREF ]

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

		self.ui.setWindowTitle('Maya asset importer v.' + str(__app_version__))

		self._initUI()
		self._initConnect()

		self.ui.show()

	def _initUI(self):
		self._loadProject()
		self._loadAssetType()
		self.loadAssetList()

		self.ui.importAs_comboBox.addItems(self.import_method)

	def _initConnect(self):
		self.ui.close_pushButton.clicked.connect(self.closeWindow)
		self.ui.project_comboBox.activated.connect(self.project_comboBox_onActivated)
		self.ui.assetType_comboBox.activated.connect(self.loadAssetList)

		self.ui.import_pushButton.clicked.connect(self.importAsset)

	def _loadProject (self):
		'''Load project list from DB'''
		projectList = listAllProject()

		self.ui.project_comboBox.addItems( projectList )

		# get active project
		for project in getEnv.globalConfig_data['setting']['projects'].keys():
			if getEnv.globalConfig_data['setting']['projects'][project]['active'] == True:
				break

		# set current actived project
		self.currentProject = self.ui.project_comboBox.findText( project )
		self.ui.project_comboBox.setCurrentIndex( self.currentProject )

		# Setup Environment
		getInfo = env.getInfo(projectName = self.currentProject )

		return projectList

	def _loadAssetType(self):
		'''Load asset type in project from DB'''
		assetType = []

		self.ui.assetType_comboBox.clear()

		for mytype in os.listdir( getInfo.assetPath ):
			if os.path.isdir(getInfo.assetPath + '/' + mytype):
				self.ui.assetType_comboBox.addItem( mytype )

		self.currentType = self.ui.assetType_comboBox.currentText()
		return assetType 

	def project_comboBox_onActivated(self):
		'''project_comboBox'''
		self.currentProject = self.ui.project_comboBox.findText( project )
		getInfo = env.getInfo(projectName = self.currentProject )

		# Load asset type in project from DB
		self._loadAssetType()

		# Clear main list
		self.ui.main_listWidget.clear()

	def loadAssetList(self):
		'''Load Asset list from current project and asset type'''
		currentProject	= self.ui.project_comboBox.currentText()
		currentType		= self.ui.assetType_comboBox.currentText()

		self.ui.main_listWidget.clear()

		path =  getInfo.assetPath + '/' + currentType
		for myAsst in os.listdir( path ):

			workspace = path + '/' + myAsst
			thumbnail_path = getInfo.getThumbnail(workspace = workspace, filename = None)

			item = QListWidgetItem(self.ui.main_listWidget)
			item.setText(myAsst)
			icon = QIcon(thumbnail_path)
			icon.pixmap (20,20)
			item.setIcon(icon)
			self.ui.main_listWidget.addItem(item)

			QApplication.processEvents()

	def importAsset(self):
		'''Asset import to scene as Scene Assembly Reference'''
		currentType		= self.ui.assetType_comboBox.currentText()
		currentAsset 	= self.ui.main_listWidget.currentItem().text()
		import_method	= self.ui.importAs_comboBox.currentText()

		asset_pubDir  = getInfo.assetPath + '/' + currentType + '/' + currentAsset + '/scenes/pub'

		# import as Assembly
		if import_method == self.import_asSAM :
			referenceNode_name = currentAsset + "_AD"
			definition_name	= currentAsset + "_AD.ma"
			definition_Path = asset_pubDir + '/' + definition_name

			if not os.path.exists(definition_Path) :
				print ("Path not exist : " + definition_Path)
				return

			result = cmds.assembly(name = referenceNode_name + "_AR", type='assemblyReference')
			cmds.setAttr(result+".definition", definition_Path, type="string")

		# import as Reference
		elif import_method == self.import_asREF :
			
			# Find
			pub_fileName = [file for file in os.listdir(asset_pubDir) if file.endswith("_pub.ma")]
			
			# Reference file
			if len(pub_fileName) == 1 :
				cmds.file( asset_pubDir + '/' + pub_fileName[0], r=True )

			elif len(pub_fileName) > 1 :
				ui_choosePubFile(pub_fileName, pub_fileName)

			else : 
				print "Not have any publish file."
				

	def closeWindow(self):
		print ("close window")
		clearUI()
#####################################################################

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def listAllProject():
	data = getEnv.globalConfig_data
	return data['setting']['projects'].keys()
	# getInfo = env.getInfo(projectName = "Vision")

def ui_choosePubFile(files, scenePath):

	def clearUI_ChoosePubFile():
		if cmds.window('sal_assetImporter_ChoosePubFile',exists=True):
			cmds.deleteUI('sal_assetImporter_ChoosePubFile')
			clearUI_ChoosePubFile()

	def import_File(*args):
		fileName = cmds.optionMenu( "pubFile_optionMenu", q=True,  v=True )
		print os.path.join(scenePath,fileName)
		cmds.file( os.path.join(scenePath,fileName), r=True )

	#-------------------
	clearUI_ChoosePubFile()

	cmds.window("sal_assetImporter_ChoosePubFile")
	cmds.columnLayout(adj=True)
	cmds.text(l="")
	cmds.optionMenu( "pubFile_optionMenu", l="Publish from :" )

	for task in files :
		cmds.menuItem( label = task )
	
	cmds.separator(h=10)
	cmds.setParent("..")
	
	cmds.rowLayout(nc = 2, adj=True)
	cmds.button(l="Import", c= import_File)
	cmds.button(l="close")
	cmds.setParent("..")

	cmds.showWindow("sal_assetImporter_ChoosePubFile")
	cmds.window("sal_assetImporter_ChoosePubFile",e=True, w= 300, h= 100)


def getMayaWindow():
	"""
	Get the main Maya window as a QMainWindow instance
	@return: QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QWidget)

def clearUI():
	if cmds.window('sal_assetImporter',exists=True):
		cmds.deleteUI('sal_assetImporter')
		clearUI()

def run():
	clearUI()
	app = mayaAssetImpoter( getMayaWindow() )
	# pass

if __name__ == '__main__':
	run()