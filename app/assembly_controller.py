import maya.cmds as cmds
import pymel.core as pm
import os

_windowObjName   = "sceneAssembly_control"
_windowTitleName = "Scene Assembly controller"

def cleanUI():
	if cmds.window( _windowObjName, exists=True ):
		cmds.deleteUI(_windowObjName)
		cleanUI()

def get_assemblyReference(mode=None):
	''' Return assembly node list depend on mode '''

	if not mode :
		mode = cmds.optionMenu("assembly_control_mode", q=True, v=True)

	# mode : all
	if mode == "all":
		result = cmds.ls(type = "assemblyReference")

	# mode : selected
	elif mode == "selected" :
		sels = pm.selected()
		result = []

		# Get name space
		for node in sels :
			parent_namespace = ""
			namespace = node.name().split(":")

			# If have namespace
			if len(namespace) > 1 :

				child_namespace = namespace[-2]

				# Type : ASM
				if pm.nodeType(node) == "assemblyReference" :
					nodename = parent_namespace+node.name()
					if nodename not in result :
						result.append(nodename)
				
				# Type : Not ASM
				else :
					# Get parent Namespace
					if len(namespace) >= 3 :
						parent_namespace = ":".join(namespace[:-2]) + ":"

					# Get assembly node name
					asm_nodeName = parent_namespace + child_namespace.replace("_NS", "")
					if asm_nodeName not in result :
						result.append(asm_nodeName)

			# Not have name space
			else :
				# Check for "assemblyReference" node
				if pm.nodeType(node) == "assemblyReference" :
					if node not in result :
						result.append(node.name())

	return result

def setActiveRep( assemblyNodes, name ) : 
	''' set active representations ''' 

	amount = len(assemblyNodes)
	exclude_nodes = cmds.textScrollList("exclude_list", q=True, allItems = True)
	exclude_nodes = exclude_nodes if exclude_nodes != None else list()

	print amount
	progress = cmds.progressWindow( title='Switching...',progress=0,max = int(amount),isInterruptable=True )

	cmds.refresh()

	for indx,asm in enumerate(assemblyNodes) :
		# Check progress bar cancelation
		if cmds.progressWindow( progress, query=True, isCancelled=True ) :
			break

		is_ignore = True if asm in exclude_nodes else False
		
		try :
			if cmds.assembly(asm, q = True, active = True) != name and not is_ignore:
				cmds.assembly(asm, e = True, active = name)
		except RuntimeError as e :
			print ("RuntimeError > skip : " + asm)
		except TypeError as e :
			print ("TypeError > skip : " + asm)
		except ValueError as e:
			print ("ValueError > skip : " + asm)

		cmds.progressWindow( progress,  
			edit=True, 
			step=1, 
			status=('Switching to '+name+' : ' + str(indx+1) + '/' + str(amount) ) )

	# if cmds.progressWindow( progress, query=True, progress=True ) >= 100 :
	cmds.progressWindow( progress, endProgress	= True)

def showAllLocator(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	setActiveRep( get_assemblyReference(), "Locator" )

def showAllGpu(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	setActiveRep( get_assemblyReference(), "Gpu" )

def showAllBBox(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	setActiveRep( get_assemblyReference(), "BBox" )

def showAllRsProxy(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	setActiveRep( get_assemblyReference(), "RsProxy" )

def showAllRender(*args):
	'''
	# Result: [u'myLocator', u'Gpu', u'BBox'] # 	
	'''
	result = cmds.confirmDialog( 
		title='Confirm', 
		message='Are you sure?\nSwith to \'RENDER\' will take a long time.', 
		button=['Yes','No'],
		defaultButton='Yes',
		cancelButton='No',
		dismissString='No' )

	if result != 'Yes' :
		return False

	setActiveRep( get_assemblyReference(), "Render" )

def switch_to_ref(*args):

	class loc:
		x  = 0
		y  = 0
		z  = 0

		rx = 0
		ry = 0
		rz = 0
		
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
				cmds.xform(group_name, piv=(0,0,0), ws=True)
				cmds.parent(group_name, switch_grp)
				cmds.select(group_name)
				cmds.move(pos.x,pos.y,pos.z,group_name, relative=True)
				cmds.rotate(pos.rx,pos.ry,pos.rz)
				cmds.scale(pos.sx,pos.sy,pos.sz)
				cmds.select(cl=True)

def selectFromView(*args):
	import maya.OpenMaya as om
	import maya.OpenMayaUI as omu

	view = omu.M3dView.active3dView()
	om.MGlobal.selectFromScreen(0, 0, view.portWidth(), view.portHeight(), om.MGlobal.kReplaceList)

def hideFromCamera(*args):
	selectFromView()

	sels = cmds.ls(sl=True)

	# List all ASM
	all_ASM = get_assemblyReference(mode = 'all')

	# List select ASM
	selected_ASM = get_assemblyReference(mode="selected")

	nodes = set(all_ASM).difference(set(selected_ASM))
	setActiveRep(nodes, "Locator")

	cmds.select(cl=True)

def hideLocatorRep(*args):
	all_asm = get_assemblyReference(mode = "all")

	for asm in all_asm :
		if cmds.assembly(asm, q = True, active = True) == "Locator":
			cmds.hide(asm)

def showAllASM(*args):
	all_asm = get_assemblyReference(mode = "all")

	for asm in all_asm :
		cmds.showHidden(asm)

def assembly_control_mode_onChange(mode):
	cmds.button("ShowAllLocator", 	e=True, l = "Show " + mode + " Locator")
	cmds.button("ShowAllBBox", 		e=True, l = "Show " + mode + " BBox")
	cmds.button("showAllGPU", 		e=True, l = "show " + mode + " GPU")
	cmds.button("showAllProxy", 	e=True, l = "show " + mode + " Proxy")
	cmds.button("showAllRender", 	e=True, l = "show " + mode + " Render")

def addExcludeItem(*args):
	all_selection = get_assemblyReference(mode = 'selected')
	exists_items  = cmds.textScrollList("exclude_list", q=True, allItems = True)

	if exists_items :
		items = list(set(all_selection).difference(exists_items))
	else : 
		items = all_selection

	cmds.textScrollList("exclude_list", e=True, append = items)

def deleteExcludeItem(*args):
	selectedItems = cmds.textScrollList("exclude_list", q=True, selectItem = True)
	# removeItem
	cmds.textScrollList("exclude_list", e=True, removeItem = selectedItems)
			
def run():

	cleanUI()
	
	cmds.window(_windowObjName, title = _windowTitleName)

	cmds.columnLayout(adj=True,rowSpacing=2)
	cmds.text("\nScene assembly controller\n")

	cmds.optionMenu( "assembly_control_mode",label='mode:',changeCommand = assembly_control_mode_onChange )
	cmds.menuItem( label='selected' )
	cmds.menuItem( label='all' )

	cmds.rowLayout(nc=2,adj=1)

	# ---------------------------------------------------------------
	cmds.columnLayout(adj=True)
	cmds.text(l="Exclude nodes :")
	cmds.textScrollList("exclude_list", allowMultiSelection=True)
	# - - - - - - - - - - - - - - 
	cmds.rowLayout(nc=2,adj=1)
	cmds.button(l="add selection" , c= addExcludeItem)
	cmds.button(l="delete selection", c = deleteExcludeItem)
	cmds.setParent("..")
	cmds.setParent("..")
	# - - - - - - - - - - - - - - 
	cmds.columnLayout(adj=True,rowSpacing=2)
	cmds.button("ShowAllLocator",   l="Show all Locator"	, h = 40, c = showAllLocator )
	cmds.button("ShowAllBBox", 		l="Show all BBox"		, h = 40, c = showAllBBox )
	cmds.button("showAllGPU", 		l="show all GPU"		, h = 40, c = showAllGpu )
	cmds.button("showAllProxy", 	l="show all Proxy"		, h = 40, c = showAllRsProxy )
	cmds.button("showAllRender", 	l="show all Render"		, h = 40, c = showAllRender )
	cmds.setParent("..")
	cmds.setParent("..")

	cmds.separator(h=5) # ------------------------------------------

	cmds.columnLayout(adj=True,rowSpacing=2)
	cmds.text(l = "Switch to ref :", align= "left")
	cmds.button("Swith to ref", c= switch_to_ref)
	cmds.separator(h=5)

	cmds.button("Select from view", c=selectFromView)
	cmds.button("Hide geo out of camera", c = hideFromCamera)
	cmds.separator(h=5)

	cmds.text(l = "Hide / Show :", align= "left")
	cmds.button("Hide Locator representation", c=hideLocatorRep)
	cmds.button("Show all assemblies", c = showAllASM)
	cmds.setParent("..") # ------------------------------------------
	cmds.setParent("..") # Main layout
	
	cmds.showWindow( _windowObjName )
	
	cmds.window( _windowObjName, e=True, w=200, h = 100 )

	# print (cmds.optionMenu("assembly_control_mode", q=True, v=True))
	assembly_control_mode_onChange('selected')

run()