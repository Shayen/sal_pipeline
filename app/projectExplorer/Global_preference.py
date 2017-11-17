# Global preference

import os, sys, json

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

try:
	from sal_pipeline.src import env
	reload(env)
	modulepath = getEnv.modulePath()

except ImportError :
	modulepath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-2] )
	print modulepath

__app_version__ = '0.1'

class sal_globalPreference( QMainWindow ):

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		self.configureFileName 			= 'configure.json'
		self._projectWidgetUIFilename_ 	= 'Global_preference_window_projectWidget.ui'

		_uiFilename_ = 'Global_preference_window.ui'
		_uiFilePath_ = modulepath + '/ui/' + _uiFilename_		

		# Check is ui file exists?
		if not os.path.isfile( _uiFilePath_ ):
			print( 'File ui not found : %s'%_uiFilePath_ )
			return

		# ---- LoadUI -----
		loader = QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QFile( _uiFilePath_ )
		file.open(QFile.ReadOnly)
		self.ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		self.ui.setWindowTitle('Global preference v.' + str(__app_version__))

		self._loadDatabase()

		self._initUI()
		self._initConnect()

		self.ui.show()

	def _initUI(self):
		self._setup_prejectSettingItem()

	def _initConnect(self):
		pass

	def _setup_prejectSettingItem(self):
		''' load project setting widget to Project's Listwidget '''
		data = self.database.copy()

		for project_name in data['setting']['projects'].keys() :

			projectData  = data['setting']['projects'][project_name]
			project_code = projectData['project_code']
			projectpath  = projectData['project_path']
			is_active 	 = projectData['active']

			item_widget = self._load_projectWidget()
			item 		= QListWidgetItem(self.ui.listWidget_projectData)

			item_widget.lineEdit_projectName.setText(project_name)
			item_widget.lineEdit_projectCode.setText(project_code)
			item_widget.lineEdit_projectPath.setText(projectpath)
			item_widget.checkBox_active.setChecked(True)

			item.setSizeHint( item_widget.sizeHint() )

			self.ui.listWidget_projectData.addItem( item )
			self.ui.listWidget_projectData.setItemWidget( item, item_widget)

	def _load_projectWidget(self):
		''' description '''
		
		_uiFilePath_ = modulepath + '/ui/' + self._projectWidgetUIFilename_		

		# Check is ui file exists?
		if not os.path.isfile( _uiFilePath_ ):
			print( 'File ui not found : %s'%_uiFilePath_ )
			return

		# ---- LoadUI -----
		loader = QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QFile( _uiFilePath_ )
		file.open(QFile.ReadOnly)
		ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		return ui

	def _loadDatabase(self):
		""" read config data from './configure.json' """
		databaseFilePath = "{0}/data/{1}".format(modulepath,self.configureFileName)
		data = json.load( open(databaseFilePath, 'r') )

		self.database = data
		return data

if __name__ == "__main__":
    app  = QApplication(sys.argv) 
    form = sal_globalPreference()
    app.exec_()