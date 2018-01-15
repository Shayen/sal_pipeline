import maya.cmds as cmds

import sys, os, shutil, logging, json, time

from sal_pipeline.src import env
from sal_pipeline.src import utils
import mayaGlobalPublisher_util as pubUtil
reload(pubUtil)
reload(utils)
reload(env)

logger = logging.getLogger( __name__.split('.')[-1] )
logger.addHandler(logging.NullHandler())

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

		result = "None"

		# save increment
		cmds.file( rename='%s/%s'%( currentPath, new_fileName ) )
		result =  cmds.file( save=True, type='mayaAscii' )

		# set Thumbnail +
		myInfo.filename = cmds.file( q=True, sn=True, shn=True )
		workspace 			= self._get_workSpace()
		thumbnail_path 		= workspace + '/_thumbnail'
		thumbnail_filename 	= myInfo.get_fileName(ext = False) + '.jpg'

		shutil.copy2(self._pubThumbnail_Path, '/'.join([thumbnail_path,thumbnail_filename]))
		print( "# Capture thumbnail : %s"%(   '/'.join([thumbnail_path,thumbnail_filename])) )

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

		# Create HERO file
		mayapy_path = os.environ["MAYA_LOCATION"] + "/bin/mayapy.exe"
		command_file= myEnv.src_dirPath() + '/createHeroFile.py'
		fileName 	= cmds.file(q=True,sn=True)
		output_file = destination_path
		
		command = "{program} {command_file} {workspace} {fileName} {output_path}".format(	
																				program 	= mayapy_path,
																				command_file= command_file,
																				workspace 	= self._get_workSpace(),
																				fileName	= fileName,
																				output_path	= output_file)

		out, err, exitcode = pubUtil.subprocess_call(command)
		if str(exitcode) != '0':
			logger.error(err)
			print 'error opening file: %s' % (output_file)
		else:
			# print 'added new layer %s to %s' % (out, output_file)
			logger.info(out)

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

	def export_pubData(self, task, filename, user, date, comment, cache):
		''' 
		save export metadata via JSON to pub directory as "pubdata.json"

		Pattern :
			{
			    "model": {
			        "filename": "",
			        "publisher": "",
			        "date": "",
			        "comment": "",
			        "cache": []
			    },
			    "texture": {
			        "filename": "",
			        "publisher": "",
			        "date": "",
			        "comment": "",
			        "cache": []
			    }
			}
		'''
		
		# Check file exists
		pubdata_file = self._get_workSpace() + '/scenes/pub/pubdata.json'
		f = open(pubdata_file, 'w+')
		data = {}
		if os.path.exists( pubdata_file ):
			# Load Json data
			try:
				data = json.load(f)
			except ValueError :
				data = {}
			
		# Modify data [Create / Update]
		data['task'] = {}
		data['task']['filename']	= filename
		data['task']['publisher']	= user
		data['task']['date']		= date
		data['task']['comment']		= comment
		data['task']['cache']		= cache

		json.dump(data, f, indent = 2)

		f.close()

	def export_GPUCache(self):
		'''Export gpu cache'''
		# Export gpu cache

		if myInfo.get_task() == 'model' :
			dest 		= self._get_workSpace() + '/scenes/pub'
			filename 	= myInfo.get_name() + "_gpu"
			result 		= pubUtil.exportGpuCache("Geo_grp", dest, filename)

			print ("Export cache : " + result)

	def export_objBBox(self):
		'''Export object boundingbox'''
		# Export bounding box
		if myInfo.get_task() == 'model' :

			mayapy_path = os.environ["MAYA_LOCATION"] + "/bin/mayapy.exe"
			command_file= myEnv.src_dirPath() + '/createBoundingBox.py'
			assetName 	= myInfo.get_name()
			dest 		= self._get_workSpace() + '/scenes/pub/'
			fileName 	= cmds.file(q=True,sn=True)
			output_file = dest +assetName + '_bbox.ma'
			
			command = "{program} {command_file} {workspace} {fileName} {assetName} {output_path}".format(	
																					program 	= mayapy_path,
																					command_file= command_file,
																					workspace 	= self._get_workSpace(),
																					fileName	= fileName,
																					assetName	= myInfo.get_name(),
																					output_path	= output_file)
			# subprocess.call(command)
			# print ("Create BBox : " + output_file )

			out, err, exitcode = pubUtil.subprocess_call(command)
			if str(exitcode) != '0':
				logger.error(err)
				print 'error opening file: %s' % (output_file)
			else:
				# print 'added new layer %s to %s' % (out, output_file)
				logger.info(out)
				return True
			# return True

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
		# subprocess.call(command)

		out, err, exitcode = pubUtil.subprocess_call(command)
		if str(exitcode) != '0':
			logger.error(err)
			print 'error opening file: %s' % (output_file)
		else:
			# print 'added new layer %s to %s' % (out, output_file)
			logger.info (out)
			return True

if __name__ == '__main__':
	app =mayaGlobalPublisher_core()
