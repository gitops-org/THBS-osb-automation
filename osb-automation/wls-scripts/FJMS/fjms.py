#!/usr/bin/python
from java.util import Properties
from java import io
from java.io import FileInputStream
from java.io import File
from java.lang import Exception
from java.lang import Throwable
import os.path
import os
import sys

def createFlstrdir(targetManageServerIP,un,pwd,dir_name):
	print("in filestor")
	os.system('sshpass -p '+pwd+' ssh '+un+'@'+targetManageServerIP+' python < /home/oracle/automation/FSC/create_dir.py - '+ dir_name)
	print("out filestor")

def createFlstr(fstr_name,dir_name,target_name):

	cd('/')
	cmo.createFileStore(fstr_name)
	print "filestore :"+fstr_name
	cd('/FileStores/'+fstr_name)
	print "Directory name : "+dir_name
	cmo.setDirectory(dir_name)
	print "target_name:"+target_name
	#set('Targets',jarray.array([ObjectName('com.bea:Name='+target_name+',Type=Cluster')], ObjectName))
	set('Targets',jarray.array([ObjectName('com.bea:Name='+target_name+',Type=Server')], ObjectName))
	print "@@@ created JMS Filestore ..."+fstr_name
	
 
def createJMSsrvr(jms_srv_name,target_name,persis_store,page_dir,thrs_high,thrs_low,msg_size):
        print "Inside createJMSsrvr "
        cd('/')
        srvr = create(jms_srv_name, "JMSServer")
        cd('/Deployments/'+jms_srv_name)
        srvr.setPersistentStore(getMBean('/FileStores/'+persis_store))
        srvr.setPagingDirectory(page_dir)
        srvr.addTarget(getMBean("/Servers/"+target_name))
        srvr.setBytesThresholdLow(long(thrs_low))
        srvr.setBytesThresholdHigh(long(thrs_high))
        srvr.setMaximumMessageSize(long(msg_size))
        print"@@@ Created JMS Server"
		
def getJMSModule(jms_mod_name,allJMSResources):
	print "in getJMSModule mode"
	for jmsResource in allJMSResources:
		JM_Mod = str(jmsResource.getName())	
		print ("in jms mode"+JM_Mod)
		if JM_Mod == jms_mod_name:
			print ("in jms mode"+JM_Mod)
			return False
	return True
	
		
		
def createJMSModule(jms_mod_name,targetms,jms_sub_mod_name,jms_srv_name,total_servers):
		# Build JMS Module - target preferrable cluster
		cd('/')
		cmo.createJMSSystemResource(jms_mod_name)
		print("jms_mod_name : "+jms_mod_name)
		cd('/SystemResources/'+jms_mod_name)
		#targets_ms=configProps.get("total_servers")
		list=[]
		M=1
		while(M <= int(total_servers)):
			#trg_sr=configProps.get("jms_targetManageServerName"+ str(target))
			print"in jms mode"
			s='com.bea:Name='+targetms+str(M)+',Type=Server'
			print("targets :"+s)
                        list.append(ObjectName(str(s)))
			M=M+1
		set('Targets',jarray.array(list, ObjectName))
		#set('Targets',jarray.array([ObjectName('com.bea:Name='+targetms+',Type=Server')], ObjectName))
		print "@@@ created JMS module ..."

		# Create and configure JMS Subdeployment for this JMS System Module 
		cmo.createSubDeployment(jms_sub_mod_name)
		cd('SubDeployments')
		#print("jms_queue_target : "+jms_queue_target)	
		cd(jms_sub_mod_name)
		list=[]
		N=1
		while(N <= int(total_servers)):
			print "in jms sub"
			print jms_srv_name
			s='com.bea:Name='+jms_srv_name+str(N)+',Type=JMSServer'
			print("targets :"+s)
                        list.append(ObjectName(str(s)))
			N=N+1
		set('Targets',jarray.array(list, ObjectName))
		print "@@@ created JMS subdeployment..."
		
def getJMSModulePath(jms_module_name):
        jms_module_path = "/JMSSystemResources/"+jms_module_name+"/JMSResource/"+jms_module_name
        return jms_module_path		
		
def createJMSFS(jms_mod_name,jms_sub_mod_name,jms_fsr_name,jms_cnfurl,jms_initialContextFactory,jms_Credential,total_pro):
		print "inside createJMSFS"
		jms_module_path = getJMSModulePath(jms_mod_name)
		cd(jms_module_path)
		cmo.createForeignServer(jms_fsr_name)
		cd(jms_module_path+'/ForeignServers/'+jms_fsr_name)
		cmo.setInitialContextFactory(jms_initialContextFactory)
		cmo.setConnectionURL(jms_cnfurl)
		cmo.setDefaultTargetingEnabled(bool("true"))
		cmo.unSet('JNDIPropertiesCredentialEncrypted')
		cmo.setJNDIPropertiesCredential(jms_Credential)
		cmo.setDefaultTargetingEnabled(false)
		cmo.setSubDeploymentName(jms_sub_mod_name)
		
def createJNDIPro(jms_mod_name,jms_fsr_name,pro_n,pro_v):
		print "inside createJNDIPro"
		jms_module_path = getJMSModulePath(jms_mod_name)
		print "jms_module_path :"+jms_module_path
		cd(jms_module_path+'/ForeignServers/'+jms_fsr_name)
		cmo.createJNDIProperty(pro_n)
		jms_fs_path = getFSpath(jms_mod_name,jms_fsr_name)
		cd(jms_fs_path+'/JNDIProperties/'+pro_n)
		cmo.setValue(pro_v)
		
		
def createFSConnectionFactory(jms_mod_name,jms_fsr_name,jms_fconf_name,fconf_ljndi,fconf_rjndi):
		print "inside createFSconf"
		jms_fs_path = getFSpath(jms_mod_name,jms_fsr_name)
		cd(jms_fs_path)
		cmo.createForeignConnectionFactory(jms_fconf_name)
		cd(jms_fs_path+'/ForeignConnectionFactories/'+jms_fconf_name)
		cmo.setLocalJNDIName(fconf_ljndi)
		cmo.setRemoteJNDIName(fconf_rjndi)

def getFSpath(jms_module_name,jms_fs_name):
		print "inside getFSpath"
		jms_module_path = getJMSModulePath(jms_module_name)
		print "jms_module_path"+jms_module_path
		jms_fs_path = jms_module_path+'/ForeignServers/'+jms_fs_name
		print "FS Path :"+jms_fs_path
		return jms_fs_path

def createFSdest(jms_module_name,jms_fs_name,jms_dest_name,ljndi,rjndi):
		print "inside createFSdest :"+jms_module_name+jms_fs_name
		cd('/')
		jms_fs_path = getFSpath(jms_module_name,jms_fs_name)
		cd(jms_fs_path)
		print jms_fs_path
		cmo.createForeignDestination(jms_dest_name)
		jms_fs_path=jms_fs_path+'/ForeignDestinations/'+jms_dest_name
		print jms_fs_path
		cd(jms_fs_path)
		cmo.setLocalJNDIName(ljndi)
		cmo.setRemoteJNDIName(rjndi)


#-------------------------------------------------------------------------------------------------------- 

def getProperties(file):
	try:
		property = FileInputStream(file)
		properties = Properties()
		properties.load(property)
	except:
		print("props file is invalid "+file)
		dumpStack()
		sys.exit(0)
	return properties

def validate_inputs(args):
        print("1. Validating inputs\n")
        valStatus= False
        arg_count = len(args)-1
        if arg_count > 4:
                print("\nInvalid extra arguments! :"+str(arg_count))
                sys.exit()
        elif arg_count < 4:
                print("\nError! Missing environment argument!. \nPlease provide environment as another argument. \nExample:- python osb-master-final.py test")
                sys.exit()
        elif arg_count == 4:
                print("Valid arguments. Continuing.")
                return True
        else :
                return False

def main(args):
  #
  # generate a unique string to use in the names
  #
	validate_inputs(args)
        propfile=args[1]
        wls_username=args[2]
        wls_password=args[3]
        url=args[4]

        #wls_username = 'wlsdeploy'
        #wls_password = 'wlsdeploy@123'
        #url = 't3://10.5.213.83:7001'
	try:
		print('--> Load properties..........')
		configProps=getProperties("/home/oracle/automation/FJMS/fsjms.property");
		connect(wls_username,wls_password,url)
		 
		edit()
		startEdit()

		print "#=============# JMS SERVER and PERSISITENT STORE CONFIGURATION #=============#"

		#total_jdest=configProps.get("total_jdest")
		total_servers=configProps.get("total_servers")
		total_jmsmn=configProps.get("total_jmsmodules")
		#total_conf=configProps.get("total_conf")
		#total_pro=configProps.get("total_pro")
		#total_fser=configProps.get("total_fser")
		
		
		#print("Total dest: "+total_jdest)
		print("Total Server : "+total_servers)
		print("Total J M : "+total_jmsmn)

		allJMSResources = cmo.getJMSSystemResources()
		
		a=1
		while(a <= int(total_jmsmn)):
				var1=int(a)
				jms_mod_name=configProps.get("jms_mod_name"+ str(var1))
				jms_sub_m=(jms_mod_name+'.jms_sub_mod_name')
				jms_sub_mod_name=configProps.get(jms_sub_m)
				JM = getJMSModule(jms_mod_name,allJMSResources)
				if JM == True:
					print("JMS MOD creation :"+jms_mod_name)
					jms_srv_n=(jms_mod_name+'.jms_srvr_name')
					jms_srv_name=configProps.get(jms_srv_n)
					jms_per_st=(jms_mod_name+'.jms_srvr_persis_store_name')
					jms_page_dir1=(jms_mod_name+'.jms_srvr_pag_dir1')
					jms_page_dir2=(jms_mod_name+'.jms_srvr_pag_dir2')
					thr_high=(jms_mod_name+'.jms_srvr_by_threshold_high')
					thr_low=(jms_mod_name+'.jms_srvr_by_threshold_low')
					mssg_size=(jms_mod_name+'.jms_srvr_max_msg_size')
					targetms=configProps.get("jms_targetManageServerName")
					print("SUB Module creation" + jms_sub_mod_name + str(var1))
					i=1
					while(i <= int(total_servers)):
						persis_store=configProps.get(jms_per_st)
						page_dir1=configProps.get(jms_page_dir1)
						page_dir2=configProps.get(jms_page_dir2)
						page_dir=(page_dir1+targetms+str(i)+page_dir2)
						thrs_high=configProps.get(thr_high)
						thrs_low=configProps.get(thr_low)
						msg_size=configProps.get(mssg_size)
						ManageServerIP=configProps.get("targetserver"+str(i))
						targetManageServerIP = ManageServerIP.split(",")
						print("page_dir"+page_dir)
						createFlstrdir(targetManageServerIP[0],targetManageServerIP[1],targetManageServerIP[2],page_dir)
						print("ddssssss")
						createFlstr(persis_store+str(i),page_dir,targetms+str(i))
						createJMSsrvr(jms_srv_name+str(i),targetms+str(i),persis_store+str(i),page_dir,thrs_high,thrs_low,msg_size)
						i = i + 1						
					createJMSModule(jms_mod_name,targetms,jms_sub_mod_name,jms_srv_name,total_servers)
				
				total_fser=configProps.get(jms_mod_name+'.foreignserver')
				fsr_name=(jms_mod_name+'.fs_name')
				jms_curl=(jms_mod_name+'.cnfurl')
				ini_cont=(jms_mod_name+'.initialContextFactory')
				Cred=(jms_mod_name+'.credentials')

				l=1
				while(l <= int(total_fser)):
					jms_fsr_name = configProps.get(fsr_name+str(l))
					jms_cnfurl = configProps.get(jms_curl+str(l))
					jms_initialContextFactory = configProps.get(ini_cont+str(l))
					jms_Credential = configProps.get(Cred+str(l))
					total_pro = configProps.get(jms_mod_name+'.'+jms_fsr_name+'.jndiproperties')
					total_jdest = configProps.get(jms_mod_name+'.'+jms_fsr_name+'.destination')
					total_conf = configProps.get(jms_mod_name+'.'+jms_fsr_name+'.connectionfactory')
					createJMSFS(jms_mod_name,jms_sub_mod_name,jms_fsr_name,jms_cnfurl,jms_initialContextFactory,jms_Credential,total_pro)
					p=1
					while(p <= int(total_pro)):
						pro_n = (jms_mod_name+'.prop_'+jms_fsr_name+str(p))
						pro_v = configProps.get(pro_n)
						pro_s = pro_v.split(":")
						createJNDIPro(jms_mod_name,jms_fsr_name,pro_s[0],pro_s[1])
						p=p+1
											

					jms_d_name=(jms_mod_name+'.'+jms_fsr_name+'.destname')
					jms_lj_name=(jms_mod_name+'.'+jms_fsr_name+'.dest_ljndi')
					jms_rj_name=(jms_mod_name+'.'+jms_fsr_name+'.dest_rjndi')

					j=1
					print("JMS DEST :"+total_jdest)
					while(j <= int(total_jdest)):
						print("JMSDEST :"+jms_d_name+jms_lj_name)
						jms_dest_name = configProps.get(jms_d_name+str(j))
						print(jms_dest_name)
						jms_ljndi_name = configProps.get(jms_lj_name+str(j))
						jms_rjndi_name = configProps.get(jms_rj_name+str(j))
						createFSdest(jms_mod_name,jms_fsr_name,jms_dest_name,jms_ljndi_name,jms_rjndi_name)
						j = j + 1
				
					fcnf_name=(jms_mod_name+'.'+jms_fsr_name+'.fconf_name')
					fcnf_ljndi1=(jms_mod_name+'.'+jms_fsr_name+'.fconf_ljndi')
					fcnf_rjndi1=(jms_mod_name+'.'+jms_fsr_name+'.fconf_rjndi')
					#fcnf_UN=(jms_mod_name+'.'+jms_fsr_name+'.fconf_UN')
					#fcnf_PWD=(jms_mod_name+'.'+jms_fsr_name+'.fconf_PWD')

					k = 1
					while(k <= int(total_conf)):
						print("CON FACT"+str(k))
						fconf_name = configProps.get(fcnf_name+str(k))
						fconf_ljndi = configProps.get(fcnf_ljndi1+str(k))
						fconf_rjndi= configProps.get(fcnf_rjndi1+str(k))
						#fconf_UN= configProps.get(fcnf_UN+str(k))
						#fconf_PWD= configProps.get(fcnf_PWD+str(k))
						createFSConnectionFactory(jms_mod_name,jms_fsr_name,fconf_name,fconf_ljndi,fconf_rjndi)
						k = k + 1

					l = l + 1
				a = a+1
				print("JMS MOD:"+str(a))
		save()
		activate(200000,block='true')
		disconnect()

	except:
		print '  ACIVATION FAILED....'
		dumpStack()
main(sys.argv)

