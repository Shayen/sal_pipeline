import maya.cmds as cmds

_windowObjName   = "sceneAssembly_control"
_windowTitleName = "Scene Assembly controller"


def cleanUI():
	if cmds.window( _windowObjName, exists=True ):
		cmds.deleteUI(_windowObjName)
		cleanUI()

def get_assemblyReference():
	return cmds.ls(type = "assemblyReference")

def setActiveRep( assemblyNode, name ) : 
	''' set active representations ''' 
	cmds.assembly(assemblyNode, e = True, active = name)

def showAllLocator(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	all_ref = get_assemblyReference()
	for node in all_ref :
		setActiveRep(node, "myLocator")

def showAllGpu(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	all_ref = get_assemblyReference()
	for node in all_ref :
		setActiveRep(node, "Gpu")

def showAllBBox(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	all_ref = get_assemblyReference()
	for node in all_ref :
		setActiveRep(node, "BBox")

def showAllRender(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	all_ref = get_assemblyReference()
	for node in all_ref :
		setActiveRep(node, "Render")
	
def run():

	cleanUI()
	
	cmds.window(_windowObjName, title = _windowTitleName)
	cmds.columnLayout(adj=True,rowSpacing=2)
	cmds.text("\nScene assembly controller\n")
	cmds.button("Show all Locator", h = 40, c = showAllLocator )
	cmds.button("Show all BBox", 	h = 40, c = showAllBBox )
	cmds.button("show all GPU", 	h = 40, c = showAllGpu )
	cmds.button("show all Render", 	h = 40, c = showAllRender )
	cmds.setParent("..")
	
	cmds.showWindow( _windowObjName )
	
	cmds.window( _windowObjName, e=True, w=100, h = 100 )

run()