#############################################################################
# MIT License
#
# Copyright (c) 2017 Sirasit sawetprom
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#############################################################################

import maya.cmds as cmds
import os, json

try :
	from tool.utils import entityInfo
	is_importEntityInfo = True
except ImportError :

	try:
		from sal_pipeline.src import env
		entityInfo = env
		is_importEntityInfo = False
	except ImportError as e:
		raise ImportError (e)

# VERSION
# 3.0   : Bug fix Query reference node.
# 3.1.2 : Bug fix Query reference node.
# 3.1.3 : Fix select from selection.
# 3.2   : clean up for use out of PT pipeline( Exception of importError PT.EntityInfo ).
# 3.3	: Support SAL pipeline workflow

# Todo [in future]:
#     [] Get new asset's ref path from popup UI with Thumbnail image.

def run_scriptJob_selectSomthing (*args):
	''' run this when somthing selected '''
	print ('Something selected!!')

class massRefRlps_UI(object):

	_toolName_ = 'Massive Reference replacement'
	# > {'Objectname':['nameSpace','node',PATH']}
	_allRef_NS_ = {}
	_appVersion_ = '3.3.0 Release'

	def __init__(self):
		self.isSelectFromUI = False

	def buttonGetRefPath_OnClick(self, *args):
		refPath = cmds.fileDialog2(fileMode = 1, dialogStyle=2)[0]
		print refPath
		refPath = refPath.replace('\\','/')
		print ('DEBUG : massRefRlps_UI|buttonGetRefPath_OnClick > refPath : ' + str(refPath) )
		cmds.textFieldGrp( 'textFieldGrp_RefPath', edit=True, text = refPath)

	def get_allRef(self,*args):

		#Get all ref path
		self._allRef_NS_ = {}
		allRefPathDict = {}

		#Get all ref node
		allRefNode = cmds.ls(type='reference')

		allRefNode_temp = allRefNode[:]
		for RN in allRefNode_temp:
			if 'sharedReferenceNode' in RN :
				allRefNode.remove(RN)

		allRefNode_temp = allRefNode[:]
		#Get all ref path
		for node in allRefNode_temp :
			try:
				refPath_tmp = cmds.referenceQuery(node, f = True) 
				allRefPathDict[str(node)] = refPath_tmp
			except RuntimeError :
				allRefNode.remove(node)

		#Check have ref inscene?
		if len(allRefNode) > 0:
			#if => True
			print('DEBUG : massRefRlps_UI|get_allRef > len(allRefPath) > 1 : True [' + str(len(allRefNode)) + ']')

			#Create progress bar window ------------
			if cmds.window('masRefReplace_progressBar_win',ex=True):
				cmds.deleteUI('masRefReplace_progressBar_win')

			cmds.window('masRefReplace_progressBar_win')
			cmds.columnLayout(adj=True)

			progressControl = cmds.progressBar('masRefReplace_progressBar',maxValue=10, width=300)
			#cmds.button( label='cancle', command='cmds.deleteUI(\'masRefReplace_progressBar_win\')' )

			cmds.showWindow( 'masRefReplace_progressBar_win' )

			print ('DEBUG : massRefRlps_UI|get_allRef : Progressbar window Create.')
			#----------------------------------------

			#Get filepath
			for node in allRefNode :

				path = allRefPathDict[node]

				#Edit progress bar
				cmds.progressBar( 'masRefReplace_progressBar',
				edit=True,
				beginProgress=True,
				isInterruptable=True,
				status='"Example Calculation ...',
				maxValue=len(allRefNode) )

				#Get name space from path
				try : 
					nameSpace = cmds.file( path, q = True, namespace = True)
					RN_name = cmds.file( path, q = True, referenceNode = True)
				except :
					cmds.progressBar('masRefReplace_progressBar', edit=True, endProgress=True)
					cmds.deleteUI('masRefReplace_progressBar_win')
					TypeError('Not Reference obj.')
					return None

				print('LOADING DATA : ' + RN_name )
				chrildren=[]
				for nameSpacechild in [cmds.ls(childObj,l=True)[0] for childObj in cmds.namespaceInfo(nameSpace ,listOnlyDependencyNodes=True)] :

					#get only transform node in namespace Child [transform & mesh]
					if cmds.nodeType(nameSpacechild) == 'transform' or cmds.nodeType(nameSpacechild) == 'mesh' :

						#
						if 'grp' not in nameSpacechild.split('|')[-1] and 'Grp' not in nameSpacechild.split('|')[-1] and '_loc' not in nameSpacechild.split('|')[-1] :
							#print nameSpacechild

							#Add reference data to Dictionary
							path = path.split('.ma')[0]
							path = path+'.ma'
							uid  = cmds.ls(nameSpacechild,uuid=True)[0]
							# self._allRef_NS_[nameSpacechild] = {'namespace' : nameSpace,'node' : node,'path' : path,'uid' : uid}
							chrildren.append(nameSpacechild)

							# print ('.... .... [DEBUG] :' + str(self._allRef_NS_[nameSpacechild]))
							cmds.progressBar('masRefReplace_progressBar', edit=True, step=1)
						else :
							# print ('.... .... [ERROR] : SKIP 2 => ' + str(nameSpacechild.split('|')[-1]))
							cmds.progressBar('masRefReplace_progressBar', edit=True, step=1)
					else :
						# print ('.... .... [ERROR] : SKIP '+ cmds.nodeType(nameSpacechild) +' => ' + str(nameSpacechild.split('|')[-1]))
						cmds.progressBar('masRefReplace_progressBar', edit=True, step=1)

				uid = cmds.ls(RN_name,uuid=True)[0]
				self._allRef_NS_[RN_name] = {'namespace' : nameSpace, 'path' : path,'uid' : uid, 'children' : chrildren }


			cmds.progressBar('masRefReplace_progressBar', edit=True, endProgress=True)
			cmds.deleteUI('masRefReplace_progressBar_win')
			
		else:

			print('DEBUG : massRefRlps_UI|get_allRef > len(allRefPath) > 1 : False : ' + str(len(allRefNode)))

			self._allRef_NS_ = {'None':{'None':None}}

	def refreshIcon_onclick(self,*args):

		print('DEBUG : massRefRlps_UI|refreshIcon_onclick : >>> function start <<<')

		self.get_allRef()

		allrefDict = self._allRef_NS_
		allref=[]

		# print (json.dumps(allrefDict,indent=2))

		#collect all ref Objname
		allref = allrefDict.keys()
			

		allref.sort()
		
		print('DEBUG : massRefRlps_UI|refreshIcon_onclick : collect all ref Objname.')

		cmds.textScrollList( 	'textScrollList_allLists', e=True, removeAll=True )
		cmds.textScrollList( 	'textScrollList_allLists',
								edit = True , 
								allowMultiSelection=True, 
								append=allref)
		# cmds.textScrollList( 'textScrollList_selectedList', e=True,removeAll=True)

		print('DEBUG : massRefRlps_UI|refreshIcon_onclick : Update textScrollList.')

	def button_SelectFromeList_Onclick(self, *args):

		print('DEBUG : massRefRlps_UI|button_SelectFromeList_Onclick : >>> function start <<<')

		mySelect = cmds.textScrollList('textScrollList_allLists', q=True, selectItem=True )
		cmds.select(mySelect)

	def buttonmoveToSelected_onClick(self, *args):

		print('DEBUG : massRefRlps_UI|buttonmoveToSelected_onClick : >>> function start <<<')

		SelectedItem = cmds.textScrollList( 'textScrollList_allLists', q=True, si=True)
		cmds.textScrollList( 'textScrollList_selectedList', e=True, append=SelectedItem)

	def massRefRlps_submit_onClick(self, *args):

		print('DEBUG : massRefRlps_UI|massRefRlps_submit_onClick : >>> function start <<<')

		allrefDict = self._allRef_NS_.copy()
		RN_name = []

		SelectedItem = cmds.textScrollList( 'textScrollList_allLists', q=True, si=True)
		selectedFile = cmds.ls( sl=True, l=True)

		if len(SelectedItem) > 0 :
			RN_name = SelectedItem

		elif len(selectedFile) > 0:
			for obj in selectedFile[:] :
				if '_loc' in obj.split('|')[-1] or cmds.referenceQuery( obj, isNodeReferenced=True ) is False:
					selectedFile.remove(obj)
					print('DEBUG : massRefRlps_UI|massRefRlps_submit_onClick : !! REMOVE \'' + obj + '\' !!')
				else :
					RN_name.append( cmds.referenceQuery( obj, referenceNode = True ))

		else :
			cmds.error('Nothing select !!')

		#Create progress bar window ------------
		if cmds.window('masRefReplace_progressBar_win',ex=True):
			cmds.deleteUI('masRefReplace_progressBar_win')

		cmds.window('masRefReplace_progressBar_win')
		cmds.columnLayout(adj=True)

		progressControl = cmds.progressBar('masRefReplace_progressBar_replace',maxValue=10, width=300)
		
		cmds.showWindow( 'masRefReplace_progressBar_win' )

		print ('DEBUG : massRefRlps_UI|get_allRef : Progressbar window Create.')
		#----------------------------------------

		#Get dest Path
		destPath = cmds.textFieldGrp( 'textFieldGrp_RefPath', q=True, text=True)
		if not os.path.exists(destPath) :
			cmds.deleteUI('masRefReplace_progressBar_win')
			cmds.error('new path file doensn\'t exists.')

		count = len(RN_name)

		#Edit progress bar
		cmds.progressBar( 'masRefReplace_progressBar_replace',
		edit=True,
		beginProgress=True,
		isInterruptable=True,
		status='"Example Calculation ...',
		maxValue=len(RN_name) )

		print ('>>>>>>>>>>>> START REPLACEMENT <<<<<<<<<<<<')
		replacedNode = []
		for i in range(count):
			RN_nodeName = RN_name[i]

			if RN_nodeName not in replacedNode and os.path.exists(destPath) :
				newPath = cmds.file(destPath,loadReference = RN_nodeName,options = "v=0",f=True)

				# rename namespace
				if is_importEntityInfo :

					new_namespace = entityInfo.info(destPath).name() 
					cmds.file(destPath,e=True, namespace = new_namespace)
				else :
					new_namespace = entityInfo.getInfo(path = destPath).get_name()
					cmds.file(destPath,e=True, namespace = new_namespace)

				#rename reference node
				cmds.lockNode(RN_nodeName,l=False)
				rename_result = cmds.rename(RN_nodeName, new_namespace+'RN')
				cmds.lockNode(rename_result,l=True)

				print ('    Old reference node ')
				print ('      object   : ' + RN_name[i] )
				print ('      RFnode   : ' + RN_nodeName )
				print ('    replace with ')
				print ('      objectNS : ' + cmds.file( newPath, q = True, namespace = True) + ':' )
				print ('      path 	   : ' + newPath +'\n    ........................................')
				replacedNode.append( RN_nodeName )
				cmds.progressBar('masRefReplace_progressBar_replace', edit=True, step=1)

			else :
				if not os.path.exists( RN_nodeName ) :
					print( RN_nodeName + ' is not exists!!!')
				else :
					print( destPath + ' is not exists!!!')

				cmds.progressBar('masRefReplace_progressBar_replace', edit=True, step=1)

			
			#print count
			count += 1
		
		cmds.progressBar('masRefReplace_progressBar_replace', edit=True, endProgress=True)
		cmds.deleteUI('masRefReplace_progressBar_win')

		self.refreshIcon_onclick()
		print('=============== Process End ===============')

	def button_SelectFromeList_onClick(self,*args):
		mySel = cmds.ls(sl=True)


		print mySel

	def button_SelectAllList_onClick(self,*args):
		print('DEBUG : massRefRlps_UI|button_SelectAllList_onClick : >>> function start <<<')
		allselectedItem = cmds.textScrollList( 'textScrollList_selectedList', q=True, ai=True)
		cmds.textScrollList( 'textScrollList_selectedList', e=True, si=allselectedItem)
	
	def textScrollList_allLists_onSelect(self, *args):
		cmds.select(cl=True)
		selectedItm = cmds.textScrollList( 	'textScrollList_allLists', q=True, si=True)

		ref_obj = cmds.referenceQuery(selectedItm, n=True)
		cmds.select(ref_obj)

		self.isSelectFromUI = True

	def clear_allSelection(self,*args):
		cmds.select(cl=True)
		# current_select = cmds.textScrollList( 'textScrollList_allLists', q=True, selectItem=True)
		cmds.textScrollList( 'textScrollList_allLists', e=True, da=True)
	
	def select_fromSelection(self,*args):

		cmds.textScrollList( 'textScrollList_allLists', e=True, da=True)
		mySel = cmds.ls(sl=True)
		myNamespace = []

		for item in mySel:
			if cmds.referenceQuery(item, isNodeReferenced = True):
				refNode = cmds.referenceQuery(item, referenceNode=True)
				if refNode in cmds.textScrollList( 'textScrollList_allLists', q=True, allItems=True):
					myNamespace.append(refNode)

		cmds.textScrollList( 'textScrollList_allLists', e=True, selectItem=myNamespace)

	def run_scriptJob_selectSomthing(self,*args):

		# print 'Mysel'
		if not self.isSelectFromUI:
			cmds.textScrollList( 'textScrollList_allLists', e=True, da=True)
		self.isSelectFromUI = False

	def showUI(self):

		if(cmds.window('massRefRlps_window', ex=True)):
			cmds.deleteUI('massRefRlps_window')

		print ('=========================== START UP ===========================')

		allRef = []

		self.myWindow = cmds.window('massRefRlps_window',w=350, title = self._toolName_)

		cmds.columnLayout(adj=True,rs=10)

		#----------------------------------------
		cmds.rowLayout(adj=True,nc=3,columnAlign =[ (1,'left'), (2,'right') ] )
		cmds.text( l = self._toolName_, fn='boldLabelFont' )
		cmds.iconTextButton( 'iconTextButton_refresh' ,style='iconAndTextHorizontal', image1='refresh.xpm', label='Refresh' , c = self.refreshIcon_onclick )
		#cmds.text( l = 'Refresh', fn='boldLabelFont' )
		cmds.setParent('..')
		#----------------------------------------

		cmds.columnLayout( adj=True )
		cmds.text(l='All Reference node : ', align='left')
		cmds.separator()

		#============== center =============
		myTextScrollList = cmds.textScrollList( 	'textScrollList_allLists',
								numberOfRows=20, 
								allowMultiSelection=True, 
								append=allRef,
								sc = self.textScrollList_allLists_onSelect)

		cmds.columnLayout(adj=True)
		cmds.setParent('..')

		cmds.setParent('..')
		#----------------------------------------
		cmds.rowLayout(adj=True,nc=3, columnAlign=[1,'left'])
		cmds.text(l='')
		cmds.button(l='From selection', c=self.select_fromSelection)
		cmds.button(l='Clear all selected', c = self.clear_allSelection)
		cmds.setParent('..')

		cmds.rowLayout(adj=True,nc=3, columnAlign=[2,'left'])
		cmds.textFieldGrp( 'textFieldGrp_RefPath',label='new Reference path : ', text='path:/...')
		cmds.button('button_GetRefPath', l ='...', c=self.buttonGetRefPath_OnClick)
		cmds.setParent('..')
		#----------------------------------------
		cmds.columnLayout(adj=True,rs=10)
		#cmds.checkBox('checkBox_Transfrom',l='Replace transform',en=False,v=False)
		#cmds.button('button_SelectFromeList', l='Get name from selection', h=45, en=True, c=self.button_SelectFromeList_onClick)
		cmds.button('massRefRlps_submit',l='replace', c= self.massRefRlps_submit_onClick,h=50,bgc=(0.5,1,0))
		cmds.setParent('..')
		#----------------------------------------
		cmds.rowLayout(adj=True,nc=2 )
		cmds.text(l='version : '+self._appVersion_)
		cmds.button(l='Close', en=True, c='cmds.deleteUI(\'massRefRlps_window\')', w=100)
		cmds.setParent('..')
		#----------------------------------------

		cmds.setParent('..')

		cmds.showWindow('massRefRlps_window')

		print('DEBUG : massRefRlps_UI|showUI : Main window created.')
		self.refreshIcon_onclick()

		jobNum = cmds.scriptJob( ct= ["SomethingSelected", self.run_scriptJob_selectSomthing], p = self.myWindow )

if __name__ == '__main__':
	app = massRefRlps_UI()
	app.showUI()

	
