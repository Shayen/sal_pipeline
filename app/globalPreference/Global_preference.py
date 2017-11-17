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
	getEnv 	= env.getEnv()
	modulepath = getEnv.modulePath()

except ImportError :
	modulepath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-2] )
	print modulepath

__app_version__ = '1.0'
# v1.0 : init app

def confirmDialog( parent=None, title ='title', message='message?' ):
	'''  
		input dialog template

		@parent
		@title
		@message

		return : input message, False if cancle
	'''

	if parent == None:
		parent = QWidget()

	msgBox = QMessageBox(parent)
	msgBox.setText(title)
	msgBox.setInformativeText(message)
	msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
	msgBox.setDefaultButton(QMessageBox.Save)
	ret = msgBox.exec_()

	if ret == QMessageBox.Yes:
	    # Save was clicked
	    return True

	elif ret == QMessageBox.Cancel:
	    # cancel was clicked
	    return False

	else:
	    # should never be reached
	    return False

class sal_globalPreference( QMainWindow ):

	def __init__(self, parent=None):
		""" Description """
		QMainWindow.__init__(self, parent)

		_configureFileName 				= 'configure.json'
		self.databaseFilePath 			= "{0}/data/{1}".format(modulepath,_configureFileName)
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
		self._setup_accountListWidget()

		self.ui.tableWidget_accout.setColumnWidth(0, 250)
		self.ui.tableWidget_accout.setColumnWidth(1, 150)
		self.ui.tableWidget_accout.setColumnWidth(2, 100)
	def _initConnect(self):
		self.ui.buttonBox_main.accepted.connect( self._updateConfigFile )

		self.ui.pushButton_add_project.clicked.connect(self.pushButton_add_project_onclick)
		self.ui.pushButton_addUser.clicked.connect( self.pushButton_addUser_onclick )
		self.ui.pushButton_deleteUser.clicked.connect(self.pushButton_deleteUser_onclick)

	def _setup_accountListWidget(self):
		data = self.database.copy()
		# self.ui.tableWidget_accout.clear()

		self.ui.tableWidget_accout.setRowCount( len(data['username'].keys()) )

		row = 0
		for computer_name in data['username'].keys() : 

			username = data['username'][computer_name]

			# username
			username_item 		= QTableWidgetItem()
			username_item.setText(computer_name)

			# computer name
			computer_name_item 	= QTableWidgetItem()
			computer_name_item.setText( username)

			# set item
			self.ui.tableWidget_accout.setItem(row,0,computer_name_item)
			self.ui.tableWidget_accout.setItem(row,1,username_item)

			row += 1

	def pushButton_addUser_onclick(self):
		''' add blank row to tableWidget_accout '''
		account_rowCount = self.ui.tableWidget_accout.rowCount()

		self.ui.tableWidget_accout.setRowCount(account_rowCount+1)

	def pushButton_deleteUser_onclick(self):
		''' delete selected roe from pushButton_deleteUser '''
		currentRow = self.ui.tableWidget_accout.currentRow()

		username = self.ui.tableWidget_accout.item(currentRow,0).text()
		is_confirm = confirmDialog(parent = self.ui, title = "Remove user !!", message = 'Do you want to delete \"%s\"'%(username))

		# delete row, True
		if is_confirm:
			self.ui.tableWidget_accout.removeRow(currentRow)

	def pushButton_add_project_onclick(self):
		''' add blank project setting widget to project listWidget '''
		item_widget = self._load_projectWidget()
		item 		= QListWidgetItem(self.ui.listWidget_projectData)

		item.setSizeHint( item_widget.sizeHint() )

		self.ui.listWidget_projectData.addItem( item )
		self.ui.listWidget_projectData.setItemWidget( item, item_widget)

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
			item_widget.checkBox_active.setChecked(is_active)

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
		data = json.load( open(self.databaseFilePath, 'r') )

		self.database = data
		return data

	def _collectProjectData(self):
		''' 
			collect project setting data from WIDGET
		
			# :: EXAMPLE ::
			output :{
					  "Pipeline_Project": {
					    "active": false, 
					    "project_path": "D:/WORK/Pipeline_projectSetup", 
					    "project_name": "Pipeline_Project", 
					    "project_code": "plp"
					  }, 
					  "Vision": {
					    "active": true, 
					    "project_path": "P:/Vision", 
					    "project_name": "Vision", 
					    "project_code": "vis"
					  }
					}
		'''
		projectData = {}
		widgetItem_count = self.ui.listWidget_projectData.count()
		all_widgetItem 	 = [ self.ui.listWidget_projectData.item(i) for i in range(widgetItem_count) ]

		for widgetItem in all_widgetItem:
			project_name = self.ui.listWidget_projectData.itemWidget(widgetItem).lineEdit_projectName.text()

			projectData[project_name] 					= {}
			projectData[project_name]['project_name'] 	= self.ui.listWidget_projectData.itemWidget(widgetItem).lineEdit_projectName.text()
			projectData[project_name]['project_code']	= self.ui.listWidget_projectData.itemWidget(widgetItem).lineEdit_projectCode.text()
			projectData[project_name]['project_path']	= self.ui.listWidget_projectData.itemWidget(widgetItem).lineEdit_projectPath.text()
			projectData[project_name]['active']			= self.ui.listWidget_projectData.itemWidget(widgetItem).checkBox_active.isChecked()

		return projectData

	def _collectAccountData(self):
		''' WIP '''
		account_data = {}
		account_rowCount = self.ui.tableWidget_accout.rowCount()

		for row in range(account_rowCount):
			username 	= self.ui.tableWidget_accout.item(row,0).text()
			computerName= self.ui.tableWidget_accout.item(row,1).text()

			account_data[computerName] = username
		return account_data

	def _updateConfigFile(self):
		''' save all update data '''

		# collect project setting data -----------
		projectData = self._collectProjectData()

		#check active state
		active_count = 0
		project_code_list = []

		for project in projectData.keys() :
			project_name 	= projectData[project]['project_name']
			project_code 	= projectData[project]['project_code']
			project_path 	= projectData[project]['project_path']
			project_active 	= projectData[project]['active']

			# check blank field
			if project_name == "" or project_code == "" or project_path == "" :
				print ("Please complete all project infomation : %s"%project_name)
				return False

			# if blank all field, ignore item
			elif project_name == "" and project_code == "" and project_path == "" :
				del projectData[project]
				continue

			# check duplicate project code
			if project_code in project_code_list:
				print ("Do not duplicate project code : %s"%project_code)
				return False

			if project_active == True:
				active_count += 1

			project_code_list.append(project_code)


		if active_count > 1 :
			print ("Only one project can active, Please check !!")
			return False
		elif active_count < 1 :
			print ("Please select active project !!")
			return False

		# collect account setting data -----------
		accountData = self._collectAccountData()

		is_success = projectData and accountData
		is_confirm = confirmDialog(parent = self.ui, title = "Update Config !!", message = 'Do you want to update config file?')

		data = {"setting":{"projects":projectData}, "username":accountData}

		if is_success and is_confirm :


			# skip when data not modified.
			if data != self.database:
				print( json.dumps(data,indent=2) )
				json.dump(data, open(self.databaseFilePath ,'w') )

				print ("Update success.")

			self.close()

if __name__ == "__main__":
    app  = QApplication(sys.argv) 
    form = sal_globalPreference()
    app.exec_()