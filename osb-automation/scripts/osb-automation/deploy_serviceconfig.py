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


input_file_path = home+"/scripts/osb-automation/osb-tmp/"



def deploy_configs(args):
	print ("Reading input file ")
	env = args[1]
	service_config_file=input_file_path+env+"/services/"+env+"-service-config.json"
	print("Service config file path :"+service_config_file)
	
	with open(service_config_file) as jsonfile:
		input_data = json.load(jsonfile)
	
	resources=input_data["resources"]
	print("Total count :"+str(len(resources)))

	for i in range(len(resources)):
		config_type = resources[i]["checkout-type"]
		service_name = resources[i]["serviceName"]
		print("Service Name :"+service_name)
		resource_name = resources[i]["resourceName"]
		call('python checkout-config_1_1.py '+service_name,shell=True)
		if config_type=='S':
			print(" Config Type :"+config_type)
			call('./uploadconfig.sh '+config_type+' '+service_name+' '+'NULL'+' '+env,shell=True)			
		elif config_type=='F':
			print(" File config :"+config_type)
			call('./uploadconfig.sh '+config_type+' '+service_name+' '+resource_name+' '+env,shell=True)
		else:
			print("None of mathces..")
		
try:
    deploy_configs(sys.argv)
except Exception as E:
    print("Error in deployment <> ",E)



