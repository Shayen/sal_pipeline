import maya.cmds as cmds
import maya.mel  as mel
import datetime, os

from sal_pipeline.src import env
from sal_pipeline.src import utils
from sal_pipeline.src import log
reload(env)
reload(utils)
reload(log)

logger = log.logger("renderSetting")
logger = logger.getLogger()
getEnv 	 = env.getEnv()
rs_utils = utils.redshiftUtils()

_APP_VERSION_ = 'v 2.1'
# v 1.0 : Build for turntable render
# v 2.0 : Add RS_AOV set up
# v 2.1 : Add log

_windowsName = "salRenderSetting_window"

# Read from config file : config/renderSetting.json
config = getEnv.get_appConfig("renderSetting")

# ---- UI ----------------------------------------

class renderSetting_window :

	def __init__(self):

		# Read from config file : config/renderSetting.json
		self._AOV_LIST = config['aov']['aov_list']

		cmds.window(_windowsName, title= "Render setting " + _APP_VERSION_)
		tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)

		# - Turntable tab
		turntable = self.tab_turntable()

		# - set aov tab
		aov = self.tab_AovSetting()

		# Adjust tab name #
		cmds.tabLayout( tabs, 
			edit	=True, 
			tabLabel= ( (turntable, 'Turntable'), 
						(aov, 'Aov setting')
						) 
			)
		
		cmds.showWindow( _windowsName )
		
		# adjust window size
		cmds.window( _windowsName, e=True, w = 400, h=100 )

	def tab_turntable(self) :
		"""  Turntable tab  """
		layout = cmds.columnLayout(adj=True)
		cmds.text(l="")
		cmds.text(l="Render path:",align="left")
		cmds.textField("RenderPath_TextFieldGroup", tx=defaultRender_path)

		cmds.text("\nasset Name :",align="left")
		cmds.textField("assetName_TextFieldGroup")
		cmds.text(l="")

		cmds.button(l="set path",c = self.setRender)
		cmds.setParent('..')

		return layout

	def tab_AovSetting(self):
		""" Aov setting tab """

		layout = cmds.columnLayout(adj  = True)

		cmds.optionMenu( "aov_optionMenu",label='Preset', changeCommand = self._setupAovOption )
		for preset in sorted( config['aov']['preset'].keys() ):
			cmds.menuItem  ( label= preset )

		cmds.text("Setup :", align = "left")
		cmds.columnLayout(adj=True)
		for menu in self._AOV_LIST :
			name = menu.replace(' ', '_') + '_checkBox'
			cmds.checkBox( name , label= menu )

		cmds.setParent('..')

		cmds.text("Setup :", align = "left")
		cmds.button(l="Set up AOV", c=self.addAov)
		cmds.setParent('..')

		self._setupAovOption()

		return layout

	# -- method --

	def setRender(self, *args):
		# Check text field

		# Read from config file : config/renderSetting.json
		defaultRender_path = config['turntable']['path']

		renderPath  = cmds.textField("RenderPath_TextFieldGroup", q=True, tx=True)
		assetName   = cmds.textField( "assetName_TextFieldGroup", q=True, tx=True)

		currentDate = datetime.datetime.now().strftime('%Y-%m-%d')
		currentTime = datetime.datetime.now().strftime('%H-%M-%S')

		if renderPath != "" and assetName != "":
			path_to_render = os.path.join( defaultRender_path, assetName,currentDate, currentTime)
			cmds.workspace( rt = ["images", path_to_render])
			cmds.setAttr("defaultRenderGlobals.imageFilePrefix","<Scene>", type = "string")
			cmds.setAttr("redshiftOptions.imageFormat",4)

		else :
			cmds.error("Field must not empty")
			return False

	def addAov(self, *args):
		""" Add selected AOV to renderer """

		# Query all selected AOV
		selected_AOV = []

		aov_list = config['aov']['aov_list']

		for aov in aov_list :
			control_name = aov.replace(" ", "_") + "_checkBox"
			try:
				isCheck = cmds.checkBox( control_name, q = True, value = True )
			except :
				logger.warning("\tSkip : " + control_name)

			if isCheck :
				aov_name = cmds.checkBox( control_name, q = True, l = True )
				selected_AOV.append(aov_name)

		for aov in selected_AOV:
			self._addAOV(aov)
			# print aov

		rs_utils.redshiftUpdateActiveAovList()

		logger.info("Add AOV preset : " + str(selected_AOV))

	def _setupAovOption(self, *args):

		currentOption = cmds.optionMenu( "aov_optionMenu", q=True, value = True )
		
		aov_list = config['aov']['preset'][currentOption]

		# clear
		self._uncheckAllAovOption()

		# Check Aov option, depend on preset
		for aov in aov_list :
			control_name = aov.replace(" ", "_") + "_checkBox"
			cmds.checkBox( control_name, e = True, value = True )

	def _uncheckAllAovOption(self):
		""" uncheck all aov check box """

		aov_list = config['aov']['aov_list']

		for aov in aov_list :
			control_name = aov.replace(" ", "_") + "_checkBox"
			try:
				cmds.checkBox( control_name, e = True, value = False )
			except :
				print ("\tSkip : " + control_name)

	def _addAOV(self, AovName):

		return mel.eval("rsCreateAov -type \"{0}\";".format( AovName ) )

def showUI():
	clearUI()

	renderSetting_window()

def clearUI():

	if cmds.window( _windowsName, q=True, exists = True ):
		cmds.deleteUI(_windowsName)
		clearUI()

if __name__ == '__main__':
	showUI()