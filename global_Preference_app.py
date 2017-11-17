# run global preference app

import os, sys, json

try:
	from PySide2.QtCore import *
	from PySide2.QtGui import *
	from PySide2.QtWidgets import *
	from PySide2.QtUiTools import *
	from PySide2 import __version__

except ImportError:
	from PySide.QtCore import *
	from PySide.QtGui import *
	from PySide.QtUiTools import *
	from PySide import __version__


from app.globalPreference import Global_preference

app  = QApplication(sys.argv) 
form = Global_preference.sal_globalPreference()
app.exec_()