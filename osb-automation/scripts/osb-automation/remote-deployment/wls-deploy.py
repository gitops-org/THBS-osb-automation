import os
import os.path
import sys
import configparser
import subprocess
from subprocess import call

def main(args):
	try:
		env=args[1]

		print("Deployment for the env :"+env)

		#call('./remote-conn.sh '+gprop.get('ssh','username')+' '+gprop.get('ssh','host')+' '+gprop.get('ssh','db')+' '+gprop.get('ssh','jms')+' '+gprop.get('ssh','fjms')+' '+gprop.get('ssh','aq')+' '+env, shell=True)

		call('./remote-conn.sh '+env, shell=True)
                
		print("Close SSH connect to target environemnt :"+env)
		
	except:
		print("Failed : Deployment configurations are invalid")
		dumpStack()
				
main(sys.argv)
