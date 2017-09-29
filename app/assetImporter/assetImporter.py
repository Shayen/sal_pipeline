#
# ===== Maya Application template =====
# 

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMayaUI as apiUI
import shiboken

from functools import partial
import os, sys, subprocess, time

# ============ Will change to qt.py ============
import PySide.QtCore as QtCore
import PySide.QtGui	 as QtGui
import PySide.QtUiTools as QtUiTools

from sal_pipeline.src import env
from sal_pipeline.src import utils
reload(custom_widget)
reload(utils)
reload(env)

getEnv 	= env.getEnv()
getInfo = env.getInfo()
modulepath = getEnv.modulePath()

__version__ = 0.1
# V0.1

class salAssetImporter( QtGui.QMainWindow ):

	def __init__(self, parent=None):
		""" Description """
		QtGui.QMainWindow.__init__(self, parent)
		pass

#####################################################################

def openExplorer(filePath):
	"""Open File explorer after finish."""
	win_publishPath = filePath.replace('/', '\\')
	subprocess.Popen('explorer \/select,\"%s\"' % win_publishPath)

def getMayaWindow():
	"""
	Get the main Maya window as a QtGui.QMainWindow instance
	@return: QtGui.QMainWindow instance of the top level Maya windows
	"""
	ptr = apiUI.MQtUtil.mainWindow()
	if ptr is not None:
		return shiboken.wrapInstance(long(ptr), QtGui.QWidget)

def clearUI():
	if cmds.window('sal_projectExplorer',exists=True):
		cmds.deleteUI('sal_projectExplorer')
		clearUI()

def run():
	clearUI()
	app = salAssetImporter( getMayaWindow() )
	# pass

if __name__ == '__main__':
	run()