# core.py
#  contain core function

import sys, os, json, subprocess
import nuke

from sal_pipeline.src import env
info   = env.nuke_info()
getEnv = env.getEnv()

configFileName = 'SAL_config.json'
configFilePath = os.path.join(os.environ['USERPROFILE'],'.nuke',configFileName)

def listAllProject():
	data = getEnv.globalConfig_data
	return data['setting']['projects'].keys()
	# getInfo = env.getInfo(projectName = "Vision")

def listAllSequence(nukeScriptsPath):
	allShot = []

	# nuke.tprint(nukeScriptsPath)

	for dirName in [ item for item in os.listdir(nukeScriptsPath) \
	if os.path.isdir(nukeScriptsPath + '/' + item) == True and not item.startswith("_")]:

		seq = dirName.split('_')[0]
		if seq not in allShot :
			allShot.append(seq)

	# if find nothing return folder is empty
	if not allShot :
		allShot = '-- Empty --'

	return allShot

def listAllShot(nukeScriptsPath,currentSeq):
	allShot = []

	for dirName in [ item for item in os.listdir(nukeScriptsPath) \
	if os.path.isdir(nukeScriptsPath + '/' + item) == True ]:

		seq = dirName.split('_')[0]
		if seq == currentSeq :
			allShot.append(dirName.split('_')[1])

	# if find nothing return folder is empty
	if not allShot :
		allShot = '-- Empty --'

	return allShot

def listAllVersion(nukeScriptsPath, seq, shot):
	_shot_dirName = "{seq}_{shot}".format(seq = seq, shot = shot)
	_shot_dirPath = os.path.join(nukeScriptsPath, _shot_dirName) 

	return [item for item in os.listdir(_shot_dirPath) \
	if os.path.isfile(_shot_dirPath + '/' + item) and (item.endswith(".nk") or item.endswith(".nknc")) ]

def _readSetting():
	''' Read config file from "%USERPROFILE%/.nuke/SAL_config.json" '''

	#  if config file dir is not exists.
	if not os.path.exists( os.path.dirname(configFilePath) ):
		return False

	#  Create file and return bare dictionary data.
	if not os.path.exists(configFilePath) :
		f = open(configFilePath, 'w')
		json.dump( dict(), f)
		f.close()
		return dict()

	# Read config data
	f = open(configFilePath, 'r')
	data = f.read()
	f.close()

	return json.loads(data)

def _writeSetting(data):
	''' write config data to "%USERPROFILE%/.nuke/SAL_config.json" '''

	#  if config file dir is not exists.
	if not os.path.exists( os.path.dirname(configFilePath) ):
		return False

	#  Create file and return bare dictionary data.
	if not os.path.exists(configFilePath) :
		f = open(configFilePath, 'w')
		json.dumps( dict(), f)
		f.close()
		return dict()

	# write data
	f = open(configFilePath, 'w')
	f.write(json.dumps( data, indent = 4))
	f.close()

	return data

def get_recentWorkingProject():
	''' Read last working project from config file'''
	configData = _readSetting()

	# if not have config data, SKIP
	if not configData :
		return False

	# Get recent project data.
	if configData.has_key('recentProject'):
		return configData['recentProject']
	
	# if not have recent project data, SKIP
	else :
		return False

def get_recentWorkingSequence():
	''' Read last working sequence from config file'''
	configData = _readSetting()

	# if not have config data, SKIP
	if not configData :
		return False

	# Get recent sequence data.
	if configData.has_key('recentSequence'):
		return configData['recentSequence']
	
	# if not have recent sequence data, SKIP
	else :
		return False

def get_recentWorkingShot():
	''' Read last working shot from config file'''
	configData = _readSetting()

	# if not have config data, SKIP
	if not configData :
		return False

	# Get recent shot data.
	if configData.has_key('recentShot'):
		return configData['recentShot']
	
	# if not have recent shot data, SKIP
	else :
		return False

def save_recentWorkingSpace(project,seq,shot):
	''' Write last working sequence to config file'''
	configData = _readSetting()

	# update data
	configData['recentSequence'] = seq
	configData['recentProject']  = project
	configData['recentShot']  	 = shot

	_writeSetting(configData)

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def objString(string):

	class objectString(object):
		def __init__(self, *args):
			self.text = args[0]

		def getString(self):
			return self.text

	data = objectString( string )
	return data

def getThumbnail( shotDirPath, filename = '', perfile=False):
	""" 
	Get nuke thumbnail 

	Note : If version is '', It will choose last version's thumbnail.
	"""

	thumbnail_path = '%s/%s'%(shotDirPath, '_thumbnail')
	missThumbnail_path  = getEnv.data_dirPath() + '/thumbnail_miss.jpg'

	# check _thumbnail path exists
	if not os.path.exists(thumbnail_path):
		return missThumbnail_path

	# if not have any image in Dir, Return : missThumbnail
	all_thumbnail_files = os.listdir( '%s/%s'%( shotDirPath, '_thumbnail') )
	if all_thumbnail_files == []:
		return missThumbnail_path

	else:
		# Get per version.
		if perfile:
			if os.path.exists(thumbnail_path+'/'+filename):
				thumbnail_path = thumbnail_path+'/'+filename
			else:
				print (thumbnail_path + ' : not exists')
				return missThumbnail_path
		# Get per shot [Return lasted version]
		else:
			thumbnail_file = sorted( all_thumbnail_files )[-1] 
			thumbnail_path += '/%s'%(thumbnail_file)

	return thumbnail_path

def saveFrame(thumbnailPath):
	viewer 		= nuke.activeViewer()
	inputNode 	= nuke.ViewerWindow.activeInput(viewer)
	viewNode 	= nuke.activeViewer().node()
	filetype 	= 'png'

	try:

		if inputNode != None:
			selInput = nuke.Node.input(viewNode, inputNode)
			
			if thumbnailPath != None:

				if not os.path.exists(os.path.dirname(thumbnailPath)):
					os.makedirs( os.path.dirname(thumbnailPath) )
				
				input_w = selInput.width()
				input_h = selInput.height()
				factor  = input_h / 448

				w = int(input_w / factor)
				h = int(input_h / factor)

				reformat= nuke.nodes.Reformat(format="%s %s" % (w, h), resize="width")
				reformat.setInput(0,selInput)
				write = nuke.nodes.Write(file = thumbnailPath, name = 'WriteSaveThisFrame', file_type=filetype)
				write.setInput(0,reformat)

				curFrame = int(nuke.knob("frame"))
				nuke.execute(write.name(), curFrame, curFrame)

				# Clear
				nuke.delete(write)
				nuke.delete(reformat)

				# Succcess
				# nuke.tprint("Save thumbnail : " + thumbnailPath)
				return thumbnailPath
		else:
			nuke.message("This viewer don't have any input connected!")

	except Exception as e:
		nuke.tprint(str(e))

if __name__ == '__main__':
	readSetting()