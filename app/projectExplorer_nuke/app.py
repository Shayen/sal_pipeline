import sys, os, subprocess
import nuke

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

from sal_pipeline.src import env
from sal_pipeline.src import utils
import core
reload(core)
reload(env)
# info = env.nuke_info()

__app_version__ = "1.1"
# v0.1
# v1.0 : add variable to remember last time working sequence
# v1.1 : Show thumbnail

getEnv 	= env.getEnv()
modulepath = getEnv.modulePath()

class nuke_projectExplorer( QMainWindow ):

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		_uiFilename_ = 'projectExplorer_nuke.ui'
		_uiFilePath_ = modulepath + '/ui/' + _uiFilename_		

		# Check is ui file exists?
		if not os.path.isfile( _uiFilePath_ ):
			nuke.tprint( 'File ui not found.' )

		# ---- LoadUI -----
		loader = QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QFile( _uiFilePath_ )
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		self.ui.setWindowTitle('Project Explorer v.' + str(__app_version__))

		nuke.tprint("\n====== Project Explorer Start ======")

		self._initConnect()
		self._initUI()

		# self.ui.show()

	def _initUI(self):
		self._setProjectComboBox()
		self._setSequenceComboBox()

		self._setScriptShotList()
		# self._setScriptVersionList()	

		self.ui.label_username.setText(getInfo.get_user())

	def _initConnect(self):
		self.ui.pushButton_open.clicked.connect(self._openScript)
		self.ui.pushButton_save.clicked.connect(self._saveScript)
		self.ui.pushButton_openExplorer.clicked.connect(self._openExplorer)
		self.ui.pushButton_addShot.clicked.connect(self._addShot)

		self.ui.listWidget_scriptShot.itemSelectionChanged.connect(self._setScriptVersionList)
		self.ui.listWidget_scriptVersion.itemClicked.connect(self._versionOnclicked)
		self.ui.comboBox_sequence.activated.connect(self._setScriptShotList)

	def _setProjectComboBox(self):
		''' Setup projectComboBox '''

		# Load all project name
		global getInfo

		self.ui.comboBox_project.clear()
		projectList = core.listAllProject()
		self.ui.comboBox_project.addItems( projectList )

		# get active project
		for project in getEnv.globalConfig_data['setting']['projects'].keys():
			if getEnv.globalConfig_data['setting']['projects'][project]['active'] == True:
				break

		getInfo = env.nuke_info(projectName = project)

		# Check project is ready to use
		activePrj = self.ui.comboBox_project.findText( project )
		self.ui.comboBox_project.setCurrentIndex(activePrj)

		# Setup last time used project
		recentPrj = core.get_recentWorkingProject()
		if recentPrj :
			index = self.ui.comboBox_project.findText(recentPrj)

			if not index is False :
				self.ui.comboBox_project.setCurrentIndex(index)
				nuke.tprint("recent project  : " + recentPrj)
			else :
				nuke.tprint("Index not found" + str(index))
		else :
			nuke.tprint("recent project not found : " + str(recentPrj))

	def _setSequenceComboBox(self):
		''' Setup sequence combo box from given project name '''
		
		self.ui.comboBox_sequence.clear()
		seqList = core.listAllSequence( str(getInfo.nukeScriptsPath) )
		# nuke.tprint(seqList)

		# Add seq to seq_combobox
		self.ui.comboBox_sequence.addItems(seqList)

		# Setup current path 
		self.ui.label_currentPath.setText(getInfo.nukeScriptsPath)

		# Setup last time used sequence
		recentSeq = core.get_recentWorkingSequence()
		if recentSeq :
			index = self.ui.comboBox_sequence.findText(recentSeq)

			if not index is False :
				self.ui.comboBox_sequence.setCurrentIndex(index)
				nuke.tprint("recent sequence : " + recentSeq)
			else :
				nuke.tprint("Index not found" + str(index))
		else :
			nuke.tprint("recent Sequence not found : " + str(recentSeq))

	def _setScriptShotList(self):

		self.ui.listWidget_scriptVersion.clear()
		self.ui.listWidget_scriptShot.clear()
		current_seq = self.ui.comboBox_sequence.currentText()

		allShot = core.listAllShot( getInfo.nukeScriptsPath, current_seq )
		self.ui.listWidget_scriptShot.addItems(allShot)

		# Setup last time used shot
		recentShot = core.get_recentWorkingShot()
		if recentShot :
			item = self.ui.listWidget_scriptShot.findItems(recentShot, Qt.MatchExactly)[0]

			if not item is False :
				self.ui.listWidget_scriptShot.setCurrentItem(item)
				nuke.tprint("recent shot     : " + recentShot)
			else :
				nuke.tprint("Item not found" + recentShot)
		else :
			nuke.tprint("recent Shot not found : " + str(recentShot))

	def _setScriptVersionList(self):
		''' Setup script listWidget '''

		current_seq  = self.ui.comboBox_sequence.currentText()
		current_shot = self.ui.listWidget_scriptShot.currentItem().text()

		# Setup current path 
		currentPath = getInfo.nukeScriptsPath	+ '/' +"{seq}_{shot}".format(seq = current_seq, shot = current_shot)
		self.ui.label_currentPath.setText(currentPath)

		versionlist = core.listAllVersion( nukeScriptsPath = getInfo.nukeScriptsPath , seq = current_seq, shot = current_shot)

		self.ui.listWidget_scriptVersion.clear()

		for fileName in versionlist :
			item = QListWidgetItem(fileName)
			item.setData(Qt.UserRole, core.objString(currentPath+'/'+fileName))

			self.ui.listWidget_scriptVersion.addItem(item)

		# show thumbnail
		try :
			thumbnailPath = core.getThumbnail(shotDirPath = currentPath, perfile = False )
			self._setThumbnail(thumbnailPath)
		except Exception as e :
			nuke.tprint(str(e))

	def _versionOnclicked(self):
		''' version in listwidget on clicked '''
		currentPath = self.ui.label_currentPath.text()
		scriptPath  = self.ui.listWidget_scriptVersion.currentItem().data( Qt.UserRole ).getString()
		scriptname  = os.path.splitext( os.path.basename(scriptPath) )[0] + '.png'

		# show thumbnail
		try :
			thumbnailPath = core.getThumbnail(shotDirPath = currentPath, filename = scriptname, perfile = True )
			self._setThumbnail(thumbnailPath)
		except Exception as e :
			nuke.tprint(str(e))

	def _openExplorer(self):
		''' open in explorer '''

		currentPath = self.ui.label_currentPath.text()

		if os.path.exists(currentPath):
			core.openExplorer(currentPath)
		else :
			nuke.tprint("Path not exists : " + currentPath)

	def _addShot(self):
		''' Add shot folder '''
		current_seq  = self.ui.comboBox_sequence.currentText()

		is_folderExists =  True
		while is_folderExists :
			shotname, ok = QInputDialog.getText(self, "Shot name :", "message")
			if ok :
				folderName = "{seq}_{shot}".format(seq = current_seq, shot = shotname)
				is_folderExists =  folderName in os.listdir( getInfo.nukeScriptsPath )
			else :
				return

		folderPath = getInfo.nukeScriptsPath + '/' + folderName
		os.mkdir( folderPath )

		self._setScriptShotList()
		
	def _setThumbnail(self, imagePath):

		missThumbnail_path  = getEnv.data_dirPath() + '/thumbnail_miss.jpg'

		# if not os.path.exists(imagePath) or imagePath == missThumbnail_path :
		# 	imagePath = missThumbnail_path
		# 	pixmap = QPixmap( imagePath )
		# 	pixmap = pixmap.scaledToHeight(180)
		# 	self.ui.thumbnail_placeholder.setPixmap(pixmap)
		# 	return

		pixmap = QPixmap( imagePath )
		pixmap = pixmap.scaledToHeight(180)
		self.ui.thumbnail_placeholder.setPixmap(pixmap)

	def _openScript(self):
		# get path
		scriptPath  = self.ui.listWidget_scriptVersion.currentItem().data( Qt.UserRole ).getString()
		current_prj = self.ui.comboBox_project.currentText()
		current_seq = self.ui.comboBox_sequence.currentText()
		current_shot= self.ui.listWidget_scriptShot.currentItem().text()
		
		# if nuke.Root().modified() :
		# 	# Confirm dialog
		# 	pass

		nuke.scriptOpen(scriptPath)
		core.save_recentWorkingSpace(project = current_prj ,seq = current_seq, shot = current_shot )

	def _saveScript(self):

		projectCode  = getInfo.projectCode
		currentpath  = self.ui.label_currentPath.text() 
		current_prj  = self.ui.comboBox_project.currentText()
		current_seq  = self.ui.comboBox_sequence.currentText()
		current_shot = self.ui.listWidget_scriptShot.currentItem().text()

		# define version
		if not os.listdir(currentpath) :
			# - create version 0001
			version = 1
		
		else :
			# - create increment verison
			version = getInfo.get_nextVersion() # INT

		filename = "{code}_{seq}_{shot}_comp_v{version}_{user}.nk".format( code = projectCode,
																			seq = current_seq,
																			shot = current_shot,
																			version = "%04d"%version,
																			user = getInfo.get_user())

		
		savePath = currentpath + '/' + filename

		# Save thumbnail
		core.saveFrame(thumbnailPath = currentpath + '/_thumbnail/'+ filename.replace(".nk", ".png") )

		# Save recent working space
		core.save_recentWorkingSpace(project = current_prj ,seq = current_seq, shot = current_shot )

		# Save Nuke script
		nuke.scriptSaveAs(savePath)
		nuke.tprint("save : " + filename)

		# Update version list in UI
		self._setScriptVersionList()

#####################################################################

def run():
	# clearUI()
	app = nuke_projectExplorer( )
	app.ui.show()

if __name__ == '__main__':
	run()