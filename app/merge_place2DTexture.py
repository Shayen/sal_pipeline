import maya.cmds as cmds
import pprint

BASE = "place2dTexture1"

# [ place2dTexture, file ]
_CONNECTION_DATA = [
	[u'coverage', u'coverage'],
	[u'translateFrame', u'translateFrame'],
	[u'rotateFrame', u'rotateFrame'],
	[u'mirrorU', u'mirrorU'],
	[u'mirrorV', u'mirrorV'],
	[u'stagger', u'stagger'],
	[u'wrapU', u'wrapU'],
	[u'wrapV', u'wrapV'],
	[u'repeatUV', u'repeatUV'],
	[u'offset', u'offset'],
	[u'rotateUV', u'rotateUV'],
	[u'noiseUV', u'noiseUV'],
	[u'vertexUvOne', u'vertexUvOne'],
	[u'vertexUvTwo', u'vertexUvTwo'],
	[u'vertexUvThree', u'vertexUvThree'],
	[u'vertexCameraOne', u'vertexCameraOne'],
	[u'outUV', u'uvCoord'],
	[u'outUvFilterSize', u'uvFilterSize']
]

_WINDOW_NAME_ = "MergePlace2DTextureNode_win"

def get_ConnectionData() :
	connection = cmds.listConnections(BASE, p=True)
	plug = []

	for i in connection:
		
		print (cmds.listConnections(i, p=True)[0],i)
		
		if i.startswith("file"):
			head = cmds.listConnections(i, p=True)[0].split('.')[0]
			tail = i.split('.')[1]
			plug.append( [head, tail])
			
	pprint.pprint( plug)

def _disconnect_input_fileNode(nodename):

	nodename = nodename
	connection = cmds.listConnections(nodename, p=True)
	plug = []

	# Collect incoming connection data
	for i in connection:
		
		if i.startswith("place2dTexture"):
			head = i
			tail = cmds.listConnections(i, p=True)[0]
			
			try:
				cmds.disconnectAttr(head, tail)
			except Exception as e :
				print (e)

def connectData(*args):
	BASE_NODE = cmds.textField("_textField_baseNodeName", q=True, tx=True)

	# select file node
	mysel = cmds.textScrollList("_textScrollList_selectNode", q=True, allItems=True)

	for node in mysel :

		# Disconnect
		_disconnect_input_fileNode(node)

		# Connect new route
		for head, tail in _CONNECTION_DATA:
			try:
				cmds.connectAttr( BASE_NODE+ '.' +head, node + '.' + tail)
			except Exception as e :
				print (e)
				
def _loadSelectedNode(*args):

	cmds.textScrollList("_textScrollList_selectNode", e=True, removeAll=True)

	# Load selected node
	selectedNode = cmds.ls(sl=True)
	cmds.textScrollList("_textScrollList_selectNode", e=True, append=selectedNode)

def main():
	clearUI()

	cmds.window(_WINDOW_NAME_)
	cmds.columnLayout(adj=True)
	cmds.text(l="\n::Merge placement 2d texture::\n")
	cmds.text(l="Base node :", align="left")
	cmds.textField("_textField_baseNodeName")
	cmds.setParent("..")

	cmds.columnLayout(adj=True)
	cmds.text(l="Selected node :", align="left")
	cmds.textScrollList("_textScrollList_selectNode")

	cmds.rowLayout(nc=2)
	
	cmds.button(l="load selected node",c= _loadSelectedNode)
	cmds.button(l="Merge", c= connectData)
	cmds.setParent("..")

	cmds.setParent("..")
	cmds.showWindow(_WINDOW_NAME_)

	cmds.window(_WINDOW_NAME_, e = True, w = 100 )

def clearUI():
	if cmds.window( _WINDOW_NAME_,exists=True):
		cmds.deleteUI(_WINDOW_NAME_)
		clearUI()

if __name__ == '__main__':
	main()