# duplicateOverSurface

from sal_pipeline.src import env
from sal_pipeline.src import log
# logger = log.logger("duplicateOverSurface")
# logger = logger.getLogger()

import maya.cmds as cmds

_APP_VERSION_ = 'v1.0'
# V1.0 : init app


_WINDOW_NAME_  = 'duplicateOverSurface_win'
_WINDOW_TITLE_ = 'Duplicate over surface ' + _APP_VERSION_ 

env = env.getEnv()

class duplicateOverSurface_app(object):

	def __init__(self):

		# Run UI
		# self.show_ui()

		# Load Plugins
		self._loadPlugin()
			
	def show_ui(self):
		''' 
		# -------- Show main ui -----------

		# from maya import cmds
		# # Duplicate pCube1 over surface.
		# cmds.duplicateOverSurface("pCube1")

		# # Duplicate selected object over surface.
		# cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0])

		# # Duplicate selected object over surface but keep original rotations.
		# cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0], rotation=False)

		'''
		cleanUI()

		cmds.window(_WINDOW_NAME_)
		cmds.columnLayout(adj=True)

		cmds.button(l = "Duplicate selected", c= self._dupSelected)
		cmds.button(l = "Duplicate selected Keep rotate", c = self._dupSelected_keep_rotation)

		cmds.separator(h=5)
		cmds.button(l = "finish", c="cmds.setToolTo(\"selectSuperContext\") ")
		cmds.setParent('..')
		cmds.showWindow(_WINDOW_NAME_)

	def _dupSelected(self,*args):
		cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0])

	def _dupSelected_keep_rotation(self, args):
		cmds.duplicateOverSurface(cmds.ls(sl=True, long=True)[0], rotation=False)

	def _loadPlugin(self):
		''' Load plugin '''
		src_path      = env.src_dirPath()
		plugin_dir    = src_path + "/plugins"

		is_pluginLoaded = cmds.pluginInfo('duplicateOverSurface',q=True,l=True)
		
		if not is_pluginLoaded :
			try :
				cmds.loadPlugin(plugin_dir + "/duplicateOverSurface.py")
			except :
				raise IOError('Plugin not load.')

def cleanUI():
	if cmds.window( _WINDOW_NAME_, exists=True ):
		cmds.deleteUI(_WINDOW_NAME_)
		cleanUI()

if __name__ == '__main__':
	app = duplicateOverSurface_app()
	app.show_ui()

