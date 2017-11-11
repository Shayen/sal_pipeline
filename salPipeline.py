import sys, os, logging

from sal_pipeline.src import env
reload(env)
env = env.getEnv()

# modulePath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-1] )
modulePath = env.modulePath()

if modulePath not in sys.path :
	sys.path.append( modulePath )

# from sal_pipeline.src import projectExplorer


##################### LOGGER #####################
# import datetime

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# logFileName = str (datetime.date.today() )

# # create a file handler
# handler = logging.FileHandler( modulePath + '/sal_pipeline/log/' + logFileName + '.log' )
# handler.setLevel(logging.INFO)

# # create a logging format
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# # add the handlers to the logger
# logger.addHandler(handler)

# logger.info('Hello baby')

#################################################

def app_projectExplorer():
	''' run project explorer '''
	env.checkEnv()

	from sal_pipeline.app import projectExplorer
	reload(projectExplorer)
	projectExplorer.run()

def app_assetImporter():
	# from sal_pipeline.app import assetImporter
	# reload(assetImporter)
	# assetImporter.run()
	pass

if __name__ == '__main__':
	app_projectExplorer()
