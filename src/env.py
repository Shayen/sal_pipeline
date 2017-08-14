import os, sys, json

modulePath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-1] )

class getEnv(object):

	def __init__(self):
		self._modulePath_ = modulePath
		self.shotTemplateFileName = 'shot_template.zip'
		self.projectTemplateFileName = 'projectSetup_template.zip'

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

class getInfo(object):

	def __init__(self):
		self.env = getEnv()

		self._configureFilePath_ = self.env.data_dirPath() + '/configure.json'
		self.configureData = self.get_ConfigureData() 

		self.user = self.configureData['setting']['username']
		self.projectPath = self.configureData['setting']['project_path']
		self.projectName = os.path.basename( self.projectPath )
		self.projectCode = self.configureData['setting']['project_code']

		self.productionPath = self.projectPath + '/production'
		self.assetPath	= self.productionPath + '/assets' 
		self.filmPath	= self.productionPath + '/film' 

		# Set with sunction 'set_projectConfigFilePath'
		self.projectConfigFilePath = ''

		self.asset 	= 'assets'
		self.shot 	= 'shot'

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


	def get_projectCode(self):
		pass


if __name__ == '__main__':
	# app = getEnv()
	# print app.modulePath()

	app = getInfo()
	print app.projectName