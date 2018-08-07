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
	
#package_name = "AggregateItemsForCharging"
def add_project_level_node(elem,package_name):
	
	#jarfile="$BUILDDIR$/"+package_name+"-"+timestamp+".jar"
	jarfile="$BUILDDIR$/$ARTIFACTID$-$VERSION$"+"-"+timestamp+".jar"
	for actor in elem.findall('{http://www.bea.com/alsb/tools/configjar/config}configjar'):
		actor.append(Element('projectLevel', {'includeSystem': 'false'}))
		actor.attrib['jar']=jarfile
	ElementTree(elem).write(osb_file_path)

def add_resource_node(elem,package_name):
	#jarfile="$BUILDDIR$/"+package_name+"-"+timestamp+".jar"
	jarfile="$BUILDDIR$/$ARTIFACTID$-$VERSION$"+"-"+timestamp+".jar"
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
		#print(actor)
		for actor1 in actor.findall('{http://www.bea.com/alsb/tools/configjar/config}resourceLevel'):
			#print(actor1)
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

	env = args[1]
	osb_common_input_file = env+"-service-input.json"
	osb_common_input_file_path = osb_common_input_file_path+env+"/services/"+osb_common_input_file
	
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
	for i in  range(len(resource_data)):
		scm_url = ""
		checkout_path = ""
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
		'''
		print("\n\n"+checkout_type)
		print(scm_project)
		print(repository_name)
		print(bitbucket_version_type)
		print(bitbucket_version_name)
		print(pathToProject)
		print(projectName)
		print(path_to_service)
		print(service_name)
		print(path_to_resource)
		print(resource_name)
		'''				
		if checkout_type == 'P':
			resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]
		elif checkout_type == 'S':
			#resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]+resource_data[i]["pathToService"]+resource_data[i]["serviceName"]
			#For dependency checkout we need to checkout entire project to find dependency folder and dependencies files entries should be added to osb.xml
			
			resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]
			dependency_path = resourcepath
			
		else:
			resourcepath=resource_data[i]["pathToProject"]+resource_data[i]["projectName"]+resource_data[i]["pathToService"]+resource_data[i]["serviceName"]+resource_data[i]["pathToresource"]+resource_data[i]["resourceName"]
		
		scm_url = checkout_url+scm_project+repository_name+'.git'
		checkout_path = home+checkout_dir_path+checkout_env+"-checkout"			
		
		print("\n\nChecking out from repository  arg1 : "+scm_url)
		print("\nChecking out following resource arg2 :"+resourcepath)
		print("\ncheckoutpath  arg3 : "+checkout_path)
		print("\nChecking out from repository bitbucketsourceType arg4 : "+bitbucket_version_type)
		print("\nChecking out from repository bitbucketsourceName arg5 : "+bitbucket_version_name)		
		
		#########################################################
		path = resourcepath
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
			add_project_level_node(root,package_name)
			check_dependencies = False
		elif checkout_type == 'S':
			update_dependency(root,checkout_type)
			package_name=resource_data[i]["serviceName"]
			#Services are treated as resource level only so updating resource node instead of projectLevel
			add_resource_node(root,package_name)
			print("\nGoing with Service Checkout")
			check_dependencies = True
		else:
			update_dependency(root,checkout_type)
			package_name=resource_data[i]["serviceName"]
			print("\nGoing with Delta Checkout")
			add_resource_node(root,package_name)
			check_dependencies = False

		call('./servicescheckout.sh '+scm_url+' '+resourcepath+' '+checkout_path+' '+bitbucket_version_type+' '+bitbucket_version_name,shell=True)
		call('./osb-build.sh ',shell=True)
		
		if check_dependencies:
			parent_project = resource_data[i]["projectName"]
			#Reading dependency for Service of a project, if any
			read_dependency(parent_project,checkout_env)
		

def read_dependency(parent_project,bitbucket_version_name):
	
	pathtoResourceDependency = home+"/code/osb/"+bitbucket_version_name+"-checkout/codebase/"+parent_project+"/dependencies"

	global output_dependencies_files 
	global output_dependencies_set
	dep = configparser.ConfigParser()	
	
	for source_file in os.listdir(pathtoResourceDependency):		
		dep_file=source_file		
		dependencies_file = pathtoResourceDependency+"/"+dep_file
		with open(dependencies_file) as jsonfile:
			dependencies_data = json.load(jsonfile)
		
		refVal = dependencies_data
		
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
	
	#############   Checkout if there is external dependencies	
	for ext_dep in output_dependencies_set :
		#print(ext_dep)
		if ext_dep.startswith(parent_project):			
			continue		
		else:
			print(ext_dep)
			print("Now checkout dependencies")
			#checkout_dependencies()
	
'''	
def checkout_dependencies():

	
	#scm_url = "http://rajesha_thammaiah@code.airtelworld.in:7990/bitbucket/scm/"
	repository_name = "IntegrationReleaseOSB"
	scm_project = "AggregateItemsForCharging"
	checkout_env = "Dev"
	checkout_dir_path = "/code/osb/"
	scm_url = "http://rajesha_thammaiah@code.airtelworld.in:7990/bitbucket/scm/"+"/"+repository_name+"/"+scm_project+'.git'
	checkout_path = home+checkout_dir_path+checkout_env+"-checkout"	
	
	#print("checking out dependencies")		
	bitbucketVersionType = "branch"
	bitbucketVersionName = "Dev"
	#print(output_dependencies_set)
	#print("\nChecking out following file arg1 :"+global_scm_url)
	
	#AggregateItemsForCharging/businessservices/BH_ACC_LOC_BY_ACC_ID_NMS_db.biz
	scm_url = "http://rajesha_thammaiah@code.airtelworld.in:7990/bitbucket/scm/intosb/integrationreleaseosb.git"
	for sd in output_dependencies_set:		
		sd = "IntegrationReleaseOSB/codebase/"+"AggregateItemsForCharging/businessservices/BH_ACC_LOC_BY_ACC_ID_NMS_db.biz"
		sd= sd.replace('\\', '/')
		print("\nChecking out following file arg2 :"+sd)		
		call('checkout.bat '+scm_url+' '+sd+" "+checkout_path+" "+bitbucketVersionType+" "+bitbucketVersionName, shell=True) 
'''
def init(args):
	print("Started ...")	
	try:
		result = validate_inputs(args)
		if result:
			print("\n3. Validation Success")
			checkout(sys.argv)
			#read_dependency("AggregateItemsForCharging","Dev")
		else:
			sys.exit()		
	except Exception as exc:
	   print("error while validating", exc) 
	
	
#################### init script ############################

try:
	init(sys.argv)
except Exception as exc:
   print("error while init script!", exc)
