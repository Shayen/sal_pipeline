# Maya Standalone

import os, sys, traceback, time

import maya.standalone
import maya.cmds as cmds
import maya.mel  as mel
maya.standalone.initialize(name='python')  

def export_objBBox( workspace, fileName, assetName, output_path ):
	# Start Maya in batch mode

	print ("\n") # New line
	print ("_"*32)
	print ("Building Redshift Proxy...")

	if not isFileExists(fileName):
		print ("file not found : " + fileName )
		time.sleep(10)
		return

	# Load redshift plugin
	loadRedshiftPlugin()

	try :
		# Open file
		cmds.file(fileName, o=True, f=True)

		# Set workspace
		mel.eval( 'setProject "'+ workspace +'";')

		# Create proxy placeHolder
		RSp_filepath = "scenes/pub/%s_rs.rs"%(assetName)
		rsProxyNodes = mel.eval("redshiftCreateProxy();")
		filePath	 = os.path.join(workspace,RSp_filepath)

		cmds.setAttr(rsProxyNodes[0] + ".fileName", filePath, type = "string")
		cmds.setAttr(rsProxyNodes[0] + ".displayMode", 1)
		cmds.setAttr(rsProxyNodes[0] + ".displayPercent", 10)

		filename 	= assetName + '_rsProxy.ma'
		result 		= cmds.file( output_path, f=True, type='mayaAscii',exportSelected=True)

		# Export Object
		print ("\t-Export Redshift Proxy : " + filename)

	except Exception as e :
		print(e)
		traceback.print_exc()
		time.sleep(10)

	print ("\nCreate Redshift Proxy success : " + output_path )
	time.sleep(0.5)

	uninitialize_maya()

	return True

def uninitialize_maya():
	# Starting Maya 2016, we have to call uninitialize to properly shutdown
	if float(cmds.about(v=True)) >= 2016.0:
		maya.standalone.uninitialize()

def loadRedshiftPlugin():
	'''
	Load Redshift plugin
	'''
	# Load gpuCache plugin
	if not cmds.pluginInfo('redshift4maya',q=True,l=True):
		try:
			cmds.loadPlugin('redshift4maya', quiet=True)
		except:
			raise Exception('Error loading redshift4maya plugin!')

def isFileExists(filePath) :
	return os.path.exists(filePath)

if __name__ == '__main__':

	workspace   = sys.argv[1]
	fileName 	= sys.argv[2]
	assetName	= sys.argv[3]
	output_path = sys.argv[4]
	export_objBBox(workspace,fileName,assetName,output_path)