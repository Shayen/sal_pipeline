# Correct Shot
import os
import shutil
import sys

import maya.cmds as cmds

# copy Rs proxy
workspace = cmds.workspace(q=True, rd=True)
data_dir  = workspace + '/data' 

def main():
	# import RsProxy

	__copyRsProxy()

def __copyRsProxy():
	''' copy Rs proxy to data '''

	rs_node = cmds.ls(type="RedshiftProxyMesh")

	for node in rs_node :
		path = cmds.getAttr(node + '.fileName')
		newpath = data_dir + '/' + os.path.basename(path)

		try :
			shutil.copy( path, newpath )
			print( "copy Success : " + os.path.basename(path) )

		except Exception as e :
			print (e)
			continue 

		# set new path
		cmds.setAttr(node + '.fileName', newpath, type = "string")

	print("Copy success")


if __name__ == '__main__':
	main()