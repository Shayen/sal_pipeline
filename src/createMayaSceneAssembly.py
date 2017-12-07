# Maya Standalone

import os, sys, traceback, time

import maya.standalone
import maya.cmds as cmds
import maya.mel  as mel
maya.standalone.initialize(name='python')  

def create_sceneAssembly( workspace, assetName, pub_filepath, output_path ):
	# Start Maya in batch mode

	loadSceneAssemblyPlugin()

	pub_filepath = pub_filepath.replace(workspace, '')
	gpu_filepath = "scenes/pub/%s_gpu.abc"%(assetName)
	box_filepath = "scenes/pub/%s_bbox.ma"%(assetName)
	
	try :
		cmds.file(f=True, new=True)

		mel.eval( 'setProject "'+ workspace +'";')


		# create Assembly Definition
		assembly_name = cmds.assembly(name = assetName+"_AD" )


		# Create Locator representation
		cmds.assembly(	assembly_name, 
						edit=True, 
						createRepresentation='Locator',
				  		repName="myLocator", 
				  		input = assetName)


		# Create GPU representation
		if isFileExists( os.path.join(workspace,gpu_filepath) ):
			
			cmds.assembly(	assembly_name , 
							edit	= True   , 
							createRepresentation='Cache',
							repName	= "Gpu"  , 
							repLabel= "GPU", 
							input	= gpu_filepath)

		# Create BBox representation
		if isFileExists( os.path.join(workspace,box_filepath) ):
		
			cmds.assembly(	assembly_name , 
							edit	= True   , 
							createRepresentation='Scene',
							repName	= "BBox"  , 
							repLabel= "BBOX", 
							input	= box_filepath)

		# Create Render representation
		if isFileExists( os.path.join(workspace,pub_filepath) ):
		
			cmds.assembly(	assembly_name , 
							edit	= True   , 
							createRepresentation='Scene',
							repName	= "Render"  , 
							repLabel= "Render_md", 
							input	= pub_filepath )

		# Save the file    
		cmds.file( rename = output_path )
		result =  cmds.file( save=True, type='mayaAscii' )


		uninitialize_maya()

	except Exception as e :
		print(e)
		traceback.print_exc()
		time.sleep(10)

	print ("Create scene assembly success : " + output_path )
	time.sleep(0.5)

def uninitialize_maya():
	# Starting Maya 2016, we have to call uninitialize to properly shutdown
	if float(cmds.about(v=True)) >= 2016.0:
		maya.standalone.uninitialize()

def loadSceneAssemblyPlugin():
	'''
	Load AbcExport plugin
	'''
	# Load AbcExport plugin
	if not cmds.pluginInfo('sceneAssembly',q=True,l=True):
		try:
			cmds.loadPlugin('sceneAssembly', quiet=True)
		except:
			raise Exception('Error loading sceneAssembly plugin!')
			time.sleep(10)

def isFileExists(filePath) :
	return os.path.exists(filePath)

if __name__ == '__main__':

	workspace   = sys.argv[1]
	assetName	= sys.argv[2]
	pub_filepath= sys.argv[3]
	output_path = sys.argv[4]
	create_sceneAssembly(workspace,assetName,pub_filepath,output_path)