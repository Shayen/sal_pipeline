import sys, os

from sal_pipeline.src import env
reload(env)
env = env.getEnv()

# modulePath = '/'.join( os.path.dirname( os.path.abspath(__file__) ).split('\\')[:-1] )
modulePath = env.modulePath()

if modulePath not in sys.path :
	sys.path.append( modulePath )

def app_projectExplorer():
	''' run project explorer '''
	env.checkEnv()

	from sal_pipeline.app import projectExplorer
	reload(projectExplorer)
	projectExplorer.run()

def app_mayaGlobalPublisher():
	''' run project explorer '''
	env.checkEnv()

	from sal_pipeline.app import globalPublisher
	reload(globalPublisher)
	globalPublisher.run()

def app_assetImporter():
	from sal_pipeline.app import assetImporter
	reload(assetImporter)
	assetImporter.run()

def app_redshiftMultiMatte():
	from sal_pipeline.app.RS_MultimatteTool import rsMM_app
	reload(rsMM_app)

def app_FileTextureManager():
	import maya.mel as mel

	app_path = env.app_dirPath() + '/FileTextureManager.mel'
	print app_path
	mel.eval("source \"{0}\";".format(app_path))
	mel.eval("FileTextureManager;")

def app_mergePlace2TextureNode():
	from sal_pipeline.app import merge_place2DTexture
	reload(merge_place2DTexture)
	merge_place2DTexture.main()

def app_replaceReference():
	from sal_pipeline.app import massRefReplace_app
	reload(massRefReplace_app)
	app = massRefReplace_app.massRefRlps_UI()
	app.showUI()

def app_renderLayerManager():
	from sal_pipeline.app import RenderlayerManager_app
	reload(RenderlayerManager_app)
	app = RenderlayerManager_app.renderLayerMan_UI()
	app.showUI()

if __name__ == '__main__':
	app_projectExplorer()
