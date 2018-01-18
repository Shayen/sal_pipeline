# core.py
#  contain core function

import sys, os
import nuke

from sal_pipeline.src import env
reload(env)
info = env.nuke_info()

def listAllProject():
	data = getEnv.globalConfig_data
	return data['setting']['projects'].keys()
	# getInfo = env.getInfo(projectName = "Vision")

def listAllSequence():
	allShot = []

	nuke.tprint(getInfo.nukeScriptsPath)

	for dirName in [ item for item in os.listdir(getInfo.nukeScriptsPath) if os.path.isdir(getInfo.nukeScriptsPath + '/' + item) == True ]:
		seq = dirName.split('_')[0]
		if seq not in allShot :
			allShot.append(seq)

	# if find nothing return folder is empty
	if not allShot :
		allShot = '-- Empty --'

	return allShot

def listAllShot(currentSeq):
	allShot = []

	for dirName in [ item for item in os.listdir(getInfo.nukeScriptsPath) if os.path.isdir(getInfo.nukeScriptsPath + '/' + item) == True ]:
		seq = dirName.split('_')[0]
		if seq == currentSeq :
			allShot.append(dirName.split('_')[1])

	# if find nothing return folder is empty
	if not allShot :
		allShot = '-- Empty --'

	return allShot

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)
