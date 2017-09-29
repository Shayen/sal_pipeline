import os, sys, json, socket
import maya.cmds as cmds
import maya.mel as mel

modulePath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-1] )

class getEnv(object):

	def __init__(self):
		self._modulePath_ = modulePath
		self.shotTemplateFileName = 'shot_template.zip'
		self.projectTemplateFileName = 'projectSetup_template.zip'
		self.assetTemplateFileName = 'asset_template.zip'

	def modulePath(self):
		""" 
			return path of main module 

			return : "D:/WORK/Programming/sal_pipeline"
		"""
		path = self._modulePath_
		return path

	def ui_dirPath(self):
		return self._modulePath_ + '/ui'

	def src_dirPath(self):
		return self._modulePath_ + '/src'

	def data_dirPath(self):
		return self._modulePath_ + '/data'

	def log_dirPath(self):
		return self._modulePath_ + '/log'

	def shotTemplate_zipPath(self):
		return self.data_dirPath() + '/' + self.shotTemplateFileName

	def projectTemplate_zipPath(self):
		return self.data_dirPath() + '/' + self.projectTemplateFileName

	def assetTemplate_zipPath(self):
		return self.data_dirPath() + '/' + self.assetTemplateFileName

class getInfo(object):

	def __init__(self,path=None):

			# self.user = self.getUsername()

			self.filename = cmds.file( q=True, sn=True, shn=True )
			self.path 	  = cmds.file( q=True, sn=True )
		else:
			self.filename = path.split('/')[-1]
			# self.user = self._getUsername_fromPath()
			self.path     = path
		if path:
		# // When input path
		self.env = getEnv()

		self._configureFilePath_ = self.env.data_dirPath() + '/configure.json'
		self.configureData = self.get_ConfigureData() 

		self.user = self.getUsername()
		self.projectPath = self.configureData['setting']['project_path']
		self.projectName = os.path.basename( self.projectPath )
		self.projectCode = self.configureData['setting']['project_code']

		self.productionPath = self.projectPath + '/production'
		self.assetPath	= self.productionPath + '/assets' 
		self.filmPath	= self.productionPath + '/film' 

		# // Will set in function 'set_projectConfigFilePath'
		self.projectConfigFilePath = ''

		# self.type = self.isType()
		self.asset 	= 'assets'
		self.shot 	= 'shot'

		self.splitPath_data = self.splitPath()

	def getUsername(self):
		'''
			setup username
			> Query computername to compare with config file
		'''

		# // Get computername
		computerName = socket.gethostname()

		# // compare with configuration file
		if computerName in self.configureData['username'].keys():
			username = self.configureData['username'][computerName]

		# // if not math any name.
		else :
			username = 'Guest'
		
		return username

	def _getUsername_fromPath(self):
		""" """
		path = self.filename
		username = path.split('_')[-1].split('.')[0]
		return username

	def splitPath (self):
		data = self.path.replace( self.projectPath+'/', '' ).split('/')

		return data

	def get_ConfigureData(self):
		''' read and get Json data from './configure.json' '''
		data = json.load( open(self._configureFilePath_,'r') )
		return data

	def get_projectConfigData(self):
		data = json.load( open(self._configureFilePath_,'r') )

	def set_projectConfigFilePath(self, projectPath):
		''' 
			set Project config file path ...

			@projectPath : path of current project
			return : path of project config file
		'''
		
		filename = 'config.con'
		filepath = projectPath + '/' + filename
		
		if not os.path.exists( projectPath ):
			print ('Project config file not found.')
			return

		self.projectConfigFilePath = filepath
		return filepath

	def get_ProjectPath(self):
		return self.projectPath

	def get_ProjectName(self):
		return self.projectName

	def get_projectCode(self):
		return self.projectCode

	def get_path(self):
		''' 
			Return full path of file
		'''
		return self.path

	def get_workspace(self):
		'''
			return working folder that constrain workspace.mel
		'''
		path = '/'.join( self.path.split('/')[:-3] )

		return path

	def isType(self):
		'''
			return type of scene : assets / shot
		'''

		myType = self.path.replace( self.projectPath+'/', '' ).split('/')[1]

		if myType == 'film':
			myType = 'shot'

		self.type = myType
		return myType

	def get_fileName(self, ext=True):
		'''
			return : ppl_sq10_sh100_lighting_v003_nook.ma
		'''

		if not ext :
			base = os.path.basename( self.filename )
			filename = os.path.splitext( base )[0]
			return filename
		else:
			return self.filename

	def get_task(self):
		task = self.splitPath_data[-2]
		return task

	def get_version(self):
		version = self.filename.split('_')[-2]
		version = int ( version.replace('v','') )
		return version

	def get_lastFileVersion(self):
		''' description '''
		if self.type == self.shot:
			path = '%s/%s/%s/%s/%s/%s/%s'%(	self.projectPath 	, 
											'production'		, 
											'film'				, 
											self.get_sequence()	, 
											self.get_shot()		, 
											'scenes'			, 
											self.get_task() 
											)

			allfile = [ file for file in os.listdir( path ) if os.path.isfile( path +'/' + file ) ]
			return allfile[-1]

		elif self.type == self.asset:
			pass

		else:
			cmds.error('Type not match : ' + self.type)

	def get_nextVersion(self, filename=False):

		lastfilename = self.get_lastFileVersion()
		version = lastfilename.split('_')[-2]
		version = int ( version.replace('v','') )
		result 	=  version + 1

		if filename :
			version = 'v%03d'%(result)
			result = '_'.join( [ self.projectCode, self.get_sequence(), self.get_shot(), self.get_task(), version, self.get_user()+'.ma' ] )

		return result

	def get_user(self):
		user = self.user
		return user
		
	def get_name(self):
		'''
			return name of asset / shot
		'''

		sub_path = self.splitPath_data

		if self.type == self.asset :
			name = sub_path[3]

		elif self.type == self.shot :
			name = sub_path[3]

		else:
			cmds.error('type not found : ' + self.type)

		return name

	def get_sequence(self):
		'''
			return : sq10
		'''
		if self.type == self.shot:
			return self.splitPath_data[2]

		else:
			cmds.warning('type is not shot : ' + self.type)
			return False

	def get_shot(self):
		'''
			return : sh100
		'''
		if self.type == self.shot:
			return self.splitPath_data[3]

		else:
			cmds.warning('type is not shot : ' + self.type)
			return False

	def getThumbnail(self, workspace, filename, perfile=False):
		""" description """

		# thumbnail_path = self.get_ProjectPath() + '/thumbnail_miss.jpg'
		# return thumbnail_path

		thumbnail_path = '%s/%s'%(workspace, '_thumbnail')

		# // check _thumbnail path exists
		if not os.path.exists(thumbnail_path):
			# print (thumbnail_path + ' : not exists')
			thumbnail_path = self.get_ProjectPath() + '/thumbnail_miss.jpg'
			return thumbnail_path

		# // check number of image file
		all_thumbnail_files = os.listdir( '%s/%s'%( workspace, '_thumbnail') )
		if all_thumbnail_files == []:
			# print ( 'not have thumbnail file : ' + str(all_thumbnail_files))
			thumbnail_path = self.get_ProjectPath() + '/thumbnail_miss.jpg'
			return thumbnail_path

		else:
			if perfile:
				if os.path.exists(thumbnail_path+'/'+filename):
					thumbnail_path = thumbnail_path+'/'+filename
				else:
					thumbnail_path = self.get_ProjectPath() + '/thumbnail_miss.jpg'
					return thumbnail_path
			else:
				thumbnail_file = sorted( all_thumbnail_files )[-1] 
				thumbnail_path += '/%s'%(thumbnail_file)

		# print ('>> : ' + thumbnail_path)
		if not os.path.exists( thumbnail_path ) :
			print (thumbnail_path + ' : not exists')
			thumbnail_path = self.get_ProjectPath() + '/thumbnail_miss.jpg'

		return thumbnail_path


def showEnvVar():
	'''
		Print all var
	'''

	myEnv = getEnv()
	myInfo = getInfo()

	print('========== getInfo ==========')

	print('get_workspace : ' + str(myInfo.get_workspace()))

	# [u'production', u'film', u'sq10', u'sh100', u'scenes', u'lighting', u'ppl_sq10_sh100_lighting_v003_nook.ma']
	print ('splitPath : ' + str(myInfo.splitPath()))

	# D:/WORK/Pipeline_projectSetup
	print ('get_ProjectPath : ' + str(myInfo.get_ProjectPath()))

	# Pipeline_projectSetup
	print ('get_ProjectName : ' + str(myInfo.get_ProjectName()))

	# ppl
	print ('get_projectCode : ' + str(myInfo.get_projectCode()))

	# shot
	print ('isType : ' + str(myInfo.isType()))

	# sh100
	print ('get_name : ' + str(myInfo.get_name()))

	# sq10
	print ('get_sequence : ' + str(myInfo.get_sequence()))

	# sh100
	print ('get_shot : ' + str(myInfo.get_shot()))

	# ppl_sq10_sh100_lighting_v003_nook.ma
	print ('get_fileName : ' + str(myInfo.get_fileName()))

	# ppl_sq10_sh100_lighting_v003_nook
	print ('get_fileName(ext=False) : ' + str(myInfo.get_fileName(ext=False)))

	# lighting
	print ('get_task : ' + str(myInfo.get_task()))

	# 3 : int
	print ('get_version : ' + str(myInfo.get_version()))

	# 4 : int
	print ('get_nextVersion : ' + str(myInfo.get_nextVersion()))

	# ppl_sq10_sh100_lighting_v004_nook.ma
	print ('get_nextVersion(filename =True) : ' + str(myInfo.get_nextVersion(filename =True)))

	# ppl_sq10_sh100_lighting_v003_nook.ma
	print ('get_lastFileVersion : ' + str(myInfo.get_lastFileVersion()))


if __name__ == '__main__':
	modulePath = 'P:/_studioTool/sal_pipeline'

	app = getEnv()
	print modulePath


	app = getInfo()

	showEnvVar()

	# app.showEnvVar()

# # [u'production', u'film', u'sq10', u'sh100', u'scenes', u'lighting', u'ppl_sq10_sh100_lighting_v003_nook.ma']
# print app.splitPath()

# # D:/WORK/Pipeline_projectSetup
# print app.get_ProjectPath()

# # Pipeline_projectSetup
# print app.get_ProjectName()

# # ppl
# print app.get_projectCode()

# # shot
# print app.isType()

# # sh100
# print app.get_name()

# # sq10
# print app.get_sequence()

# # sh100
# print app.get_shot()

# # ppl_sq10_sh100_lighting_v003_nook.ma
# print app.get_fileName()

# # ppl_sq10_sh100_lighting_v003_nook
# print app.get_fileName(ext=False)

# # lighting
# print app.get_task()

# # 3 : int
# print app.get_version()

# # 4 : int
# print app.get_nextVersion()

# # ppl_sq10_sh100_lighting_v004_nook.ma
# print app.get_nextVersion(filename =True)

# # ppl_sq10_sh100_lighting_v003_nook.ma
# print app.get_lastFileVersion()





# D:/WORK/Pipeline_projectSetup
# Pipeline_projectSetup
# ppl