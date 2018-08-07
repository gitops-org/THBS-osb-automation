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
epoch_now = time.time()
timestamp = dt.datetime.utcfromtimestamp(epoch_now).strftime("%Y%m%d%H%M%S")
######## Navigate to home from current working dir #########################
cwd = os.getcwd()
parent=os.path.abspath(os.path.join(cwd, os.pardir))
home=os.path.abspath(os.path.join(parent, os.pardir))
home=home.replace('\\', '/')


def checkout_config(args):
	#inputs	
	env = args[1]
	
	checkout_config_bb_url = "ssh://git@code.airtelworld.in:7999/intosb/"
	checkout_config_repo = "integrationrelease"
	checkout_config_path = "/"+env	
	bitbucket_version_type = "branch"
	bitbucket_version_name = env 
	checkout_env = env	
	
	checkout_path = "/home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp"
	resourcepath = checkout_config_path	
	scm_url = checkout_config_bb_url+checkout_config_repo+".git"	
	print("\n\nscm_url : "+scm_url)
	print("resourcepath :"+resourcepath)
	print("checkout_path :"+checkout_path)
	print("bitbucket_version_type :"+bitbucket_version_type)
	print("bitbucket_version_name :"+bitbucket_version_name)
	
	call('/home/automation/deploymentAutomation/scripts/osb-automation/propscheckout.sh '+scm_url+' '+resourcepath+' '+checkout_path+' '+bitbucket_version_type+' '+bitbucket_version_name,shell=True)	
		
#################### init script ############################
try:
	checkout_config(sys.argv)	
except Exception as exc:
   print("error while init script!", exc)
