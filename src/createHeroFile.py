# Maya Standalone

import os, sys, traceback, time

import maya.standalone
import maya.cmds as cmds
import maya.mel  as mel
maya.standalone.initialize(name='python')  

def export_objBBox( workspace, fileName, output_path ):
	# Start Maya in batch mode

	print ("\n") # New line
	print ("_"*32)
	print ("Building Hero file...")

	if not isFileExists(fileName):
		print ("file not found : " + fileName )
		time.sleep(10)
		return

	# Create hero file.
	try :
		# open file
		cmds.file(fileName, o=True, f=True)
		mel.eval( 'setProject "'+ workspace +'";')
		
		# import reference
		import_refObject()

		# Save File
		cmds.file( rename = output_path )
		cmds.file( save=True, type='mayaAscii' )

	except Exception as e :
		print(e)
		traceback.print_exc()
		time.sleep(10)

	print ("\nCreate Hero file - success : " + output_path )
	# time.sleep(0.5)

	uninitialize_maya()

	return True

def uninitialize_maya():
	# Starting Maya 2016, we have to call uninitialize to properly shutdown
	if float(cmds.about(v=True)) >= 2016.0:
		maya.standalone.uninitialize()

def import_refObject():
	refs = cmds.ls(type='reference')
	for i in refs:

		if i == "sharedReferenceNode":
			logger.warning ("skip : " + i)
			continue

		rFile = cmds.referenceQuery(i, f=True)
		cmds.file(rFile, importReference=True)

		print ("\nImport object : " + i )

def isFileExists(filePath) :
	return os.path.exists(filePath)

if __name__ == '__main__':

	workspace   = sys.argv[1]
	fileName 	= sys.argv[2]
	output_path = sys.argv[3]
	export_objBBox(workspace,fileName,output_path)