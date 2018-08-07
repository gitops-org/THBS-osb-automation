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
osb_file_path = home+'/code/osb/osb.xml'
##############  global variable declaration ################################
global_checkout_path = home+'/code/osb/'
global_json_file_path = home+"/scripts/osb-automation/config.json"
input_proxies_set = set()
######################## To Update build.properties ################

buildProperty_file = home+'/code/osb/build.properties'
bprop = configparser.ConfigParser()
bprop.read(buildProperty_file)
bprop.sections()

# Context Manager to change current directory.
class change_dir:

  def __init__(self, newPath):
    self.newPath = os.path.expanduser(newPath)

  # Change directory with the new path
  def __enter__(self):
    self.savedPath = os.getcwd()
    os.chdir(self.newPath)

  # Return back to previous directory
  def __exit__(self, etype, value, traceback):
    os.chdir(self.savedPath)

###########################  Modify osb.xml #################################

def reloadOSBFile():
	ET.register_namespace('', "http://www.bea.com/alsb/tools/configjar/config")
	tree = ET.parse(osb_file_path)
	root = tree.getroot()
	return root

def add_project_level_node(elem):		
	
	jarfile="$BUILDDIR$/"+"servicename-"+timestamp +".jar"	
	
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('projectLevel', {'includeSystem': 'false'}))		
		actor.attrib['jar']=jarfile
	ElementTree(elem).write(osb_file_path)

def add_resource_node(elem):		
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('resourceLevel'))
	ElementTree(elem).write(osb_file_path)
	
def delete_projectlevel_node(elem):
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		
		for projectLevel in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}projectLevel'):
			actor.remove(projectLevel)
		for resource in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}resourceLevel'):
			actor.remove(resource)
			
	ElementTree(elem).write(osb_file_path)

def validate_node(elem, path):
	for child in elem.getchildren():
		child.append(Element('project', {'dir': path}))
		break		

def delete_node(elem, path):
    for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}source'):
        for project in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}project'):
            actor.remove(project)
            print("Deleting project elem in code/osb/osb.xml")                        
    ElementTree(elem).write(osb_file_path)

def add_project(elem, path):
    for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}source'):
        print("Adding project entry in code/osb/osb.xml")
        actor.append(Element('project', {'dir': path}))
    ElementTree(elem).write(osb_file_path)

############################################################################################

def read_build_resource():
	env = sys.argv[1]	
	with open(global_json_file_path) as jsonfile:
		global_json_data = json.load(jsonfile)	
		
	environment = global_json_data["config"][1]	
	env_flag = False	
	
	index_count = 0
	for i in  range(len(environment["environment"][0]["env"])):
		env_val = environment["environment"][0]["env"][i]		
		if env in env_val:
			env_flag = True
			index_count= i
			break
		else:
			continue
			
	if env_flag:
		global_env = env		
		
	else :
		print("Environment Not Found!")
		sys.exit()	

	global_env_resource_file_path = global_env+'-resource.json'
	with open(global_env_resource_file_path) as jsonfile:
		global_json_data = json.load(jsonfile)		

	resources = global_json_data["resources"]	

	for i in  range(len(resources)):
 
		delta = resources[i]["delta"]
		if delta == 'false':
			rec_path = resources[i]["serviceName"]	
		else:
			rec_path = resources[i]["serviceName"]

		input_proxies_set.add(rec_path)
		#print(rec_path)

	
def invoke_build_script():
	path = "dev-checkout/codebase/AggregateItemsForCharging"
	root = reloadOSBFile()
	delete_node(root,path)
	
	delete_projectlevel_node(root)
	add_project(root,global_checkout_path+path)	
	
	delta = 'false'	

	if delta.lower() == 'true':	
		add_resource_node(root)
	else:	
		add_project_level_node(root)	

	pom_filename = 'osb-pom.xml'
	
	global timestamp
	print("\n5. Invoking Build Script!")	
	print("\nBuild started ...")
	version=timestamp	
	for service in  input_proxies_set:
		
		#print(service)
		artifactId=service	
		bprop['builds']["build-"+timestamp]=artifactId+"-"+version+".jar"			
		with open(buildProperty_file, 'w+') as configfile:
			bprop.write(configfile)
		
		mvn_path = "/home/automation/deploymentAutomation/lib/apache-maven-3.1.1/bin/mvn"
		finalName=artifactId+"-"+version
		try:
		
			deployment_status_code=subprocess.call([mvn_path, "-s", "settings.xml", "-f", "../../"+pom_filename, "package", "-Djar.finalName="+finalName], shell=False, timeout=120)
			if deployment_status_code == 0:		
				print("\nSuccessfully build given Service/s. Returned Status code as : %s"%(deployment_status_code))
			else:
				print("\nError while building the service/s.Returned Status code as : %s"%(deployment_status_code))
				sys.exit()	
		except subprocess.TimeoutExpired:
			print('\nFailed to connect while Deployment. Timed out')

		

#################### init script ############################

try:
	read_build_resource()
	invoke_build_script()
except Exception as exc:
   print("error while reading JSON file", exc)

