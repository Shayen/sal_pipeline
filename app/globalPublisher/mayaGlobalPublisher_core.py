import maya.cmds as cmds

import sys, os, shutil, logging, json, time, traceback

from sal_pipeline.src import env
from sal_pipeline.src import utils
import mayaGlobalPublisher_util as pubUtil
# reload(pubUtil)
# reload(utils)
# reload(env)

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

MAYAPY_PATH = os.environ["MAYA_LOCATION"] + "/bin/mayapy.exe"

class mayaGlobalPublisher_core(object):

	def __init__(self):
		pass

	def saveIncrement(self, comment = ''):
		filename 		= cmds.file(q=True,sn=True, shn=True)
		new_fileName 	= myInfo.get_nextVersion(filename = True )
		currentPath 	= os.path.dirname( cmds.file(q=True, sn=True) )

		result = "None"

		# save increment
		new_filePath = '%s/%s'%( currentPath, new_fileName )
		cmds.file( rename=new_filePath )
		result =  cmds.file( save=True, type='mayaAscii' )

		# set Thumbnail +
		myInfo.filename = cmds.file( q=True, sn=True, shn=True )
		workspace 			= self._get_workSpace()
		thumbnail_path 		= workspace + '/_thumbnail'
		thumbnail_filename 	= myInfo.get_fileName(ext = False) + '.jpg'

		shutil.copy2(self._pubThumbnail_Path, '/'.join([thumbnail_path,thumbnail_filename]))
		print( "# Capture thumbnail : %s"%(   '/'.join([thumbnail_path,thumbnail_filename])) )
		
		if comment == '' :
			comment = 'Publish and save increment.'

		# save comment
		if comment != '' :
			try :

				comment = '[Publish] ' + comment

				saveComment( filename = new_filePath, comment = comment )
				logger.info("Save comment : " + comment)
			except Exception as e :
				logger.error("Cannot save comment : " + str(e))
				traceback.print_exc()

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
		command_file= myEnv.src_dirPath() + '/createHeroFile.py'
		fileName 	= cmds.file(q=True,sn=True)
		output_file = destination_path

		# Export selection "Geo_Grp"
		if not cmds.objExists("Geo_grp") and not cmds.objExists("Set_grp") :
			logger.error("Cannot create hero file : No Geo_grp or Set_Grp.")
			return False

		cmds.select("Geo_grp")
		# cmds.select("Set_grp")
		cmds.file(output_file, type='mayaAscii', exportSelected = True, f=True )
		cmds.select(cl=True)
		
		command = "{program} {command_file} {workspace} {fileName} {output_path}".format(	
																				program 	= MAYAPY_PATH,
																				command_file= command_file,
																				workspace 	= self._get_workSpace(),
																				fileName	= output_file,
																				output_path	= output_file)

		out, err, exitcode = pubUtil.subprocess_call(command)
		if str(exitcode) != '0':
			logger.error(err)
			print 'error opening file: %s' % (output_file)
		else:
			# print 'added new layer %s to %s' % (out, output_file)
			logger.info("Create Hero file : " + output_file)

		return destination_path

	def _get_workSpace(self):
		'''return workspace'''
		filePath = cmds.file(q=True, sn=True)
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
			    "model": [
				    {
				        "filename": "",
				        "publisher": "",
				        "date": "",
				        "comment": "",
				        "cache": []
				    },
				    {
				    	"filename": "",
				        "publisher": "",
				        "date": "",
				        "comment": "",
				        "cache": []
				    }
			    ],
			    "texture": [{
			        "filename": "",
			        "publisher": "",
			        "date": "",
			        "comment": "",
			        "cache": []
			    }]
			}
		'''
		
		# Check file exists
		pubdata_file = self._get_workSpace() + '/scenes/pub/pubdata.json'

		if not os.path.exists(os.path.dirname(pubdata_file)):
			os.mkdir(os.path.dirname(pubdata_file))
			logger.info ("Create folder : " + os.path.dirname(pubdata_file) )

		if not os.path.exists(pubdata_file) :
			f = open(pubdata_file, 'w')
			f.write("{}")
			f.close()

		f = open(pubdata_file, 'r')
		data = {}
		if os.path.exists( pubdata_file ):
			# Load Json data
			try:
				read_data = f.read()
				data = json.loads(read_data)
			except ValueError as e:
				logger.exception(str(e))
				data = {}
		f.close()

		# Check {task} exists ?
		if not data.has_key(task):
			# Define data[task] as list
			data[task] = []
		else :
			# Change data type
			if type(data[task]) == dict():
				tmp_data 	= data[task]
				data[task] 	= [tmp_data]

		# Modify data [Create / Update]
		pub_data = {}
		pub_data['filename']	= filename
		pub_data['publisher']	= user
		pub_data['date']		= date
		pub_data['comment']		= comment
		pub_data['cache']		= cache

		data[task].append(pub_data)

		f = open(pubdata_file, 'w')
		json.dump(data, f, indent = 2)
		f.close()

	def export_GPUCache(self):
		'''Export gpu cache'''
		# Export gpu cache

		if myInfo.get_task() == 'model' :
			dest 		= self._get_workSpace() + '/scenes/pub'
			filename 	= myInfo.get_name() + "_gpu"
			result 		= pubUtil.exportGpuCache("Geo_grp", dest, filename)

			logger.info ("Export cache : " + result)

		return ('/'.join([dest, filename]))

	def export_objBBox(self):
		'''Export object boundingbox'''
		# Export bounding box
		if myInfo.get_task() == 'model' :

			command_file= myEnv.src_dirPath() + '/createBoundingBox.py'
			assetName 	= myInfo.get_name()
			dest 		= self._get_workSpace() + '/scenes/pub/'
			fileName 	= cmds.file(q=True,sn=True)
			output_file = dest +assetName + '_bbox.ma'
			
			command = "{program} {command_file} {workspace} {fileName} {assetName} {output_path}".format(	
																					program 	= MAYAPY_PATH,
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
				logger.info("Create BoundingBox : " + output_file)
				return True
			
			return output_file

	def export_sceneAssembly(self):
		'''Create scene Assembly'''
		# Create scene Assembly
		command_file= myEnv.src_dirPath() + '/createMayaSceneAssembly.py'
		workspace 	= self._get_workSpace()
		pub_filepath= self._getHeroFile_path()
		output_file = self._get_workSpace() + '/scenes/pub/%s_AD.ma'%(myInfo.get_name())
		command = "{program} {command_file} {workspace} {assetName} {pub_filepath} {output_path}".format(	program 	= MAYAPY_PATH,
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
			logger.info ("Create scene assembly : " + pub_filepath)
			return True

		return output_file

	def export_RSProxy(self):
		''' 
		Create redshift proxy data 

		rsProxy 
			-fp "C:/Users/siras/Desktop/sphere_test.rs" 
			-sl;
		'''

		dest 		= self._get_workSpace() + '/scenes/pub'
		rsfilename 	= myInfo.get_name() + "_rs.rs"
		result 		= pubUtil.exportRSProxy("Geo_grp", dest, rsfilename)

		logger.info ("Export Rs proxy : " + result)

		# (workspace,fileName,assetName,output_path)
		command_file= myEnv.src_dirPath() + '/createRedshiftProxy.py'
		workspace 	= self._get_workSpace()
		pub_filepath= self._getHeroFile_path()
		output_file = self._get_workSpace() + '/scenes/pub/%s_rsProxy.ma'%(myInfo.get_name())
		command     = "{program} {command_file} {workspace} {fileName} {assetName} {output_path}".format(program = MAYAPY_PATH,
																									command_file= command_file,
																									workspace	= workspace,
																									fileName 	= pub_filepath,
																									assetName	= myInfo.get_name(),
																									output_path	= output_file)
		out, err, exitcode = pubUtil.subprocess_call(command)
		if str(exitcode) != '0':
			logger.error(err)
			print 'error opening file: %s' % (output_file)
		else:
			# print 'added new layer %s to %s' % (out, output_file)
			logger.info (out)
			return True

		return output_file

	
def saveComment(filename, comment):
	''' Save comment data to data.json file '''

	info  = env.getInfo(path=filename)
	filename  = info.get_fileName() 
	workspace = info.get_workspace()
	task = info.get_task()
	name  = info.get_name()

	dataFile = workspace + "/data.json"

	# Create file
	if not os.path.exists(dataFile):

		data = {task: {filename : comment}}
		f = open(dataFile, 'w')
		f.write(json.dumps( data, indent = 4 ))
		f.close()

	# Update data
	else :
		try :
			f = open(dataFile,'r')
			raw_data = json.loads(f.read())
			f.close()
		except :
			raw_data = {}

		if not raw_data.has_key(task):
			raw_data[task] = {}

		raw_data[task][filename] = comment

		# Write file
		f = open(dataFile, 'w')
		f.write(json.dumps( raw_data, indent = 4 )) 
		f.close()

	return True

if __name__ == '__main__':
	app =mayaGlobalPublisher_core()
