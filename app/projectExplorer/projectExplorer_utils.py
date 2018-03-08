import os, sys, json

from ...src import env
getEnv 	= env.getEnv()

def getComment(workspace):
	dataFile = workspace + "/data.json"

	#  File not exists
	if not os.path.exists(dataFile):
		return {}

	try:
		f = open(dataFile, 'r')
		data = json.loads( f.read() )
		f.close()

	except Exception as e :
		print (e)
		return {}

	return data

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