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
	print ("Building Bounding box...")

	if not isFileExists(fileName):
		print ("file not found : " + fileName )
		time.sleep(10)
		return

	try :
		cmds.file(fileName, o=True, f=True)

		mel.eval( 'setProject "'+ workspace +'";')

		# convert object to BBox
		# cmds.select("Geo_grp")
		assetName 	= assetName
		my_BBox		= create_BBox( obj="Geo_grp", name=assetName, nameSuffix="_BBox" )
		filename 	= assetName + '_bbox.ma'
		result 		= cmds.file( output_path, f=True, type='mayaAscii',exportSelected=True)

		# Export Object
		print ("\t-Export Bounding box : " + filename)

	except Exception as e :
		print(e)
		traceback.print_exc()
		time.sleep(10)

	print ("\nCreate BoundingBox success : " + output_path )
	time.sleep(0.5)

	uninitialize_maya()

	return True

def uninitialize_maya():
	# Starting Maya 2016, we have to call uninitialize to properly shutdown
	if float(cmds.about(v=True)) >= 2016.0:
		maya.standalone.uninitialize()

def create_BBox(obj,name,nameSuffix):
	x1, y1, z1, x2, y2, z2 = cmds.exactWorldBoundingBox(obj, calculateExactly=True)

	cube = cmds.polyCube()[0]
	cmds.move(x1, '%s.f[5]' % cube, x=True)
	cmds.move(y1, '%s.f[3]' % cube, y=True)
	cmds.move(z1, '%s.f[2]' % cube, z=True)
	cmds.move(x2, '%s.f[4]' % cube, x=True)
	cmds.move(y2, '%s.f[1]' % cube, y=True)
	cmds.move(z2, '%s.f[0]' % cube, z=True)

	return cmds.rename( name + nameSuffix )

def isFileExists(filePath) :
	return os.path.exists(filePath)

if __name__ == '__main__':

	workspace   = sys.argv[1]
	fileName 	= sys.argv[2]
	assetName	= sys.argv[3]
	output_path = sys.argv[4]
	export_objBBox(workspace,fileName,assetName,output_path)