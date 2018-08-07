import os
import sys
import configparser
import subprocess
import errno
import stat, shutil
import time
import os.path
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
import base64

######## Navigate to home from current working dir #########################
cwd = os.getcwd()
parent=os.path.abspath(os.path.join(cwd, os.pardir))
home=os.path.abspath(os.path.join(parent, os.pardir))
home=home.replace('\\', '/')

global_json_file_path = ""
##### Properties files path
#propertiesfile_checkoutpath=home+'/scripts/osb-automation/osb-tmp/'
#propertiesfile_bitbucketpath=""
global_env = ""

######################## To Update global common.properties ################

globalProperty_file = home+'/code/osb/common.properties'
gprop = configparser.ConfigParser()
gprop.read(globalProperty_file)
gprop.sections()




#############################################################################
def validate_inputs(args):	
	valStatus= False
	arg_count = len(args)
	if arg_count > 2:
		print("\nInvalid extra arguments!")
		sys.exit()	
	elif arg_count < 2:		
		print("\nError! Missing environment argument!. \nPlease provide environment as another argument. \n")
		sys.exit()
	elif arg_count == 2:		
		return True
	else :
		return False

def read_config():

	global global_env
	global propertiesfile_bitbucketpath
	global global_json_file_path
	
	result = validate_inputs(sys.argv)		
	if result == False:
		sys.exit()
		
	env = sys.argv[1]
	global_json_file_path = home+"/scripts/osb-automation/osb-tmp/env_details/cust_config.json"	
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
	else :
		print("Environment Not Found!")
		sys.exit()	

	

def wls_build():
	read_config()
	invoke_deployment_script()

	
def invoke_deployment_script():
	pom_filename = 'osb-pom.xml'
	
	print("\n5. Invoking Deployment Script!")	
	print("\nDeployment started ...")
	
	with open(global_json_file_path) as jsonfile:
		json_data = json.load(jsonfile)	
	common_json = json_data["config"][2]["common"][0]	
	env_json = json_data["config"][1]["environment"][0]["env"]		
	index_count = 0	
	for i in  range(len(env_json)):
		env_val = env_json[i]		
		if global_env in env_val:			
			env_flag = True
			index_count= i
			break
		else:			
			continue
	
	domain_name =env_json[index_count][global_env][0]["domain-name"]
	admin_url = env_json[index_count][global_env][0]["admin-url"]	
	admin_username = env_json[index_count][global_env][0]["admin-userName"]	
	admin_password = env_json[index_count][global_env][0]["admin-password"]	
	admin_password = base64.b64decode(admin_password).decode("utf-8", "ignore") 
	
	configjar = common_json["skip-configjar"]	
	skip_customization = common_json["skip-customization"]	
	import_val = common_json["skip-import"]	
	jdbc = common_json["skip-jdbc"]	
	jms = common_json["skip-jms"]	
	aq = common_json["skip-aq"]
	
	gprop['common']['domain.name']=domain_name
	gprop['common']['admin_url']=admin_url
	gprop['common']['admin_username']=admin_username
	gprop['common']['admin_password']=admin_password
	gprop['common']['configjar']=configjar
	gprop['common']['customization']=skip_customization
	gprop['common']['import']=import_val
	gprop['common']['jdbc']=jdbc
	gprop['common']['jms']=jms
	gprop['common']['aq']=aq
	gprop['common']['env']=global_env
	
	with open(globalProperty_file, 'w+') as configfile:
		gprop.write(configfile)
	
	print("\nEnvironment details found ...\n")
	print('\ndomain_name:\t'+domain_name)
	print('\nadmin_url:\t'+admin_url)
	print('\nconfigjar:\t'+configjar)
	print('\nskip_customization:\t'+skip_customization)
	print('\nimport_val:\t'+import_val)
	print('\njdbc:\t'+jdbc)
	print('\njms:\t'+jms)
	print('\naq:\t'+aq)
	print('\nglobal_env:\t'+global_env)	
	
	mvn_path = "/home/automation/deploymentAutomation/lib/apache-maven-3.1.1/bin/mvn"

	try:
	
		deployment_status_code=subprocess.call([mvn_path, "-s", "settings.xml", "-f", "../../"+pom_filename, "deploy"], shell=False, timeout=120)
		if deployment_status_code == 0:		
			print("\nSuccessfully deployed given Service/s. Returned Status code as : %s"%(deployment_status_code))
		else:
			print("\nError while deploying the service/s.Returned Status code as : %s"%(deployment_status_code))
			sys.exit()	
	except subprocess.TimeoutExpired:
		print('\nFailed to connect while Deployment. Timed out')
	
	

#################### init script ############################

try:
	wls_build()
except Exception as exc:
   print("error while reading JSON file", exc)

