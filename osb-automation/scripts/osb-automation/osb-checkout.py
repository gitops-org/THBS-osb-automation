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

##############  global variable declaration ################################
global_checkout_path = home+'/code/osb/'
global_json_file_path = home+"/scripts/osb-automation/config.json"
osb_file_path = home+'/code/osb/osb.xml'
global_env = ""
global_env_resource_file_path = ""
global_scm_url = ""
global_json_data = ""
repositoryName = ''
bitbucketVersionType = ''
bitbucketVersionName = ''
pathToService = ''
serviceName= ''
pathToresource = ''
resourceName = ''
delta= ''
input_proxies_set = set()
output_dependencies_set = set()
output_dependencies_files = set()

######################## To Update global common.properties ################

globalProperty_file = home+'/code/osb/common.properties'
gprop = configparser.ConfigParser()
gprop.read(globalProperty_file)
gprop.sections()


################# Logger Implementation for the OSB automation #############
class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
		
    def flush(self):
        pass

sys.stdout = Logger("automation-log.log")

############################################################################

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
package_name = "AggregateItemsForCharging"
def add_project_level_node(elem):
	
	jarfile="$BUILDDIR$/"+package_name+"-"+timestamp+".jar"
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('projectLevel', {'includeSystem': 'false'}))
		actor.attrib['jar']=jarfile
	ElementTree(elem).write(osb_file_path)

def add_resource_node(elem):
	jarfile="$BUILDDIR$/"+package_name+"-"+timestamp+".jar"
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('resourceLevel'))
		actor.attrib['jar']=jarfile
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


def add_project_dependencies(elem, path,dependencies):
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}source'):
		print("Adding project entry in code/osb/osb.xml")
		for dep in dependencies:
			new_path= path+dep
			actor.append(Element('project', {'dir': new_path}))
	ElementTree(elem).write(osb_file_path)	

#############################################################################
def validate_inputs(args):	
	valStatus= False
	arg_count = len(args)
	if arg_count > 2:
		print("\nInvalid extra arguments!")
		sys.exit()	
	elif arg_count < 2:		
		print("\nError! Missing environment argument!. \nPlease provide environment as another argument. \nExample:- python osb-master-final.py test")
		sys.exit()
	elif arg_count == 2:		
		return True
	else :
		return False

def checkout_resource():
	print("1. Started ...\n")
	global global_checkout_path
	global global_json_file_path
	global global_json_data
	global global_proxypath
	global global_scm_url
	global repositoryName
	global	bitbucketVersionType
	global	bitbucketVersionName
	global	pathToService
	global	serviceName
	global	pathToresource
	global	resourceName
	global global_env_resource_file_path
	global delta
	global global_env
	result = validate_inputs(sys.argv)		
	if result == False:
		sys.exit()
		
	env = sys.argv[1]	
	with open(global_json_file_path) as jsonfile:
		global_json_data = json.load(jsonfile)	
		
	scm = global_json_data["config"][0]["scm"][0]
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
		url=scm["ssh-url"]
		
	else :
		print("Environment Not Found!")
		sys.exit()	

	global_env_resource_file_path = global_env+'-resource.json'
	with open(global_env_resource_file_path) as jsonfile:
		global_json_data = json.load(jsonfile)		

	resources = global_json_data["resources"]
	global_checkout_path = global_checkout_path+global_env+"-checkout"
	print("Services checkout path : "+global_checkout_path)
	
	for i in  range(len(resources)):
 
		delta = resources[i]["delta"]
		
		if delta == 'false':
			proxy_path = resources[i]["pathToService"]+resources[i]["serviceName"]	
		else:
			proxy_path = resources[i]["pathToService"]+resources[i]["serviceName"]+resources[i]["pathToresource"]+resources[i]["resourceName"]

		input_proxies_set.add(proxy_path)	
		repositoryName = resources[i]["repositoryName"]
		pathToService = resources[i]["pathToService"]
		serviceName = resources[i]["serviceName"]
		bitbucketVersionName = resources[i]["bitbucketVersionName"]
		bitbucketVersionType = resources[i]["bitbucketVersionType"]		
		pathToresource = resources[i]["pathToresource"]
		resourceName = resources[i]["resourceName"]
		global_scm_url = url+repositoryName+'.git'		
		
		#global_checkout_path = global_checkout_path+global_env+"-checkout"

		print("\nChecking out from repository  arg1 : "+global_scm_url)
		print("\nChecking out following resource arg2 :"+proxy_path)
		print("\ncheckoutpath  arg3 : "+global_checkout_path)
		print("\nChecking out from repository bitbucketsourceType arg4 : "+bitbucketVersionType)
		print("\nChecking out from repository bitbucketsourceName arg5 : "+bitbucketVersionName)
		print("\ndelta : "+delta)
		print("\npathToresource : "+pathToresource)
		print("\nresourceName : "+resourceName)
		
		path = proxy_path
		
		root = reloadOSBFile()
		delete_node(root,path)
		delete_projectlevel_node(root)
		add_project(root,global_checkout_path+path)		
		if delta.lower() == 'true':
			add_resource_node(root)
		else:	
			add_project_level_node(root)			
		
		call('./servicescheckout.sh '+global_scm_url+' '+path+' '+global_checkout_path+' '+bitbucketVersionType+' '+bitbucketVersionName, shell=True) 
		
	print("\n2 . Checkout completed!\n")
	
	
def read_dependency():
	#print("Reading dependencies ")
	checkoutFolder="dev-checkout"
	pathToService= "codebase"
	serviceName = "AggregateItemsForCharging"
	pathtoResourceDependency = home+"/code/osb/"+checkoutFolder+"/"+pathToService+"/"+serviceName+"/dependencies"
	global output_dependencies_files 
	global output_dependencies_set
	dep = configparser.ConfigParser()
	#print("pathtoResourceDependency :"+pathtoResourceDependency)
	for source_file in os.listdir(pathtoResourceDependency):
		dep_file=source_file
		
		dependencies_file = home+'/code/osb/dev-checkout/codebase/AggregateItemsForCharging/dependencies'+"/"+dep_file
		#output_dependencies_files.add(dependencies_file)
		
		'''
		f = open(dependencies_file)			
		print(dependencies_file)
		refVal=f.read().split(',')		
		#print(len(refVal))
		'''
		
		with open(dependencies_file) as jsonfile:
			dependencies_data = json.load(jsonfile)			
		
		refVal = dependencies_data
		#print(refVal)
		for i in  range(len(refVal)):			
		
			if refVal[i]["dependency"].startswith("Utility"):
				continue
			elif refVal[i]["dependency"].startswith("CommonResources"):
				continue
			elif refVal[i]["dependency"].startswith("NorthBoundInterfaces"):
				continue
			elif refVal[i]["dependency"].startswith("SouthBoundInterfaces"):
				continue
			else:						
				output_dependencies_set.add(refVal[i]["dependency"])
	
	print(output_dependencies_set)
	root = reloadOSBFile()
	##### Only update osb.xml
	add_project_dependencies(root,global_checkout_path,output_dependencies_set)
	
def checkout_dependencies():
	#print("checking out dependencies")		
	bitbucketVersionType = "branch"
	bitbucketVersionName = "dev"
	#print(output_dependencies_set)
	#print("\nChecking out following file arg1 :"+global_scm_url)
	for sd in output_dependencies_set:		
		sd = "IntegrationReleaseOSB/codebase/"+sd
		print("\nChecking out following file arg2 :"+sd)
		call('sparsecheckoutresource.bat '+global_scm_url+' '+sd+" "+global_checkout_path+" "+bitbucketVersionType+" "+bitbucketVersionName, shell=True) 
	
################# init script ####################

try:
	checkout_resource()
	read_dependency()
except Exception as exc:
   print("error while reading JSON file", exc)

