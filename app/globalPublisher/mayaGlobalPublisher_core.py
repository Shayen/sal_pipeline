import maya.cmds as cmds

from sal_pipeline.src import env
from sal_pipeline.src import utils
reload(utils)
reload(env)

try:
	myInfo = env.getInfo()
	myInfo.get_task()
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
		pass

		return result

	def creat_HeroFile(self):
		''' save to Hero file '''
		# - Get hero path
		currentPath  = os.path.dirname( cmds.file(q=True, sn=True) )
		pub_fileName = myInfo.get_pubName(ext=True)
		destination_path = "{0}/{1}/{2}".format( os.path.dirname( currentPath ), 'pub', pub_fileName )

		# copy file  to destination
		shutil.copy2(src = cmds.file(q=True,sn=True), dst = destination_path)

		return destination_path

	def captureViewport(self):

		filePath = cmds.file(q=True, sn=True)
		if myInfo.isType() == 'shot':
			workspace = '/'.join( filePath.split('/')[:-2] )
		else :
			workspace = '/'.join( filePath.split('/')[:-3] )

		# generate unique filename
		pubThumbnail_Path 	= "{0}/_thumbnail".format(workspace)
		thumbnail_file		= "pub_temp"

		#capture
		_pubThumbnail_Path = utils.utils().captureViewport( outputdir = pubThumbnail_Path, filename = thumbnail_file )
		
		return _pubThumbnail_Path

	def export_pubData(self):
		''' save export metadata via JSON to pub directory '''
		pass

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