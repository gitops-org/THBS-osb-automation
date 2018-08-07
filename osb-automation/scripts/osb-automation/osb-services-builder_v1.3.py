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
timestamp = dt.datetime.utcfromtimestamp(epoch_now).strftime("%Y%m%d%H%M%S%f")
######## Navigate to home from current working dir #########################
cwd = os.getcwd()
parent=os.path.abspath(os.path.join(cwd, os.pardir))
home=os.path.abspath(os.path.join(parent, os.pardir))
home=home.replace('\\', '/')

osb_common_input_file_path = home+"/scripts/osb-automation/osb-tmp/"
osb_file_path = home+'/code/osb/osb-services/osb.xml'

############################################################################
##########Checkout related global variables
############################################################################
checkout_input_file_path=''
checkout_url=''
checkout_env=''
checkout_from_type=''
checkout_from_name=''
checkout_repo=''
checkout_dir_path=''
checkout_type=''
checkout_url_set = set()
check_dependencies = False
output_dependencies_set = set()
############################################################################

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
###########################################################################

def validate_inputs(args):	
	print("1. Validating inputs\n")	
	valStatus= False
	arg_count = len(args)
	if arg_count > 2:
		print("\nInvalid extra arguments!")
		sys.exit()	
	elif arg_count < 2:		
		print("\nError! Missing environment argument!. \nPlease provide environment as another argument. \nExample:- python osb-master-final.py test")
		sys.exit()
	elif arg_count == 2:	
		print("Valid arguments. Continuing.")
		return True
	else :
		return False

############################################################################
###########################  Modify osb.xml #################################

def reloadOSBFile():
	ET.register_namespace('', "http://www.bea.com/alsb/tools/configjar/config")
	tree = ET.parse(osb_file_path)
	root = tree.getroot()
	return root
	
def add_project_level_node(elem,package_name):
	timestamp = dt.datetime.utcfromtimestamp(epoch_now).strftime("%Y%m%d")
	uniqueString = str(int(time.time()))
	jarfile="$BUILDDIR$/$ARTIFACTID$-$VERSION$"+"-"+timestamp+uniqueString+".jar"
	print("jar file :"+jarfile)
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('projectLevel', {'includeSystem': 'false'}))
		actor.attrib['jar']=jarfile
	ElementTree(elem).write(osb_file_path)
	return timestamp+uniqueString

def add_resource_node(elem,package_name):
	timestamp = dt.datetime.utcfromtimestamp(epoch_now).strftime("%Y%m%d%H%M%S")
	uniqueString = str(int(time.time()))
	jarfile="$BUILDDIR$/$ARTIFACTID$-$VERSION$"+"-"+timestamp+uniqueString+".jar"
	print("jar file :"+jarfile)
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('resourceLevel'))
		actor.attrib['jar']=jarfile
	ElementTree(elem).write(osb_file_path)
	return timestamp+uniqueString
	
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
	
def update_dependency(elem, update_for):
	if update_for == "D":
		print("update dependency for delta :")
	elif update_for == "S":
		print("update dependency for service")
	else :
		print("update dependency for project")
	
	
def add_project_dependencies_as_resource_level(elem, path,dependencies):
	print("inside add_project_dependencies_as_resource_level : ")
	
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		for actor1 in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}resourceLevel'):			
			for actor2 in actor1.findall('{http://www.bea.com/alsb/tools/configjar/config}resources'):
				for actor3 in actor2.findall('{http://www.bea.com/alsb/tools/configjar/config}include'):					
					actor2.remove(actor3)				
	ElementTree(elem).write(osb_file_path)
	
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):		
		for actor1 in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}resourceLevel'):
			if actor1.find('{http://www.bea.com/alsb/tools/configjar/config}resources') == None:
				actor1.append(Element('resources'))
				print("Added resources tag  in osb.xml ")
	ElementTree(elem).write(osb_file_path)
	elem = reloadOSBFile()
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		for actor1 in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}resourceLevel'):
			for actor2 in actor1.findall('{http://www.bea.com/alsb/tools/configjar/config}resources'):
				#print(actor2)
				#print("Adding resource level entry in code/osb/osb.xml")
				#print("path : "+path)		
				for dep in dependencies:
					#new_path= path+"/"+dep.replace('\\', '/')
					new_path= dep.replace('\\', '/')
					#print("reading dep : "+new_path)
					actor2.append(Element('include', {'name': new_path}))			
	ElementTree(elem).write(osb_file_path)

def checkout(args):	

	print("Reading Inputs ...")
	print("Checkout Inputs... : ")
	global checkout_url
	global checkout_env
	global checkout_from_type
	global checkout_from_name
	global checkout_repo
	global checkout_dir_path
	global checkout_type
	global checkout_url_set
	global check_dependencies
	global osb_common_input_file_path
	global timestamp
	env = args[1]
	osb_common_input_file = env+"-service-input.json"
	osb_common_input_file_path = osb_common_input_file_path+"/service_resources/release/"+osb_common_input_file
	print("config file : "+osb_common_input_file_path)
	
	with open(osb_common_input_file_path) as jsonfile:
		osb_common_input_data = json.load(jsonfile)
		
	#print(osb_common_input_data)
	
	scm_data = osb_common_input_data["config"][0]["scm"][0]	
	checkout_url = scm_data["ssh-url"]
	#print(checkout_url)
	
	custimization_data = osb_common_input_data["config"][1]["custom"]	
	checkout_dir_path = custimization_data["checkout_dir_path"]
	#checkout_env = custimization_data["env"]
	checkout_env = args[1]
	#print(checkout_dir_path)
		
	resource_data = osb_common_input_data["config"][2]["resources"]	
	i=1
	for i in range(len(resource_data)):
		scm_url = ""
		checkout_path = ""
		deltapath = ""
		checkout_type = resource_data[i]["checkout-type"]
		scm_project = resource_data[i]["scm-project"]
		repository_name = resource_data[i]["repositoryName"]
		bitbucket_version_type = resource_data[i]["bitbucketVersionType"]
		bitbucket_version_name = resource_data[i]["bitbucketVersionName"]
		path_to_project = resource_data[i]["pathToProject"]
		project_name = resource_data[i]["projectName"]		
		path_to_service = resource_data[i]["pathToService"]
		service_name = resource_data[i]["serviceName"]
		path_to_resource = resource_data[i]["pathToresource"]
		resource_name = resource_data[i]["resourceName"]		

		if checkout_type == 'P':
			resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]
		elif checkout_type == 'S':
			#For dependency checkout we need to checkout entire project to find dependency folder and dependencies files entries should be added to osb.xml
			
			resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]
			dependency_path = resourcepath
			
		else:
			resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]+resource_data[i]["pathToService"]+resource_data[i]["serviceName"]+resource_data[i]["pathToresource"]+resource_data[i]["resourceName"]
			deltapath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]
		
		scm_url = checkout_url+scm_project+repository_name+'.git'
		checkout_path = home+checkout_dir_path+checkout_env+"-checkout"		
		build_name=project_name
		build_number=""
		
		print("\n\nChecking out from repository  arg1 : "+scm_url)
		print("\nChecking out following resource arg2 :"+resourcepath)
		print("\ncheckoutpath  arg3 : "+checkout_path)
		print("\nChecking out from repository bitbucketsourceType arg4 : "+bitbucket_version_type)
		print("\nChecking out from repository bitbucketsourceName arg5 : "+bitbucket_version_name)		
		
		#########################################################
		path = resourcepath
		if deltapath != '':
			path=deltapath

		root = reloadOSBFile()
		delete_node(root,path)
		delete_projectlevel_node(root)
		add_project(root,checkout_path+path)	
		
		#########################################################
		package_name = ""
		if checkout_type == 'P':
			update_dependency(root,checkout_type)
			print("\nGoing with project Checkout")
			package_name=resource_data[i]["projectName"]
			build_number=add_project_level_node(root,package_name)
			check_dependencies = False
		elif checkout_type == 'S':
			update_dependency(root,checkout_type)
			package_name=resource_data[i]["serviceName"]
			build_name=package_name
			#Services are treated as resource level only so updating resource node instead of projectLevel
			build_number=add_resource_node(root,package_name)
			print("\nGoing with Service Checkout")
			check_dependencies = True
		else:
			update_dependency(root,checkout_type)
			package_name=resource_data[i]["serviceName"]
			print("\nGoing with Delta Checkout")
			build_number=add_resource_node(root,package_name)
			check_dependencies = False

		call('./servicescheckout.sh '+scm_url+' '+resourcepath+' '+checkout_path+' '+bitbucket_version_type+' '+bitbucket_version_name,shell=True)

		if check_dependencies:
                        parent_project = resource_data[i]["projectName"]
                        #Reading dependency for Service of a project, if any
                        read_dependency(parent_project,checkout_env,package_name,path_to_project)

		checkout_env = checkout_env
		print("Buiild  :"+build_number)
		branch_name = checkout_env
		call('./osb-build.sh ',shell=True)
		call('./upload.sh '+build_number+' '+build_name+' '+checkout_env,shell=True)	

def read_dependency(parent_project,bitbucket_version_name,package_name,path_to_project):
	
	pathtoResourceDependency = home+"/code/osb/"+bitbucket_version_name+"-checkout"+path_to_project+parent_project+"/dependencies"
	servicepath=  parent_project+"/proxyservices/"+package_name+"/*.proxy"
	global output_dependencies_files 
	global output_dependencies_set
	serviceName=package_name
	
	#for source_file in os.listdir(pathtoResourceDependency):		
	dep_file="Dep_"+serviceName+".json"
	print("Dep File : "+dep_file)
	print("Service path :"+servicepath)
	dependencies_file = pathtoResourceDependency+"/"+dep_file
	with open(dependencies_file) as jsonfile:
		dependencies_data = json.load(jsonfile)
		refVal = dependencies_data
		output_dependencies_set.add(servicepath)
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
				resc_dep = refVal[i]["dependency"].replace('\\', '/')
				#print(i)
				#print("resc_dep :"+resc_dep)
				if resc_dep == "":
					continue
				else:
					output_dependencies_set.add(resc_dep)
	
	root = reloadOSBFile()
	##### Only update osb.xml
	add_project_dependencies_as_resource_level(root,checkout_dir_path,output_dependencies_set)
	
	
def init(args):
	print("Started ...")	
	try:
		result = validate_inputs(args)
		if result:
			print("\n3. Validation Success")
			checkout(sys.argv)
		else:
			sys.exit()		
	except Exception as exc:
	   print("error while validating", exc) 
	
	
#################### init script ############################

try:
	init(sys.argv)
except Exception as exc:
   print("error while init script!", exc)

