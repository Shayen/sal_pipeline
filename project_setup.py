import os, sys, json

project_path = "D:/WORK/Pipeline_projectSetup/post_production"

data_dict = {}

for folder in os.listdir( project_path ):
	print folder