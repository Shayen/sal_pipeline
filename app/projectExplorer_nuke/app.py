import sys, os
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
reload(env)
info = env.nuke_info()

__app_version__ = "v 0.1"
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

	def _initConnect(self):
		self.ui.pushButton_open.clicked.connect(self._openScript)
		self.ui.pushButton_save.clicked.connect(self._saveScript)

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
		

	def _openScript(self):
		pass

	def _saveScript(self):
		pass

#####################################################################

def listAllProject():
	data = getEnv.globalConfig_data
	return data['setting']['projects'].keys()
	# getInfo = env.getInfo(projectName = "Vision")

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