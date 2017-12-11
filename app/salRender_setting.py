import maya.cmds as cmds
import datetime, os

_windowsName = "salRenderSetting_window"
defaultRender_path = "P:/smf_project/post_production/output/render/Turntable"

def setRender(*args):
	# Check text field
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

def showUI():
	clearUI()

	cmds.window(_windowsName, title= "Render setting")
	cmds.columnLayout(adj=True)
	cmds.text(l="")
	cmds.text(l="Render path:",align="left")
	cmds.textField("RenderPath_TextFieldGroup", tx=defaultRender_path)

	cmds.text("\nasset Name :",align="left")
	cmds.textField("assetName_TextFieldGroup")
	cmds.text(l="")

	cmds.button(l="set path",c = setRender)
	cmds.showWindow( _windowsName )

	# adjust window size
	cmds.window( _windowsName, e=True, w = 400, h=100 )

def clearUI():

	if cmds.window( _windowsName, q=True, exists = True ):
		cmds.deleteUI(_windowsName)
		clearUI()

if __name__ == '__main__':
	showUI()