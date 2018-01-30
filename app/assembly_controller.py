import maya.cmds as cmds
import os

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
	try :
		cmds.assembly(assemblyNode, e = True, active = name)
	except RuntimeError as e :
		print ("skip : " + assemblyNode)

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

def switch_to_ref(*args):

	class loc:
		x = 0
		y = 0
		z = 0
		rx=0
		ry=0
		rz=0
		sx = 0
		sy = 0
		sz = 0
	
	#sels = cmds.ls(type = "assemblyReference")
	sels = cmds.ls(sl=True)

	switch_grp = "switch_grp"
	if not cmds.objExists(switch_grp):
		cmds.group(n = switch_grp, em= True)

	for asm in sels :
		try :
			path = cmds.getAttr('%s.definition' %asm)
		except :
			continue

		pos 	= loc()
		pos.x 	= cmds.getAttr('%s.tx' %asm)
		pos.y	= cmds.getAttr('%s.ty' %asm)
		pos.z	= cmds.getAttr('%s.tz' %asm)
		pos.rx	= cmds.getAttr('%s.rx' %asm)
		pos.ry	= cmds.getAttr('%s.ry' %asm)
		pos.rz	= cmds.getAttr('%s.rz' %asm)
		pos.sx	= cmds.getAttr('%s.sx' %asm)
		pos.sy	= cmds.getAttr('%s.sy' %asm)
		pos.sz	= cmds.getAttr('%s.sz' %asm)

		
		cmds.hide(asm)
		
		for myfile in os.listdir(os.path.dirname(path)):
			
			if myfile.endswith("texture_pub.ma"):
				filepath = os.path.dirname(path) + '/' + myfile
				namespace = asm.split(":")[-1]
				group_name = "{ns}_refGrp".format(ns=asm)
				cmds.file(filepath, r=True, namespace = namespace,gr=True, gn= group_name)
				
				# geo_grp = "{namespace}:Geo_grp".format(namespace = namespace)
				
				cmds.parent(group_name, switch_grp)
				cmds.select(group_name)
				cmds.move(pos.x,pos.y,pos.z,group_name, relative=True)
				cmds.rotate(pos.rx,pos.ry,pos.rz)
				cmds.scale(pos.sx,pos.sy,pos.sz)
				cmds.select(cl=True)

def run():

	cleanUI()
	
	cmds.window(_windowObjName, title = _windowTitleName)
	cmds.columnLayout(adj=True,rowSpacing=2)
	cmds.text("\nScene assembly controller\n")
	cmds.button("Show all Locator", h = 40, c = showAllLocator )
	cmds.button("Show all BBox", 	h = 40, c = showAllBBox )
	cmds.button("show all GPU", 	h = 40, c = showAllGpu )
	cmds.button("show all Render", 	h = 40, c = showAllRender )
	cmds.separator(h=5)
	cmds.text(l = "Switch to ref :", align= "left")
	cmds.button("Swith to ref", c= switch_to_ref)
	cmds.setParent("..")
	
	cmds.showWindow( _windowObjName )
	
	cmds.window( _windowObjName, e=True, w=100, h = 100 )

run()