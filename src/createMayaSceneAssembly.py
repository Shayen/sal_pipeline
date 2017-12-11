# Maya Standalone

import os, sys, traceback, time

import maya.standalone
import maya.cmds as cmds
import maya.mel  as mel
maya.standalone.initialize(name='python')  

def create_sceneAssembly( workspace, assetName, pub_filepath, output_path ):
	# Start Maya in batch mode

	print ("\n") # New line
	print ("_"*32)
	print ("Building scene Assembly...")

	loadSceneAssemblyPlugin()

	# pub_filepath = pub_filepath.replace(workspace, '')
	gpu_filepath = "scenes/pub/%s_gpu.abc"%(assetName)
	box_filepath = "scenes/pub/%s_bbox.ma"%(assetName)
	
	try :
		cmds.file(f=True, new=True)

		mel.eval( 'setProject "'+ workspace +'";')

		# create Assembly Definition
		assembly_name = cmds.assembly(name = assetName+"_AD" )

		# Create Locator representation
		cmds.assembly(		assembly_name, 
							edit=True, 
							createRepresentation='Locator',
							repName="myLocator", 
							input = assetName)

		editRepresentation(	assemblyNode = assembly_name, 
							type 	= "Locator", 
							path 	= assetName, 
							newName = "Locator" , 
							oldName = "myLocator")

		print ("\t- Add Locator")

		# Create GPU representation
		if isFileExists( os.path.join(workspace,gpu_filepath) ):
			
			cmds.assembly(		assembly_name , 
								edit	= True   , 
								createRepresentation='Cache',
								repName	= "Gpu"  , 
								repLabel= "GPU")

			editRepresentation(	assemblyNode = assembly_name, 
								type 	= "Cache", 
								path 	= os.path.join(workspace,gpu_filepath), 
								newName = "Gpu" , 
								oldName = "Gpu")

			print ("\t- Add GPU" )

		# Create BBox representation
		if isFileExists( os.path.join(workspace,box_filepath) ):
		
			cmds.assembly(	assembly_name , 
							edit	= True   , 
							createRepresentation='Scene',
							repName	= "BBox"  , 
							repLabel= "BBOX")

		editRepresentation(	assemblyNode = assembly_name, 
							type 	= "Scene", 
							path 	= os.path.join(workspace,box_filepath), 
							newName = "BBox" , 
							oldName = "BBox")

		print ("\t- Add Bounding box" )

		# Create Render representation
		if isFileExists( pub_filepath ):
	
			cmds.assembly(	assembly_name , 
							edit	= True   , 
							createRepresentation='Scene',
							repName	= "Render"  , 
							repLabel= "Render" )

		editRepresentation(	assemblyNode = assembly_name, 
							type 	= "Scene", 
							path 	= os.path.join(workspace,pub_filepath) , 
							newName = "Render" , 
							oldName = "Render")

		print ("\t- Add Render geometry")

		# Save the file    
		cmds.file( rename = output_path )
		result =  cmds.file( save=True, type='mayaAscii' )


		uninitialize_maya()

	except Exception as e :
		print(e)
		traceback.print_exc()
		# time.sleep(10)

	print ("Create scene assembly success : " + output_path )
	# time.sleep(1)

def uninitialize_maya():
	# Starting Maya 2016, we have to call uninitialize to properly shutdown
	if float(cmds.about(v=True)) >= 2016.0:
		maya.standalone.uninitialize()

def loadSceneAssemblyPlugin():
	'''
	Load AbcExport plugin
	'''
	# Load AbcExport plugin
	if not cmds.pluginInfo('sceneAssembly',q=True,l=True):
		try:
			cmds.loadPlugin('sceneAssembly', quiet=True)
		except:
			raise Exception('Error loading sceneAssembly plugin!')
			time.sleep(10)

def editRepresentation(assemblyNode, type, path, newName, oldName):
	''' add representations & rename & relabel --> type = Scene / Cache / Locator '''
	# _addRepresentation(assemblyNode, type, path)
	listNameIndex  = listRepIndex(assemblyNode, listType = 'name')
	listLabelIndex = listRepIndex(assemblyNode, listType = 'label')

	# check if given name is in the representation list 
	if oldName in listNameIndex : 
		setName (assemblyNode, listNameIndex.index(oldName), newName)
		setLabel(assemblyNode, listNameIndex.index(oldName), newName)
		setData (assemblyNode, listNameIndex.index(oldName), path)

		return True 

	else : 
		mm.eval('warning "No name [%s] in representation list";' % oldName)
		return False 

def _addRepresentation(assemblyNode, type, path) : 
	''' add representations --> type = Scene / Cache / Locator '''
	result = cmds.assembly(assemblyNode, edit = True, createRepresentation = type, input = path)
	return result 

def listRepIndex(assemblyNode, listType = 'name') : 
	''' query representation lists --> listType = name / label ''' 
	lists = cmds.assembly(assemblyNode, q = True, listRepresentations = True)

	if listType == 'name' : 
		return lists 

	labels = []
	datas = []

	if lists : 
		for i in range(len(lists)) : 
			label = cmds.getAttr('%s.representations[%s].repLabel' % (assemblyNode, i))
			data = cmds.getAttr('%s.representations[%s].repData' % (assemblyNode, i))
			labels.append(label)
			datas.append(data)

	if listType == 'label' : 
		return labels 

	if listType == 'data' : 
		return datas

def setLabel(assemblyNode, index, newName) :
	''' change label name by giving index item '''  
	cmds.setAttr('%s.representations[%s].repLabel' % (assemblyNode, index), newName, type = 'string')


def setName(assemblyNode, index, newName) : 
	''' change name by giving index item ''' 
	activeNode = getActiveRep(assemblyNode)

	cmds.setAttr('%s.representations[%s].repName' % (assemblyNode, index), newName, type = 'string')

def setData(assemblyNode, index, value) :
	''' change label name by giving index item '''  
	cmds.setAttr('%s.representations[%s].repData' % (assemblyNode, index), value, type = 'string')

def getActiveRep(assemblyNode) : 
	''' query active representations ''' 
	activeNode = cmds.assembly(assemblyNode, q = True, active = True)
	
	return activeNode 

def isFileExists(filePath) :
	return os.path.exists(filePath)

if __name__ == '__main__':

	workspace   = sys.argv[1]
	assetName	= sys.argv[2]
	pub_filepath= sys.argv[3]
	output_path = sys.argv[4]
	create_sceneAssembly(workspace,assetName,pub_filepath,output_path)