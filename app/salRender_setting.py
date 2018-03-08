import maya.cmds as cmds
import maya.mel  as mel
import datetime, os

from sal_pipeline.src import env
from sal_pipeline.src import utils
from sal_pipeline.src import log
# reload(env)
# reload(utils)
# reload(log)

logger = log.logger("renderSetting")
logger = logger.getLogger()
getEnv 	 = env.getEnv()
getInfo	 = env.getInfo()
rs_utils = utils.redshiftUtils()

_APP_VERSION_ = 'v 2.2'
# v 1.0 : Build for turntable render
# v 2.0 : Add RS_AOV set up
# v 2.1 : Add log
# v 2.2 : Add Shot option

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

		cmds.optionMenu("optionMenu_option", label='Option', changeCommand=self.optionmenu_onChange )
		cmds.menuItem( label='Turntable' )
		cmds.menuItem( label='Shot' )

		cmds.text(l="Render path:",align="left")
		cmds.textField("RenderPath_TextFieldGroup", tx = config['turntable']['path'])

		cmds.text("text_assetname",l="\nasset Name :",align="left")
		cmds.textField("assetName_TextFieldGroup")

		cmds.text("text_version",l="version :",align="left")
		cmds.rowLayout(ad1 = True, nc = 2)
		cmds.text("v")
		cmds.textField("textField_version")
		cmds.setParent("..")
		cmds.text(l="")

		cmds.button(l="set path",c = self.setRender)
		cmds.setParent('..')

		# set to if entity is shot
		if getInfo.isType() == 'shot' :
			cmds.text("text_assetname", e=True, l = "\nshot Name" )
			cmds.optionMenu("optionMenu_option", e=True, value = 'Shot')
			self.optionmenu_onChange()

		# set version
		assetPath 	= cmds.textField("RenderPath_TextFieldGroup",q=True,tx=True)
		assetPath 	+= '/' + cmds.textField("assetName_TextFieldGroup",q=True,tx=True)
		version 	= "%04d"%int(_checkversion(assetPath))
		cmds.textField("textField_version", e=True, tx = version)

		return layout

	def optionmenu_onChange(delf, *args):
		current_option = cmds.optionMenu("optionMenu_option",q=True, value = True)
		if current_option == 'Shot' and getInfo.isType() == 'shot' :
			cmds.textField("RenderPath_TextFieldGroup", e=True, tx = config['shot']['path'] + getInfo.get_sequence())
			cmds.textField("assetName_TextFieldGroup" , e=True, tx = getInfo.get_shot())

		elif current_option == "Turntable":
			cmds.textField("RenderPath_TextFieldGroup", e=True, tx = config['turntable']['path'])

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
		option 		= cmds.optionMenu("optionMenu_option", q=True, v=True)

		currentDate = datetime.datetime.now().strftime('%Y%m%d')
		currentTime = datetime.datetime.now().strftime('%H%M%S')

		assetRenderPath = os.path.join( renderPath, assetName)
		# version 	= _checkversion(assetRenderPath)
		version 	= "v%04d"%int(cmds.textField("textField_version",q=True, tx=True))

		if renderPath != "" and assetName != "":
			path_to_render = os.path.join( assetRenderPath, version)
			cmds.workspace( rt = ["images", path_to_render])
			cmds.setAttr("defaultRenderGlobals.imageFilePrefix","<Scene>", type = "string")

			if option == "Turntable":
				cmds.setAttr("redshiftOptions.imageFormat",4)

			elif option == "Shot":
				cmds.setAttr("defaultRenderGlobals.enableDefaultLight",0)# enableDefaultLight 0
				cmds.setAttr("defaultResolution.width",1920)			# setAttr "defaultResolution.width" 1920;
				cmds.setAttr("defaultResolution.height",1080) 			# setAttr "defaultResolution.height" 1080;
				cmds.setAttr("defaultResolution.deviceAspectRatio",1.778) 
				cmds.setAttr("defaultResolution.pixelAspect",1)
				cmds.setAttr("redshiftOptions.imageFormat",1)
				cmds.setAttr("redshiftOptions.exrForceMultilayer",1)	# exrForceMultilayer 1
				cmds.setAttr("redshiftOptions.exrMultipart",1) 			# exrMultipart 1
				cmds.setAttr("redshiftOptions.copyToTextureCache",0) 	# copyToTextureCache 0 
				cmds.setAttr("redshiftOptions.primaryGIEngine",4)
				cmds.setAttr("redshiftOptions.secondaryGIEngine",4)
		else :
			cmds.error("Field must not empty")
			return False

		# Result
		logger.info (cmds.workspace( "images",q=True ,fileRuleEntry = True ))

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

def _checkversion(assetRenderPath):
	''' Check version folder '''
	
	# If path not exists return version 1.
	if not os.path.exists(assetRenderPath):
		return '0001'

	# Get max version
	allDir =  [int(d.replace("v", "")) for d in os.listdir(assetRenderPath) if d.startswith('v')]
	allDir.sort()

	# Get max version.
	if len(allDir) > 0 :
		lastversion = max(allDir)
		nextversion = lastversion + 1 

	# If not version exists 1
	else :
		nextversion = 1

	return ("{version:04d}".format(version = nextversion))

def clearUI():

	if cmds.window( _windowsName, q=True, exists = True ):
		cmds.deleteUI(_windowsName)
		clearUI()

if __name__ == '__main__':
	showUI()