# import maya.OpenMaya as om

import os, shutil

# imagePath = "P:/smf_project/production/assets/prop/WoodenTreeB/_thumbnail/smf_prop_WoodenTreeB_model_v001_Nook.jpg"
# newPath = "P:/smf_project/production/assets/prop/WoodenTreeB/_thumbnail/smf_prop_WoodenTreeB_model_v001_Nook_new.jpg"

assetPath = "P:/smf_project/production/assets"
dest_dit  = "P:/tmp/All_thumbnail"

for assetType in os.listdir(assetPath):

	for assetName in os.listdir(assetPath + '/' + assetType) :

		for image in os.listdir(assetPath + '/' + assetType + '/' + assetName + '/_thumbnail'):

			if image.endswith(".jpg") :
				path = (assetPath + '/' + assetType + '/' + assetName + '/_thumbnail/' + image)


				# myImage = om.MImage()
				# myImage.readFromFile(path)
				# myImage.resize(448,252)
				# myImage.writeToFile(path, "jpg")

				shutil.copy2(path, dest_dit+'/'+image)


				print ("copy : " + os.path.basename(path))