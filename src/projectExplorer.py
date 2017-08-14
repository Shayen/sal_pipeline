import maya.cmds as cmds
import maya.OpenMayaUI as apiUI
import shiboken

import PySide.QtCore as QtCore
import PySide.QtGui	 as QtGui
import PySide.QtUiTools as QtUiTools
import os, sys

from sal_pipeline.src import env
from sal_pipeline.src import utils
from sal_pipeline.ui import custom_widget
reload(custom_widget)
reload(utils)
reload(env)

getEnv 	= env.getEnv()
getInfo = env.getInfo()
# print os.path.dirname( os.path.abspath(__file__) )
modulepath = getEnv.modulePath()

class salProjectExplorer( QtGui.QMainWindow ):
	"""A bare minimum UI class - showing a .ui file inside Maya 2016"""

	def __init__(self,parent=None):
		''' init '''
		QtGui.QMainWindow.__init__(self, parent)

		self._uiFilename_ = 'projectExplorer.ui'
		self._uiFilePath_ = modulepath + '/ui/' + self._uiFilename_

		# Check is ui file exists?
		if not os.path.isfile( self._uiFilePath_ ):
			cmds.error( 'File ui not found.' )

		# ---- LoadUI -----
		loader = QtUiTools.QUiLoader()
		currentDir = os.path.dirname(__file__)
		file = QtCore.QFile( self._uiFilePath_ )
		file.open(QtCore.QFile.ReadOnly)
		self.ui = loader.load(file, parentWidget=self)
		file.close()
		# -----------------

		self.initUI()

		self.refresh('project')
		# self.refresh('task_list')
		self.refresh('asset_list')
		self.refresh('shot_list')

		self.ui.show()

	def initUI(self):

		self.ui.label_myAccount.setText( getInfo.user )
		self.ui.listWidget_object_center.setSpacing(2)

		self.ui.addSequence_pushButton.clicked.connect(self.addSequence_pushButton_onClick)
		self.ui.addAsset_pushButton.clicked.connect(self.addAsset_pushButton_onClick)
		self.ui.addTask_pushButton.clicked.connect(self.addTask_pushButton_onClick)

		self.ui.comboBox_project.activated.connect(self.project_select)
		self.ui.listWidget_asset.itemSelectionChanged.connect(self.listWidget_asset_itemSelectionChanged)
		self.ui.listWidget_shots.itemSelectionChanged.connect(self.listWidget_shots_itemSelectionChanged)
		self.ui.listWidget_task.itemClicked.connect(self.listWidget_task_itemSelectionChanged)
		self.ui.tabWidget.currentChanged.connect(self.tabWidget_currentChanged)
		self.ui.listWidget_object_center.itemClicked.connect(self.listWidget_object_center_itemClicked)

	def refresh(self,section):
		''' 
			refresh 

			@section : section to refresh
		'''

		if section == 'project':
			self.ui.comboBox_project.addItem( getInfo.projectName )
			self.ui.comboBox_project.setCurrentIndex(1)

			result = True

		# Update task_list
		elif section == 'task_list':

			#
			self.ui.listWidget_task.clear()

			tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
			
			# tab is assets
			if tabText == 'assets':

				self.ui.groupBox_task.setTitle('Task')

				if not self.ui.listWidget_asset.currentItem():
					return

				currentItem = self.ui.listWidget_asset.currentItem().text()
				currentAssetsItem = self.ui.listWidget_object_center.currentItem()
				filename_ma = self.ui.listWidget_object_center.itemWidget( currentAssetsItem ).filename(True)
				# print help(item)
				# print currentAssetsItem
				path =  getInfo.productionPath + '/' + tabText + '/' + currentItem + '/' + filename_ma + '/' + 'scenes'

				for i in os.listdir(path):
					self.ui.listWidget_task.addItem(i)
				result = filename_ma

			# tab is shots
			else :

				self.ui.groupBox_task.setTitle('Shots')

				if not self.ui.listWidget_shots.currentItem():
					return

				currentItem = self.ui.listWidget_shots.currentItem().text()
				path =  getInfo.filmPath + '/' +  currentItem 

				for i in os.listdir(path):
					self.ui.listWidget_task.addItem(i)

				result = path

			self.ui.listWidget_task.setCurrentRow(0)

		# Update asset_list
		elif section == 'asset_list':

			#
			self.ui.listWidget_asset.clear()

			for mytype in os.listdir( getInfo.assetPath ):
				if os.path.isdir(getInfo.assetPath + '/' + mytype):
					self.ui.listWidget_asset.addItem( mytype )

			result = True

		# Update shot_list
		elif section == 'shot_list':

			#
			self.ui.listWidget_shots.clear()

			for mytype in os.listdir( getInfo.filmPath ):
				if os.path.isdir(getInfo.filmPath + '/' + mytype):
					self.ui.listWidget_shots.addItem( mytype )

			result = True

		elif section == 'center':
			
			self.ui.listWidget_object_center.clear()
			tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )

			if tabText == 'assets':
			
				#
				currentAssetsItem = self.ui.listWidget_asset.currentItem()

				if not currentAssetsItem:
					return				
				else :
					currentAssetsItem = currentAssetsItem.text()

				for mytype in os.listdir( getInfo.assetPath + '/' + currentAssetsItem ):

					thumbnail_path = "C:/Users/siras/Pictures/14936969_1362716400413980_313115908_n.jpg" 
					item = QtGui.QListWidgetItem(self.ui.listWidget_object_center)
					brush = QtGui.QBrush(QtGui.QColor(16, 65, 53))
					brush.setStyle(QtCore.Qt.SolidPattern)	
					item.setBackground(brush)
					item_widget = custom_widget.customWidgetFileExplorer()

					item_widget.setThumbnail( thumbnail_path )
					item_widget.setFilename( mytype )
					item_widget.setDateModified( '' )
					item_widget.setComment( '' )

					item.setSizeHint( item_widget.sizeHint() )

					# if os.path.isfile(getInfo.assetPath + '/' + mytype):
					self.ui.listWidget_object_center.addItem( item )
					self.ui.listWidget_object_center.setItemWidget( item, item_widget)
				#listWidget_object_center
				# item = QtGui.QListWidgetItem(self.listWidget)

			# Tab is shots
			else:

				currentSeqItem = self.ui.listWidget_shots.currentItem()

				if not currentSeqItem :
					return

				else:
					currentSeqItem = currentSeqItem.text()
					path =  getInfo.filmPath + '/' +  currentSeqItem 

				for mytype in os.listdir( path ):

					thumbnail_path = "C:/Users/siras/Pictures/14936969_1362716400413980_313115908_n.jpg" 
					item = QtGui.QListWidgetItem(self.ui.listWidget_object_center)
					brush = QtGui.QBrush(QtGui.QColor(16, 65, 53))
					brush.setStyle(QtCore.Qt.SolidPattern)	
					item.setBackground(brush)
					item_widget = custom_widget.customWidgetFileExplorer()

					item_widget.setThumbnail( thumbnail_path )
					item_widget.setFilename( mytype )
					item_widget.setDateModified( '' )
					item_widget.setComment( '' )

					item.setSizeHint( item_widget.sizeHint() )

					# if os.path.isfile(getInfo.assetPath + '/' + mytype):
					self.ui.listWidget_object_center.addItem( item )
					self.ui.listWidget_object_center.setItemWidget( item, item_widget)
				#listWidget_object_center
				# item = QtGui.QListWidgetItem(self.listWidget)

			result = True

		else:
			result = False

		return result

	def project_select(self):
		currenttext = self.ui.comboBox_project.currentText()
		print currenttext

	def listWidget_asset_itemSelectionChanged(self):
		currentItem = self.ui.listWidget_asset.currentItem().text()
		path = self.refresh('center')
		# path = self.refresh('task_list')

		# Update current path
		# self.ui.label_path_editable.setText( path )

	def listWidget_shots_itemSelectionChanged(self):
		currentItem = self.ui.listWidget_shots.currentItem().text()
		path = self.refresh('task_list')
		self.refresh('center')

		# Update current path
		self.ui.label_path_editable.setText( path )

	def listWidget_task_itemSelectionChanged(self):
		# print 'x'

		currentItem = self.ui.listWidget_task.currentItem().text()
		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )

		if tabText == 'assets':
			assetsItem = self.ui.listWidget_asset.currentItem().text()
			path =  getInfo.productionPath + '/' + tabText + '/' + assetsItem + '/' + currentItem
		else: 
			sequenceItem = self.ui.listWidget_shots.currentItem().text()
			path =  getInfo.filmPath + '/' +  sequenceItem + '/' + currentItem

		# print path
		# Update current path
		self.ui.label_path_editable.setText( path )

	def listWidget_object_center_itemClicked(self):
		self.refresh('task_list')

	def tabWidget_currentChanged(self):
		
		self.ui.listWidget_object_center.clear()
		self.refresh('asset_list')
		self.refresh('shot_list')
		self.refresh('center')
		self.refresh('task_list')

	def addSequence_pushButton_onClick(self):
		''' description '''
		result = utils.windows().inputDialog(parent = self, title='new folder', message = 'Object name...')
		
		if result == False :
			return

		path = getInfo.filmPath + '/' + result

		# when folder exists
		while os.path.exists(path):
			result = utils.windows().inputDialog(parent = self, title='new folder', message = ' name was exist...!!!\nObject name...')
		
			if result == False :
				return
			else :
				path = getInfo.filmPath + '/' + result

		try:
			os.mkdir(path)
			print('Create success.')
			# utils.utils().unzip(zipPath = getEnv.shotTemplate_zipPath() ,dest = path)
			# print('Create new sequence success : ' + path)
		except Exception as e:
			raise(e)
			
		self.refresh('shot_list')

	def addAsset_pushButton_onClick(self):
		self.refresh('asset_list')

	def addTask_pushButton_onClick(self):
		'''
			- Create new shot in shots mode
			- Create new task in assets mode
		'''

		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
		
		# Description
		if tabText == 'assets':

			currentSubType = self.ui.listWidget_asset.currentItem()
			currentAssets  = self.ui.listWidget_object_center.currentItem()

			if not sequence or not currentAssets :
				return

			else:
				currentSubType = sequcurrentSubTypeence.text()
				currentAssets  = currentAssets.text()

			# Description
			result = utils.windows().inputDialog(parent = self, title='new task', message = 'Task name...')
			
			if result == False :
				return

			path = getInfo.assetPath + '/' + currentSubType + '/' + currentAssets + '/' + 'scenes/' + result
			path = '%s/%s/%s/scenes/%s'%()

			# when folder exists
			while os.path.exists(path):
				result = utils.windows().inputDialog(parent = self, title='new shot', message = ' name was exist...!!!\nObject name...')
			
				if result == False :
					return
				else :
					path = getInfo.filmPath + '/' + sequence + '/' + result

			try:
				# Description
				os.mkdir(path)

				# Description
				utils.utils().unzip(zipPath = getEnv.shotTemplate_zipPath() ,dest = path)
				print('Create new sequence success : ' + path)

			except Exception as e:
				raise(e)

		# Description		
		else:

			sequence = self.ui.listWidget_shots.currentItem()
			if not sequence :
				return
			else:
				sequence = sequence.text()

			# Description
			result = utils.windows().inputDialog(parent = self, title='new shot', message = 'Shot name...')
			
			if result == False :
				return

			path = getInfo.filmPath + '/' + sequence + '/' + result

			# when folder exists
			while os.path.exists(path):
				result = utils.windows().inputDialog(parent = self, title='new shot', message = ' name was exist...!!!\nObject name...')
			
				if result == False :
					return
				else :
					path = getInfo.filmPath + '/' + sequence + '/' + result

			try:
				# Description
				os.mkdir(path)

				# Description
				utils.utils().unzip(zipPath = getEnv.shotTemplate_zipPath() ,dest = path)
				print('Create new sequence success : ' + path)

			except Exception as e:
				raise(e)

		self.refresh('task_list')

#####################################################################

def getMayaWindow():
	"""
	Get the main Maya window as a QtGui.QMainWindow instance
	@return: QtGui.QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QtGui.QWidget)

def clearUI():
	if cmds.window('sal_projectExplorer',exists=True):
		cmds.deleteUI('sal_projectExplorer')
		clearUI()

def run():
	clearUI()
	app = salProjectExplorer( getMayaWindow() )
	# pass

if __name__ == '__main__':
	app = salProjectExplorer()
	# app._uiFilePath_ = '/'.join( os.path.dirname(__file__).split('\\\\')[:-1] ) + '/ui/' + app._uiFilename_
	