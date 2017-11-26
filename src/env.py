import os, sys, json, socket, shutil
import maya.mel as mel

modulePath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-1] )

class getEnv(object):

	def __init__(self):
		self._modulePath_ = modulePath
		self.shotTemplateFileName = 'shot_template.zip'
		self.projectTemplateFileName = 'projectSetup_template.zip'
		self.assetTemplateFileName = 'asset_template.zip'
		self.configureFileName = 'configure.json'

		self.globalConfig_data = self._read_globalConfig()
		self.user = self._get_Username()

	def modulePath(self):
		""" 
			return path of main module 

			return : "D:/WORK/Programming/sal_pipeline"
		"""
		path = self._modulePath_
		return path

	def checkEnv(self):
		''' checking environment '''
		is_envSet = False

		# get active project
		for project in self.globalConfig_data['setting']['projects'].keys():
			if self.globalConfig_data['setting']['projects'][project]['active'] == True:
				break

		project_path = self.globalConfig_data['setting']['projects'][project]["project_path"]
		if os.path.exists( project_path ):

			info = getInfo( projectName=project, path=project_path )
			if not os.path.exists(info.assetPath) or not os.path.exists(info.filmPath):
				raise IOError("asset path or film path not exists. please recheck.")
			else:
				is_envSet = True

		return is_envSet

	def ui_dirPath(self):
		return self._modulePath_ + '/ui'

	def src_dirPath(self):
		return self._modulePath_ + '/src'

	def data_dirPath(self):
		return self._modulePath_ + '/data'

	def log_dirPath(self):
		return self._modulePath_ + '/log'

	def app_dirPath(self):
		return self._modulePath_ + '/app'

	def shotTemplate_zipPath(self):
		return self.data_dirPath() + '/' + self.shotTemplateFileName

	def projectTemplate_zipPath(self):
		return self.data_dirPath() + '/' + self.projectTemplateFileName

	def assetTemplate_zipPath(self):
		return self.data_dirPath() + '/' + self.assetTemplateFileName

	def configure_filePath(self):
		return self.data_dirPath() + '/' + self.configureFileName

	def update_config(self, data):
		"""
			update config data to configure.json file 

			Var : @data : config data (json)
		"""
		
		try :
			# Dump data to config file
			json.dump( data , open( self.configure_filePath(), 'w') )

			# Replace Variable
			self.globalConfig_data = data

		except Exception as e:
			print(e)
		
	def _read_globalConfig(self):
		""" read config data from './configure.json' """
		try:
			data = json.load( open( self.configure_filePath(), 'r') )
			return data
		except IOError:
			#  configure_default.json
			src = self.data_dirPath() + '/configure_default.json'
			dst = self.data_dirPath() + '/configure.json'
			shutil.copy2(src, dst)

			if os.path.exists(dst):
				from app.globalPreference import Global_preference as global_pref
				
				app  = QApplication(sys.argv) 
				form = global_pref.sal_globalPreference()
				app.exec_()
			else:
				print ("Cannot open config file : " + dst )
				return {}

			raise("please restart tool.")

	def _get_Username(self):
		'''
			setup username
			> Query computername to compare with config file
		'''

		# // Get computername
		computerName = socket.gethostname()

		# // compare with configuration file
		if computerName in self.globalConfig_data['username'].keys():
			username = self.globalConfig_data['username'][computerName]

		# // if not math any name.
		else :
			username = 'Guest'
		
		return username

class getInfo(object):

	def __init__(self,projectName=None,path=None):
		import maya.cmds as cmds

		self.env = getEnv()

		self.globalConfigureData = self.env.globalConfig_data

		# // When input path
		if path:
			self.path     = path
			self.filename = path.split('/')[-1]
			# self.user = self._getUsername_fromPath()
		else:
			self.path 	  = cmds.file( q=True, sn=True )
			self.filename = cmds.file( q=True, sn=True, shn=True )
			# self.user = self.getUsername()

		# // when project name was set
		if projectName:
			self.projectName = projectName
		else :
			# split from file path
			self.projectName = self._get_projectNameFromPath()

		self.user = self.env.user
		
		self.projectPath = self.globalConfigureData['setting']['projects'][self.projectName]['project_path']
		self.projectCode = self.globalConfigureData['setting']['projects'][self.projectName]['project_code']

		self.productionPath = self.projectPath + '/production'
		self.assetPath	= self.productionPath + '/assets' 
		self.filmPath	= self.productionPath + '/film' 

		# // Will set in function 'set_projectConfigFilePath'
		self.projectConfigFilePath = ''

		# self.type = self.isType()
		self.asset 	= 'assets'
		self.shot 	= 'shot'

		self.splitPath_data = self.splitPath()

	def _get_projectNameFromPath(self):
		""" get full name of project"""

		filename 	= self.filename
		project_code= filename.split('_')[0]

		# get full project name from project code
		for projectName in self.globalConfigureData['setting']['projects'].keys():
			if self.globalConfigureData['setting']['projects'][projectName]['project_code'] == project_code:
				break 

		print ("Get project name from path : %s"%projectName)
		return projectName

	def getUsername(self):
		'''
			setup username
			> Query computername to compare with config file
		'''

		# // Get computername
		computerName = socket.gethostname()

		# // compare with configuration file
		if computerName in self.globalConfigureData['username'].keys():
			username = self.globalConfigureData['username'][computerName]

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
		# else : 
		# 	myType = 'assets'

		self.type = myType
		return myType

	def _getAssetType(self):
		''' get type of asset '''

		assetType = self.splitPath()[2]
		return assetType

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

	def get_pubName(self, ext=True):
		''' Generate publish name '''

		_splitData = self.get_fileName(ext=False).split("_")[:-3]
		_splitData.append( self.get_task() )
		_splitData.append( "pub.ma" )

		return '_'.join(_splitData)

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
			path = '%s/%s/%s/%s/%s/%s/%s'%(	self.projectPath 	, 
											'production'		, 
											'assets'			, 
											self._getAssetType(), 
											self.get_name()		, 
											'scenes'			, 
											self.get_task() 
											)
			print path

			allfile = [ file for file in os.listdir( path ) if os.path.isfile( path +'/' + file ) ]
			return allfile[-1]

		else:
			cmds.error('Type not match : ' + self.type)

	def get_nextVersion(self, filename=False):

		lastfilename = self.get_lastFileVersion()
		version = lastfilename.split('_')[-2]
		version = int ( version.replace('v','') )
		result 	=  version + 1

		if filename :
			version = 'v%03d'%(result)

			if self.type == self.shot:
				result = '_'.join( [ self.projectCode, self.get_sequence(), self.get_shot(), self.get_task(), version, self.get_user()+'.ma' ] )
			else :
				result = '_'.join( [ self.projectCode, self._getAssetType(), self.get_name(), self.get_task(), version, self.get_user()+'.ma' ] )

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
	myInfo = getInfo(projectName = "Vision", path = "P:/Vision/production/film/Anim/duo1Shot1Nal/scenes/anim/vis_Anim_duo1Shot1Nal_anim_v001_Dear.ma")

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
	modulePath = 'D:/WORK/Programming/sal_pipeline'

	# app = getEnv()
	# print os.listdir(modulePath+"/data")
	# configFile = modulePath+"/data/configure_test.json"
	# data = json.load( open(configFile,'r') )
	# print json.dumps(data,indent=2)

	showEnvVar()

	# app.showEnvVar()
# // test path : "P:/Vision/production/film/Anim/duo1Shot1Nal/scenes/anim/vis_Anim_duo1Shot1Nal_anim_v001_Dear.ma"

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
