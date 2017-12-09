import maya.cmds as cmds

def isGpuCacheNode(gpuCacheNode):
	'''
	Check if the specified node is a valid GPU cache node
	@param gpuCacheNode: Object to query
	@type gpuCacheNode: str
	'''
	# Check object exists
	if not cmds.objExists(gpuCacheNode): return False
	
	# Check node type
	if cmds.objectType(gpuCacheNode) != 'gpuCache': return False
	
	# Return result
	return True

'''
- Ma  file
- Export GPU
- Export BBox

create AD file & locator (create by default)
'''

# Export GPU
def loadAbcExportPlugin():
	'''
	Load AbcExport plugin
	'''
	# Load AbcExport plugin
	if not cmds.pluginInfo('AbcExport',q=True,l=True):
		try:
			cmds.loadPlugin('AbcExport', quiet=True)
		except:
			raise Exception('Error loading AbcExport plugin!')

def loadGpuCachePlugin():
	'''
	Load gpuCache plugin
	'''
	# Load gpuCache plugin
	if not cmds.pluginInfo('gpuCache',q=True,l=True):
		try:
			cmds.loadPlugin('gpuCache', quiet=True)
		except:
			raise Exception('Error loading gpuCache plugin!')

def exportGpuCache(objName , dest, filename):
	'''
	Export GPU cache

	Variable :
	@objName	: Object name
	@dest		: Directory destination
	@filename	: finemat without extension
	'''
	# Export GPU cache
	loadGpuCachePlugin()

	loadAbcExportPlugin()

	result = cmds.gpuCache(	objName,
					startTime	= 1,
					endTime		= 1,
					optimize 	= True,
					optimizationThreshold = 40000, 
					writeMaterials = True,
					dataFormat 	= "ogawa", 
					directory 	= dest,
					fileName 	= filename)

	return str(result)
