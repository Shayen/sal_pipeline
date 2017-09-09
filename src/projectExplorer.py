import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as apiUI
import shiboken

from functools import partial
import PySide.QtCore as QtCore
import PySide.QtGui	 as QtGui
import PySide.QtUiTools as QtUiTools
import os, sys, subprocess

from sal_pipeline.src import env
from sal_pipeline.src import utils
from sal_pipeline.ui  import custom_widget
reload(custom_widget)
reload(utils)
reload(env)

getEnv 	= env.getEnv()
getInfo = env.getInfo()
# print os.path.dirname( os.path.abspath(__file__) )
modulepath = getEnv.modulePath()


# make unclickable object clickable.
def clickable(widget):
 
	class Filter(QtCore.QObject):
	 
		clicked = QtCore.Signal()
		 
		def eventFilter(self, obj, event):
		 
			if obj == widget:
				if event.type() == QtCore.QEvent.MouseButtonRelease:
					if obj.rect().contains(event.pos()):
						self.clicked.emit()
						# The developer can opt for .emit(obj) to get the object within the slot.
						return True
			 
			return False
	 
	filter = Filter(widget)
	widget.installEventFilter(filter)
	return filter.clicked

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def objString(string):

	class objectString(object):
		def __init__(self, *args):
			self.text = args[0]

		def getString(self):
			return self.text

	data = objectString( string )
	return data

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
		self.refresh('sequence_list')

		self.ui.show()

	def initUI(self):

		self.ui.label_myAccount.setText( getInfo.user )
		self.ui.listWidget_object_center.setSpacing(2)

		self.ui.addSequence_pushButton.clicked.connect(self.addSequence_pushButton_onClick)
		self.ui.addAsset_pushButton.clicked.connect(self.addAsset_pushButton_onClick)
		self.ui.addTask_pushButton.clicked.connect(self.addTask_pushButton_onClick)
		self.ui.pushButton_open.clicked.connect(self.pushButton_open_onClick)
		self.ui.pushButton_openExplorer.clicked.connect(self.openExplorer_onclick )
		self.ui.pushButton_saveIncrement.clicked.connect(self.pushButton_saveIncrement_onclick)
		self.ui.pushButton_addnewCentralItem.clicked.connect(self.pushButton_addnewCentralItem_onClick)

		# Make QLabel object cliackable.
		clickable(self.ui.label_path_editable).connect( self.openExplorer_onclick )

		self.ui.comboBox_project.activated.connect(self.project_select)
		self.ui.listWidget_asset.itemSelectionChanged.connect(self.listWidget_asset_itemSelectionChanged)
		self.ui.listWidget_sequence.itemSelectionChanged.connect(self.listWidget_sequence_itemSelectionChanged)
		self.ui.listWidget_task.itemClicked.connect(self.listWidget_task_itemSelectionChanged)
		self.ui.tabWidget.currentChanged.connect(self.tabWidget_currentChanged)
		self.ui.listWidget_object_center.itemClicked.connect(self.listWidget_object_center_itemClicked)
		self.ui.listWidget_version.itemClicked.connect(self.listWidget_version_itemClicked)

	def refresh(self,section):
		''' 
			refresh 

			@section : section to refresh
		'''

		if section == 'project':
			self.ui.comboBox_project.addItem( getInfo.projectName )
			self.ui.comboBox_project.setCurrentIndex(1)

			result = True

		# // Update task_list
		elif section == 'task_list':

			#
			self.ui.listWidget_task.clear()

			tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
			
			#  // tab is assets
			if tabText == 'assets':

				self.ui.groupBox_task.setTitle('Task')

				currentItem 	  = self.ui.listWidget_asset.currentItem()
				currentAssetsItem = self.ui.listWidget_object_center.currentItem()
				filename_ma 	  = self.ui.listWidget_object_center.itemWidget( currentAssetsItem )

				if not currentItem or not currentAssetsItem or not filename_ma:
					return
				else:
					currentItem 	  = currentItem.text()
					currentAssetsItem = currentAssetsItem.text()
					filename_ma   	  = filename_ma.filename(True)


				path =  getInfo.productionPath + '/' + tabText + '/' + currentItem + '/' + filename_ma + '/' + 'scenes'

				if not os.path.exists(path):
					return

				for i in os.listdir(path):
					self.ui.listWidget_task.addItem(i)
				result = filename_ma

			# // tab is shots
			else :


				if not self.ui.listWidget_sequence.currentItem() or not self.ui.listWidget_object_center.currentItem():
					return

				currentSequence = self.ui.listWidget_sequence.currentItem().text()
				currentShot		= self.ui.listWidget_object_center.currentItem()

				if not currentShot :
					print ('return.')
					return

				shotName 		= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)
				path 			= '%s/%s/%s/%s'%(getInfo.filmPath,currentSequence,shotName,'scenes')

				# // list all dir, ignore 'edits' folder
				dirList = [i for i in os.listdir(path) if i != 'edits']

				print '>',
				print dirList

				if dirList == [] :
					self.ui.listWidget_task.addItem('-- no task --')

				for i in dirList:

					self.ui.listWidget_task.addItem(i)

				result = path

			self.ui.listWidget_task.setCurrentRow(0)

		# // Update asset_list
		elif section == 'asset_list':

			#
			self.ui.listWidget_asset.clear()

			for mytype in os.listdir( getInfo.assetPath ):
				if os.path.isdir(getInfo.assetPath + '/' + mytype):
					self.ui.listWidget_asset.addItem( mytype )

			result = True

		# // Update sequence_list
		elif section == 'sequence_list':

			#
			self.ui.listWidget_sequence.clear()

			for mytype in os.listdir( getInfo.filmPath ):
				if os.path.isdir(getInfo.filmPath + '/' + mytype):
					self.ui.listWidget_sequence.addItem( mytype )

			result = True

		# // Update center list widget
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

				path =  getInfo.assetPath + '/' + currentAssetsItem
				for mytype in os.listdir( path ):

					workspace = '%s/%s'%( path, mytype) 
					# thumbnail_path = "C:/Users/siras/Pictures/14936969_1362716400413980_313115908_n.jpg"
					thumbnail_path = workspace + '/thumbnail.jpg'
					if not os.path.exists( thumbnail_path ) :
						thumbnail_path = getInfo.get_ProjectPath() + '/thumbnail_miss.jpg'

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

					self.ui.listWidget_object_center.addItem( item )
					self.ui.listWidget_object_center.setItemWidget( item, item_widget)

			# Tab is shots
			else:

				currentSeqItem = self.ui.listWidget_sequence.currentItem()

				if not currentSeqItem :
					return

				else:
					currentSeqItem = currentSeqItem.text()
					path =  getInfo.filmPath + '/' +  currentSeqItem 

				for mytype in os.listdir( path ):

					workspace = '%s/%s'%( path, mytype) 
					# thumbnail_path = "C:/Users/siras/Pictures/14936969_1362716400413980_313115908_n.jpg"
					thumbnail_path = workspace + '/thumbnail.jpg'
					if not os.path.exists( thumbnail_path ) :
						thumbnail_path = getInfo.get_ProjectPath() + '/thumbnail_miss.jpg'

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

					self.ui.listWidget_object_center.addItem( item )
					self.ui.listWidget_object_center.setItemWidget( item, item_widget)

			result = True

		# update version list
		elif section == 'version':

			self.ui.listWidget_version.clear()
			tabText 	= self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
			currentTask	= self.ui.listWidget_task.currentItem()

			# Tab is Assets
			if tabText == 'assets':

				currentSubType 	= self.ui.listWidget_asset.currentItem()
				currentAssets  	= self.ui.listWidget_object_center.currentItem()
				task 			= currentTask
				
				if not currentSubType or not currentAssets or not task:
					return

				path = self.ui.label_path_editable.text()

				if not os.path.exists(path):
					print ('Path not exists.')
					return

				# list all dir, ignore 'edits' folder
				dirList = [i for i in os.listdir(path) if i != 'edits']

				for i in dirList:
					item = QtGui.QListWidgetItem(i)
					# item.setText(i)
					item.setData(QtCore.Qt.UserRole, objString(path+'/'+i))
					self.ui.listWidget_version.addItem(item)

				result = True

			# Tab is shots
			else :

				currentSequence = self.ui.listWidget_sequence.currentItem()
				currentShot		= self.ui.listWidget_object_center.currentItem()

				if not currentSequence or not currentShot or not currentTask:
					return

				currentSequence = currentSequence.text()
				shotName 		= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)
				currentTask 	= currentTask.text()

				path = '%s/%s/%s/%s/%s'%(getInfo.filmPath,currentSequence,shotName,'scenes',currentTask)

				if not os.path.exists(path):
					print ('Path not exists.')
					return

				# list all dir, ignore 'edits' folder
				dirList = [i for i in os.listdir(path) if i != 'edits']

				for i in dirList:
					item = QtGui.QListWidgetItem(i)
					# item.setText(i)
					item.setData(QtCore.Qt.UserRole, objString(path+'/'+i))
					self.ui.listWidget_version.addItem(item)

				result = True

		else:
			result = False

		return result

	def project_select(self):
		currenttext = self.ui.comboBox_project.currentText()
		print currenttext

	def listWidget_asset_itemSelectionChanged(self):
		currentItem = self.ui.listWidget_asset.currentItem().text()
		self.refresh('center')

		path = getInfo.projectPath + '/production/assets/' + currentItem
		self.ui.label_path_editable.setText(path)
		
		self.refresh('task_list')

		# Update current path
		# self.ui.label_path_editable.setText( path )

	def listWidget_sequence_itemSelectionChanged(self):
		currentItem = self.ui.listWidget_sequence.currentItem().text()
		
		self.refresh('center')
		self.refresh('task_list')

		path = "%s/%s"%(getInfo.filmPath, currentItem)

		# Update current path
		self.ui.label_path_editable.setText( path )

	def listWidget_task_itemSelectionChanged(self):
		# print 'x'

		currentItem = self.ui.listWidget_task.currentItem().text()
		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )

		if not self.ui.listWidget_object_center.currentItem() :
			self.ui.listWidget_task.clear()
			return

		# Tab is Assets
		if tabText == 'assets':
			assetsType = self.ui.listWidget_asset.currentItem().text()
			assetsItem	= self.ui.listWidget_object_center.currentItem()
			assetsName 	= self.ui.listWidget_object_center.itemWidget( assetsItem ).filename(True)			
			path =  getInfo.productionPath + '/' + tabText + '/' + assetsType + '/' + assetsName + '/scenes/' + currentItem

		# Tab is shot
		else: 
			sequenceItem = self.ui.listWidget_sequence.currentItem().text()
			currentShot	= self.ui.listWidget_object_center.currentItem()
			shotName 	= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)			

			# path =  getInfo.filmPath + '/' +  sequenceItem + shotName + '/scenes/' + currentItem
			path = "%s/%s/%s/scenes/%s"%( getInfo.filmPath, sequenceItem, shotName, currentItem )

		self.refresh(section = 'version')

		# print path
		# // Update current path
		self.ui.label_path_editable.setText( path )

	def listWidget_object_center_itemClicked(self):

		
		currentItem	= self.ui.listWidget_object_center.currentItem()
		filename 	= self.ui.listWidget_object_center.itemWidget( currentItem ).filename(True)
		
		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )

		if tabText == 'assets':
			assetType = self.ui.listWidget_asset.currentItem().text()
			path = getInfo.projectPath + '/production/assets/' + assetType + '/' + filename
		else :

			sequence  = self.ui.listWidget_sequence.currentItem().text()
			path = getInfo.projectPath + '/production/film/' + sequence + '/' + filename

		self.ui.label_path_editable.setText(path)
		self.refresh('task_list')

	def listWidget_version_itemClicked(self):

		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
		filePath = self.ui.listWidget_version.currentItem().data( QtCore.Qt.UserRole ).getString()
		# self.ui.label_path_editable.setText( filePath )

		# When working on assets
		if tabText == 'assets':

			currentSubType = self.ui.listWidget_asset.currentItem()
			currentAssets  = self.ui.listWidget_object_center.currentItem()

			if not sequence or not currentAssets :
				return

			else:
				currentSubType = sequcurrentSubTypeence.text()
				currentAssets  = currentAssets.text()

		# When working on shot		
		else:

			sequence 	= self.ui.listWidget_sequence.currentItem()
			currentShot	= self.ui.listWidget_object_center.currentItem()
			shotName 	= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)

			if not sequence or not currentShot:
				return
			else:
				sequence = sequence.text()
		

	def tabWidget_currentChanged(self):
		
		self.ui.listWidget_object_center.clear()
		self.refresh('asset_list')
		self.refresh('sequence_list')
		self.refresh('center')
		self.refresh('version')
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
		
		self.ui.label_path_editable.setText(path)
		self.refresh('sequence_list')

	def addAsset_pushButton_onClick(self):
		self.refresh('asset_list')

	def pushButton_open_onClick(self):
		'''
			Open file from given path
		'''

		filePath = self.ui.listWidget_version.currentItem().data( QtCore.Qt.UserRole ).getString()
		# self.ui.label_path_editable.setText( filePath )

		if os.path.exists(filePath) :

			# // When file have some change
			if cmds.file(q=True, modified=True) :

				result =cmds.confirmDialog(	title 		=  'Save file',
											message 	=  'File is unsave, Save this file?', 
											button 		=  ['Yes','No'], 
											defaultButton= 'Yes', 
											cancelButton = 'No', 
											dismissString= 'No' 
											)

				# When user say 'YES' then Save file
				if result == 'Yes':
					cmds.SaveScene()
				else:
					# return False
					pass

			# Flush scene
			cmds.file( new = True, force = True ) 
			# Open mayafile
			print ('Opening file : ' + filePath)
			try:
				cmds.file(filePath, o=True)
				workspace = getInfo.get_workspace()
				print ('setup workspace : ' + workspace)
				mel.eval( 'setProject "'+ workspace +'";')

			except Exception as e:
				raise e

	def openExplorer_onclick(self):
		'''
			open Explorer
		'''
		path = self.ui.label_path_editable.text()
		if os.path.exists( path ):
			openExplorer(path)
		else :
			cmds.error('Path not found')

	def pushButton_saveIncrement_onclick(self):

		# When file have some change
		if cmds.file(q=True, modified=True) :

			result =cmds.confirmDialog(	title 		=  'Save file',
										message 	=  'File is unsave, Save this file?', 
										button 		=  ['Yes','No'], 
										defaultButton= 'Yes', 
										cancelButton = 'No', 
										dismissString= 'No' 
										)

			# When user say 'YES' then Save file
			if result == 'Yes':
				cmds.SaveScene()
			else:
				# return False
				pass

		currentPath = self.ui.label_path_editable.text()
		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )

		sequence 	= self.ui.listWidget_sequence.currentItem()
		currentShot	= self.ui.listWidget_object_center.currentItem()
		task 		= self.ui.listWidget_task.currentItem()

		currentSubType = self.ui.listWidget_asset.currentItem()
		currentAssets  = self.ui.listWidget_object_center.currentItem()

		if tabText == 'shots':
			if not sequence or not currentShot or not task:
				return
		else :
			if not currentSubType or not currentAssets or not task:
				return

		if os.listdir( currentPath ) != [] :

			if tabText == 'shots':
			
				# Create next version
				lastfilename = [ file for file in os.listdir( currentPath ) if os.path.isfile( currentPath +'/' + file ) ][-1]
				
				workType 	= 'film'
				sequence 	= sequence.text()
				shotName 	= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)
				task 		= task.text()
				user 		= getInfo.get_user()

				version = lastfilename.split('_')[-2]
				version = int ( version.replace('v','') )
				version = 'v%03d'%(version + 1)
				
				filename = '_'.join( [ getInfo.projectCode, sequence, shotName, task, version, user+'.ma' ] )

			else :

				# Create next version
				lastfilename = [ file for file in os.listdir( currentPath ) if os.path.isfile( currentPath +'/' + file ) ][-1]
				
				workType  	= 'assets'
				assetType 	= currentSubType.text()
				assetName 	= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)
				task 		= task.text()
				user 		= getInfo.get_user()

				version = lastfilename.split('_')[-2]
				version = int ( version.replace('v','') )
				version = 'v%03d'%(version + 1)
				
				filename	= '_'.join( [ getInfo.projectCode, assetType, assetName, task, version, user+'.ma' ] ) 


		# Create file version 001
		else:

			if tabText == 'shots':

				workType 	= 'film'
				sequence 	= sequence.text()
				shotName 	= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)
				task 		= task.text()
				user 		= getInfo.get_user()

				filename	= '_'.join( [ getInfo.projectCode, sequence, shotName, task, 'v001', user+'.ma' ] ) 

			else :

				workType  	= 'assets'
				assetType 	= currentSubType.text()
				assetName 	= self.ui.listWidget_object_center.itemWidget( currentShot ).filename(True)
				task 		= task.text()
				user 		= getInfo.get_user()

				filename	= '_'.join( [ getInfo.projectCode, assetType, assetName, task, 'v001', user+'.ma' ] ) 

		try:
			# Save new version
			cmds.file( rename='%s/%s'%( currentPath, filename ) )
			result =  cmds.file( save=True, type='mayaAscii' )
			workspace = getInfo.get_workspace()
			print ('setup workspace : ' + workspace)
			mel.eval( 'setProject "'+ workspace +'";')

		except Exception as e:
			raise (e)

		# // return result

		if result :
			refresh_result = self.refresh('version')
			print result

	def addTask_pushButton_onClick(self):
		'''
			add task in scene' folder
		'''
		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
		
		# When working on assets
		if tabText == 'assets':

			currentSubType = self.ui.listWidget_asset.currentItem()
			currentAssets  = self.ui.listWidget_object_center.currentItem()

			if not currentSubType or not currentAssets :
				return

			else:
				currentSubType = sequcurrentSubTypeence.text()
				currentAssets  = currentAssets.text()

			# Description
			result = utils.windows().inputDialog(parent = self, title='new task', message = 'Task name...')
			
			if result == False :
				return

			# path = getInfo.assetPath + '/' + currentSubType + '/' + currentAssets + '/scenes/' + result
			path = '%s/%s/%s/scenes/%s'%( assetPath, currentSubType, currentAssets, result )

			# when folder exists
			while os.path.exists(path):
				result = utils.windows().inputDialog(parent = self, title='new task', message = 'task was exist...!!!\nObject name...')
			
				if result == False :
					return
				else :
					path = '%s/%s/%s/scenes/%s'%( assetPath, currentSubType, currentAssets, result )

			try:
				# Description
				os.mkdir(path)
				self.refresh('task')

			except Exception as e:
				raise(e)

			# 	# Description
			# 	utils.utils().unzip(zipPath = getEnv.assetTemplate_zipPath() ,dest = path)
			# 	print('Create new sequence success : ' + path)

			# except Exception as e:
			# 	raise(e)

		# When working on shot		
		else:

			sequence 	= self.ui.listWidget_sequence.currentItem()
			currentShot	= self.ui.listWidget_object_center.currentItem()
			shotName 	= self.ui.listWidget_object_center.itemWidget( currentShot )

			if not sequence or not currentShot:
				return
			else:
				sequence = sequence.text()
				shotName = shotName.filename(True)

			# Description
			result = utils.windows().inputDialog(parent = self, title='new task', message = 'Task name...')
			
			if result == False :
				return

			path = getInfo.filmPath + '/' + sequence + '/' + shotName + '/scenes/' + result

			# when folder exists
			while os.path.exists(path):
				result = utils.windows().inputDialog(parent = self, title='new Task', message = 'Task was exist...!!!\nObject name...')
			
				if result == False :
					return
				else :
					path = getInfo.filmPath + '/' + sequence + '/' + shotName + '/scenes/' + result

			try:
				# Description
				os.mkdir(path)
				self.refresh('task')
			except Exception as e:
				raise(e)

			# 	# Description
			# 	utils.utils().unzip(zipPath = getEnv.shotTemplate_zipPath() ,dest = path)
			# 	print('Create new sequence success : ' + path)

			# except Exception as e:
			# 	raise(e)

		self.refresh('center')

	def pushButton_addnewCentralItem_onClick(self):
		'''
			- Create new shot in shots mode
			- Create new task in assets mode
		'''

		print ('Onclicked')
		tabText = self.ui.tabWidget.tabText( self.ui.tabWidget.currentIndex() )
		
		# When working on assets
		if tabText == 'assets':

			print ('tabText : ' + tabText)

			currentSubType = self.ui.listWidget_asset.currentItem()
			currentAssets  = self.ui.listWidget_object_center.currentItem()

			if not currentSubType or not currentAssets :
				print ('Retuen.')
				return

			else:
				currentSubType = sequcurrentSubTypeence.text()
				currentAssets  = currentAssets.text()

			# Description
			result = utils.windows().inputDialog(parent = self, title='new task', message = 'Task name...')
			
			if result == False :
				return

			# path = getInfo.assetPath + '/' + currentSubType + '/' + currentAssets + '/scenes/' + result
			path = '%s/%s/%s/scenes/%s'%( assetPath, currentSubType, currentAssets, result )

			# when folder exists
			while os.path.exists(path):
				result = utils.windows().inputDialog(parent = self, title='new task', message = 'task was exist...!!!\nObject name...')
			
				if result == False :
					return
				else :
					path = '%s/%s/%s/scenes/%s'%( assetPath, currentSubType, currentAssets, result )
			
			try:
				# Description
				os.mkdir(path)

				# Description
				utils.utils().unzip(zipPath = getEnv.assetTemplate_zipPath() ,dest = path)
				print('Create new sequence success : ' + path)

			except Exception as e:
				raise(e)

		# When working on shot		
		else:

			print ('tabText : ' + tabText)

			sequence 	= self.ui.listWidget_sequence.currentItem()
			# currentShot	= self.ui.listWidget_object_center.currentItem()
			# shotName 	= self.ui.listWidget_object_center.itemWidget( currentShot )

			if not sequence :
				print ("return.")
				return
			else:
				sequence = sequence.text()
				# shotName = shotName.filename(True)

			# Description
			result = utils.windows().inputDialog(parent = self, title='new task', message = 'Task name...')
			
			if result == False or result == '' :
				return

			path = getInfo.filmPath + '/' + sequence + '/' + result

			# when folder exists
			while os.path.exists(path):
				result = utils.windows().inputDialog(parent = self, title='new Task', message = 'Task was exist...!!!\nObject name...')
			
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

		self.refresh('center')

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
	