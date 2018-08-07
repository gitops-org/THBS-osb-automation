import os
import sys
import configparser
import subprocess
import errno
import stat, shutil
import time
import os.path
import string
import pprint
import json
import random
from shutil import copy2
from shutil import rmtree
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring, ElementTree, Element
from subprocess import Popen
from subprocess import call
from distutils.dir_util import copy_tree
import time
import datetime as dt

cwd = os.getcwd()
parent=os.path.abspath(os.path.join(cwd, os.pardir))
home=os.path.abspath(os.path.join(parent, os.pardir))
home=home.replace('\\', '/')


input_file_path = home+"/osb-automation/osb-tmp/"


def deploy_configs(args):
	print ("Reading input file ")
	env = args[1]
	domain_path=args[2]
	service_config_file=input_file_path+"/service_resources/release/"+env+"-service-config.json"
	print("Service config file path :"+service_config_file)
	
	with open(service_config_file) as jsonfile:
		input_data = json.load(jsonfile)
	
	resources=input_data["resources"]
	print("Total count :"+str(len(resources)))

	for i in range(len(resources)):
		config_type = resources[i]["checkout-type"]
		bb_repo_name = resources[i]["repositoryName"]
		bb_config_path = resources[i]["pathToProject"]
		bb_branch_name = resources[i]["bitbucketVersionName"]
		service_name = resources[i]["serviceName"]		
		service_name1 = bb_config_path+service_name
		print("Service Name :"+service_name)
		resource_name = resources[i]["resourceName"]
		resource_name1=service_name1+'/'+resource_name
		call('python checkout-config_1_1.py '+bb_repo_name+' '+bb_config_path+' '+bb_branch_name+' '+service_name,shell=True)
		if config_type=='S':
			print(" Config Type :"+config_type)
			call('./uploadconfig.sh '+config_type+' '+service_name1+' '+'NULL'+' '+env+' '+domain_path,shell=True)			
		elif config_type=='F':
			print(" File config :"+config_type)
			call('./uploadconfig.sh '+config_type+' '+resource_name1+' '+service_name+' '+env+' '+domain_path,shell=True)
		else:
			print("None of mathces..")
		
try:
    deploy_configs(sys.argv)
except Exception as E:
    print("Error in deployment <> ",E)





