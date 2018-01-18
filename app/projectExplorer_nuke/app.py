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
import core
reload(env)
info = env.nuke_info()

__app_version__ = "0.1"
# V0.1

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

		self._initUI()
		self._initConnect()

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

		self.ui.listWidget_scriptShot.itemClicked.connect(self._setScriptVersionList)

	def _setProjectComboBox(self):
		''' Setup projectComboBox '''

		# Load all project name
		global getInfo

		self.ui.comboBox_project.clear()
		projectList = listAllProject()
		self.ui.comboBox_project.addItems( projectList )

		# get active project
		for project in getEnv.globalConfig_data['setting']['projects'].keys():
			if getEnv.globalConfig_data['setting']['projects'][project]['active'] == True:
				break

		getInfo = env.nuke_info(projectName = project)

		# Check project is ready to use
		activePrj = self.ui.comboBox_project.findText( project )
		self.ui.comboBox_project.setCurrentIndex(activePrj)

		result = True

	def _setSequenceComboBox(self):
		''' Setup sequence combo box from given project name '''
		
		self.ui.comboBox_sequence.clear()
		seqList = listAllSequence()
		nuke.tprint(seqList)

		# Add seq to seq_combobox
		self.ui.comboBox_sequence.addItems(seqList)

	def _setScriptShotList(self):

		self.ui.listWidget_scriptShot.clear()
		current_seq = self.ui.comboBox_sequence.currentText()

		allShot = listAllShot(current_seq)
		self.ui.listWidget_scriptShot.addItems(allShot)

	def _setScriptVersionList(self):
		''' Setup script listWidget '''

		current_seq  = self.ui.comboBox_sequence.currentText()
		current_shot = self.ui.listWidget_scriptShot.currentItem().text()

		# Setup current path 
		currentPath = getInfo.nukeScriptsPath	+ '/' +"{seq}_{shot}".format(seq = current_seq, shot = current_shot)
		self.ui.label_currentPath.setText(currentPath)

		versionlist = listAllVersion(seq = current_seq, shot = current_shot)

		self.ui.listWidget_scriptVersion.clear()

		for fileName in versionlist :
			item = QListWidgetItem(fileName)
			item.setData(Qt.UserRole, objString(currentPath+'/'+fileName))

			self.ui.listWidget_scriptVersion.addItem(item)

	def _openExplorer(self):
		''' open in explorer '''

		currentPath = self.ui.label_currentPath.text()

		if os.path.exists(currentPath):
			openExplorer(currentPath)

	def _openScript(self):
		# get path
		scriptPath = self.ui.listWidget_scriptVersion.currentItem().data( Qt.UserRole ).getString()

		# if nuke.Root().modified() :
		# 	# Confirm dialog
		# 	pass

		nuke.scriptOpen(scriptPath)

	def _saveScript(self):

		projectCode  = getInfo.projectCode
		currentpath  = self.ui.label_currentPath.text() 
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

		nuke.tprint(filename)
		savePath = currentpath + '/' + filename
		nuke.scriptSaveAs(savePath)

		self._setScriptVersionList()

#####################################################################

def listAllProject():
	data = getEnv.globalConfig_data
	return data['setting']['projects'].keys()
	# getInfo = env.getInfo(projectName = "Vision")

def listAllSequence():
	allShot = []

	nuke.tprint(getInfo.nukeScriptsPath)

	for dirName in [ item for item in os.listdir(getInfo.nukeScriptsPath) if os.path.isdir(getInfo.nukeScriptsPath + '/' + item) == True ]:
		seq = dirName.split('_')[0]
		if seq not in allShot :
			allShot.append(seq)

	# if find nothing return folder is empty
	if not allShot :
		allShot = '-- Empty --'

	return allShot

def listAllShot(currentSeq):
	allShot = []

	for dirName in [ item for item in os.listdir(getInfo.nukeScriptsPath) if os.path.isdir(getInfo.nukeScriptsPath + '/' + item) == True ]:
		seq = dirName.split('_')[0]
		if seq == currentSeq :
			allShot.append(dirName.split('_')[1])

	# if find nothing return folder is empty
	if not allShot :
		allShot = '-- Empty --'

	return allShot

def listAllVersion(seq,shot):
	_shot_dirName = "{seq}_{shot}".format(seq = seq, shot = shot)
	_shot_dirPath = os.path.join(getInfo.nukeScriptsPath, _shot_dirName) 

	return [item for item in os.listdir(_shot_dirPath) if os.path.isfile(_shot_dirPath + '/' + item) ]

def objString(string):

	class objectString(object):
		def __init__(self, *args):
			self.text = args[0]

		def getString(self):
			return self.text

	data = objectString( string )
	return data

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def run():
	# clearUI()
	app = nuke_projectExplorer( )
	app.ui.show()

if __name__ == '__main__':
	run()