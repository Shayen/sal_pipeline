import maya.cmds as cmds

import sys, os, shutil, subprocess

from sal_pipeline.src import env
from sal_pipeline.src import utils
import mayaGlobalPublisher_util as pubUtil
reload(pubUtil)
reload(utils)
reload(env)

try:
	myInfo = env.getInfo()
	myInfo.get_task()

	myEnv = env.getEnv()

except IndexError :
	e_msg = "## This file is not in pipeline. please check your file. ##\n"
	print('_'*64)
	print(e_msg)

class mayaGlobalPublisher_core(object):

	def __init__(self):
		pass

	def saveIncrement(self):
		filename 		= cmds.file(q=True,sn=True, shn=True)
		new_fileName 	= myInfo.get_nextVersion(filename = True )
		currentPath 	= os.path.dirname( cmds.file(q=True, sn=True) )

		# save increment
		cmds.file( rename='%s/%s'%( currentPath, new_fileName ) )
		result =  cmds.file( save=True, type='mayaAscii' )

		# set Thumbnail +
		workspace 			= self._get_workSpace()
		thumbnail_path 		= workspace + '/_thumbnail'
		thumbnail_filename 	= myInfo.get_fileName(ext = False) + '.jpg'

		shutil.copy2(self._pubThumbnail_Path, '/'.join([thumbnail_path,thumbnail_filename]))
		print( "# Capture thumbnail : %s"%( thumbnail_filename) )

		return result

	def _getHeroFile_path(self):
		currentPath  = os.path.dirname( cmds.file(q=True, sn=True) )
		pub_fileName = myInfo.get_pubName(ext=True)
		destination_path = "{0}/{1}/{2}".format( os.path.dirname( currentPath ), 'pub', pub_fileName )
		
		return destination_path

	def creat_HeroFile(self):
		''' save to Hero file '''
		# - Get hero path
		destination_path = self._getHeroFile_path()
		# copy file  to destination
		shutil.copy2(src = cmds.file(q=True,sn=True), dst = destination_path)

		return destination_path

	def _get_workSpace(self):
		'''return workspace'''
		filePath = cmds.file(q=True, sn=True)
		if myInfo.isType() == 'shot':
			workspace = '/'.join( filePath.split('/')[:-2] )
		else :
			workspace = '/'.join( filePath.split('/')[:-3] )

		return workspace

	def captureViewport(self):

		workspace = self._get_workSpace()

		# generate unique filename
		pubThumbnail_Path 	= "{0}/_thumbnail".format(workspace)
		thumbnail_file		= "pub_temp"

		#capture
		self._pubThumbnail_Path = utils.utils().captureViewport( outputdir = pubThumbnail_Path, filename = thumbnail_file )
		
		return self._pubThumbnail_Path

	def export_pubData(self):
		''' save export metadata via JSON to pub directory '''
		pass

	def export_GPUCache(self):
		'''Export gpu cache'''
		# Export gpu cache

		if myInfo.get_task() == 'model' :
			dest 		= self._get_workSpace() + '/scenes/pub'
			filename 	= myInfo.get_name() + "_gpu"
			result = pubUtil.exportGpuCache("Geo_grp", dest, filename)

			print ("Export cache : " + result)

	def export_objBBox(self):
		'''Export object boundingbox'''
		# Export bounding box
		if myInfo.get_task() == 'model' :
			#Duplicate Object
			myOBJ = cmds.duplicate("Geo_grp")

			cmds.select(myOBJ[0])
			assetName 	= myInfo.get_name()
			my_BBox 	= cmds.geomToBBox( name = assetName, nameSuffix="_BBox", single=True )
			dest 		= self._get_workSpace() + '/scenes/pub/'
			filename 	= assetName + '_bbox.ma'
			result = cmds.file( dest + filename, type='mayaAscii',exportSelected=True)

			# Delete Object
			cmds.delete( my_BBox[0].split(":")[1] )
			print ("Export Bounding box : " + filename)
			return True

	def export_sceneAssembly(self):
		'''Create scene Assembly'''
		# Create scene Assembly
		mayapy_path = os.environ["MAYA_LOCATION"] + "/bin/mayapy.exe"
		command_file= myEnv.src_dirPath() + '/createMayaSceneAssembly.py'
		workspace 	= self._get_workSpace()
		pub_filepath= self._getHeroFile_path()
		output_file = self._get_workSpace() + '/scenes/pub/%s_AD.ma'%(myInfo.get_name())
		command = "{program} {command_file} {workspace} {assetName} {pub_filepath} {output_path}".format(	program 	= mayapy_path,
																				command_file= command_file,
																				workspace	= workspace,
																				assetName	= myInfo.get_name(),
																				pub_filepath= pub_filepath,
																				output_path	= output_file)
		subprocess.call(command)
		
		print ("Create Assembly : " + output_file )

	def post_toFacebook(self,data = {}):
		''' post update to facebook group '''

		from sal_pipeline.src import facepy
		# repo : https://github.com/jgorset/facepy

		#
		#
		result = {}

		return result

if __name__ == '__main__':
	app =mayaGlobalPublisher_core()
	app.post_toFacebook()