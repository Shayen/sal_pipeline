# LOGGER
import os, datetime, logging, __main__

import env
reload(env)
env = env.getEnv()

modulePath = env.modulePath()

###### USAGE ######
# from sal_pipeline.src import log
# reload(log)

# logger = log.logger("test")
# logger = logger.getLogger()

# logger.info('Test message')

# ------------------------------

class logger():

	def __init__(self, name = "GLobal" ):

		self.logger = logging.getLogger(__main__.__name__)
		self._clearHandlers()
		self.logger.setLevel(logging.INFO)

		logFileName = str (datetime.date.today() )

		# create a file handler
		loggerPath = '{logDir}/{tool}/{logFileName}.log'.format(logDir = env.log_dirPath(), tool=name, logFileName = logFileName)
		self._checkLogFolder(name)
		handler = logging.FileHandler( loggerPath )
		handler.setLevel(logging.INFO)

		print loggerPath

		# create a logging format
		formatter = logging.Formatter('%(asctime)s - %(lineno)d - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)

		# add the handlers to the self.logger
		self.logger.addHandler(handler)

	def _clearHandlers(self):
		# DELETE EXISTSED HANDLER

		for each in self.logger.handlers[::-1] :
			if type(each).__name__ == 'StreamHandler':
				self.logger.removeHandler(each)

			if type(each).__name__ == 'NullHandler':
				self.logger.removeHandler(each)

			if type(each).__name__== 'FileHandler': 
				self.logger.removeHandler(each)
				each.flush()
				each.close()

	def _checkLogFolder(self, tool):
		''' Checking log folder '''

		logPath = env.log_dirPath()
		if not os.path.exists(logPath):
			os.mkdir(logPath)
			print ("Create directory : " + logPath)

		if not os.path.exists(logPath + '/' + tool) :
			os.mkdir(logPath + '/' + tool)
			print ("Create Directory : " + logPath + '/' + tool)


	def getLogger(self):
		return self.logger