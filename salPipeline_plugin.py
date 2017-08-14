import sys
import maya.api.OpenMaya as om
import maya.OpenMayaMPx as ompx

KPluginCmdName = 'salPlugin_test'

#command
class scriptedCommand(ompx.MPxCommand):
	def __init__(self):
		ompx.MPxCommand.__init__(self)

	#invoked when the command is run
	def doIt(self,argList):
		print ("hello world")

# Creator
def cmdCreator():
	return ompx.asMPxPtr( scriptedCommand() )

#initialize the script plug-in
def initializePlugin(mobject):
	mplugin = ompx.MFnPlugin(mobject)
	try:
		mplugin.registerCommand( KPluginCmdName, cmdCreator )

	except:
		sys.stderr.write("Failed to register command: %s\n" % KPluginCmdName)
		raise

# Unintilize the script plug-in
def uninitializePlugin(mobject):
	mplugin = ompx.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand( KPluginCmdName )
	except :
		sys.stderr.write(  "Failed to unregister command: %s\n" % kPluginCmdName )