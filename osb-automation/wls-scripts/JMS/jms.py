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
	cmo.setDirectory(dir_name+'/'+str(fstr_name))
	print "target_name:"+target_name
	#set('Targets',jarray.array([ObjectName('com.bea:Name='+target_name+',Type=Cluster')], ObjectName))
	set('Targets',jarray.array([ObjectName('com.bea:Name='+target_name+',Type=Server')], ObjectName))
	print "@@@ created JMS Filestore ..."+fstr_name
	
def createJDstr(jstr_name,ds_name,target_name,prefix):
        cd('/')
        jst = create(jstr_name, "JDBCStore")
        cd('/JDBCStores/'+jstr_name)
        cmo.setDataSource(getMBean('/SystemResources/'+ds_name))
        cmo.setPrefixName(prefix)
        jst.addTarget(getMBean("/Servers/"+target_name))
 
def createJMSsrvr(jms_srv_name,target_name,persis_store,page_dir,thrs_high,thrs_low,msg_size):
		print "in jms scerver"
		cd('/')
		srvr = create(jms_srv_name, "JMSServer")
		cd('/Deployments/'+jms_srv_name)
		srvr.setPersistentStore(getMBean('/FileStores/'+persis_store))
		srvr.setPagingDirectory(page_dir)
		srvr.addTarget(getMBean("/Servers/"+target_name))
		srvr.setBytesThresholdLow(long(thrs_low))
		srvr.setBytesThresholdHigh(long(thrs_high))
		srvr.setMaximumMessageSize(long(msg_size))
		print"in jms scerver"
		
def getJMSModule(jms_mod_name,allJMSResources):
	print "in jmsyyyy mode"
	for jmsResource in allJMSResources:
		JM_Mod = str(jmsResource.getName())	
		print ("in jms mode"+JM_Mod)
		if JM_Mod == jms_mod_name:
			print ("in jms xxmode"+JM_Mod)
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
		print "in jms sub-0"
		cd('SubDeployments')
		print "in jms sub0"
		#print("jms_queue_target : "+jms_queue_target)	
		cd(jms_sub_mod_name)
		print "in jms sub1"
		list=[]
		print "in jms sub2"
		N=1
		print "in jms sub3"
		while(N <= int(total_servers)):
			print "in jms sub"
			print jms_srv_name
			s='com.bea:Name='+jms_srv_name+str(N)+',Type=JMSServer'
			print("targets :"+s)
                        list.append(ObjectName(str(s)))
			N=N+1
		set('Targets',jarray.array(list, ObjectName))
		print "@@@ created JMS subdeployment..."
		

def createJMSConnectionFactory(jms_mod_name,jmsCF,jmsCFJNDI,jms_sub_mod_name):
		cd('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name)
		cmo.createConnectionFactory(jmsCF)
		cd('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name+'/ConnectionFactories/'+ jmsCF)
		cmo.setJNDIName(jmsCFJNDI)
		cd('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name+'/ConnectionFactories/'+ jmsCF)
		cmo.setSubDeploymentName(jms_sub_mod_name)
		#cmo.setDefaultTargetingEnabled(bool("true"))
		print "@@@ created JMS Connection Factory..."
		
def createJMSQueue(jms_sub_mod_name,jms_mod_name,jms_queue_name,jms_jndi_name,jms_queuetype,jms_RedeliveryDelay,jms_RedeliveryLimit,jms_ExpirationPolicy):
	try:	
		if jms_queuetype =='Distributed':
			newQueue = getMBean("/JMSSystemResources/"+jms_mod_name+"/JMSResource/"+jms_mod_name+"/Queues/"+jms_queue_name)
			if newQueue is None:
				jmsResource = getMBean('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name)
				print("Creating Uniform Distributed JMS Queue")
				newQueue = jmsResource.createUniformDistributedQueue(jms_queue_name)
				newQueue.setJNDIName(jms_jndi_name)
				print ("jms_RedeliveryDelay" +jms_RedeliveryDelay)
				newQueue.getDeliveryParamsOverrides().setRedeliveryDelay(int(jms_RedeliveryDelay))
				newQueue.getDeliveryFailureParams().setRedeliveryLimit(int(jms_RedeliveryLimit))
				newQueue.getDeliveryFailureParams().setExpirationPolicy(str(jms_ExpirationPolicy))
				print("JNDIName : "+jms_jndi_name)
				print("JNDI connection URL :"+jms_jndi_name)
				print("setSubDeploymentName_D :"+jms_sub_mod_name)
				newQueue.setSubDeploymentName(jms_sub_mod_name)
				print "@@@ created JMS Request Queue..." 
			else: 
				print "*** JMS Queue already exists... Skipping"
				
		elif jms_queuetype =='Topics':
			newQueue = getMBean("/JMSSystemResources/"+jms_mod_name+"/JMSResource/"+jms_mod_name+"/Topics/"+jms_queue_name)
			if newQueue is None:
				jmsResource = getMBean('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name)
				print("Creating Topcis Queue")
				newQueue = jmsResource.createTopic(jms_queue_name)
				newQueue.setJNDIName(jms_jndi_name)
				newQueue.getDeliveryParamsOverrides().setRedeliveryDelay(int(jms_RedeliveryDelay))
				newQueue.getDeliveryFailureParams().setRedeliveryLimit(int(jms_RedeliveryLimit))
				newQueue.getDeliveryFailureParams().setExpirationPolicy(str(jms_ExpirationPolicy))
				print("JNDIName : "+jms_jndi_name)
				print("JNDI connection URL :"+jms_jndi_name)
				print("setSubDeploymentName_T :"+jms_sub_mod_name)
				newQueue.setSubDeploymentName(jms_sub_mod_name)
				print "@@@ created JMS Request Topics..."
			else: 
				print "*** Topics already exists... Skipping"
					
		else:
			newQueue = getMBean("/JMSSystemResources/"+jms_mod_name+"/JMSResource/"+jms_mod_name+"/Queues/"+jms_queue_name)
			if newQueue is None:
				jmsResource = getMBean('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name)
				print("Creating Jms Queue")
				newQueue = jmsResource.createQueue(jms_queue_name)
				newQueue.setJNDIName(jms_jndi_name)
				newQueue.getDeliveryParamsOverrides().setRedeliveryDelay(int(jms_RedeliveryDelay))
				newQueue.getDeliveryFailureParams().setRedeliveryLimit(int(jms_RedeliveryLimit))
				newQueue.getDeliveryFailureParams().setExpirationPolicy(str(jms_ExpirationPolicy))
				print("JNDIName : "+jms_jndi_name)
				print("JNDI connection URL :"+jms_jndi_name)
				print("setSubDeploymentName_Q :"+jms_sub_mod_name)
				newQueue.setSubDeploymentName(jms_sub_mod_name)
				print "@@@ created JMS Request Queue..." 
			else: 
				print "*** JMS Queue already exists... Skipping"
	except :
        
        	print dumpStack()

	
#-------------------------------------------------------------------------------------------------------- 

def getProperties(file):
  try:
    property = FileInputStream(file)
    properties = Properties()
    properties.load(property)
  except:
    print("props file is invalid")
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

	#propfile=sys.argv[1]
        #wls_username=sys.argv[2]
        #wls_password=sys.argv[3]
        #url=sys.argv[4]
        #wls_username = 'wlsdeploy'
        #wls_password = 'wlsdeploy@123'
        #url = 't3://10.5.213.83:7001'  
	try:
		print('--> Load properties..........')
		configProps=getProperties("/home/oracle/automation/JMS/jms.property");
		connect(wls_username,wls_password,url)
		 
		edit()
		startEdit()

		print "#=============# JMS SERVER and PERSISITENT STORE CONFIGURATION #=============#"

		#total_jque=configProps.get("total_jque")
		total_servers=configProps.get("total_servers")
		total_jmsmn=configProps.get("total_jmsmodules")
		#total_conf=configProps.get("total_conf")

		#print("Total JMS queue: "+total_jque)
		print("Total Server : "+total_servers)
		print("Total J M : "+total_jmsmn)
		allJMSResources = cmo.getJMSSystemResources()
		
		a=1
		print("aaaa ou1"+ str(a))
		while(a <= int(total_jmsmn)):
				print("aaaa ou2"+ str(a))
				var1=int(a)
				jms_mod_name=configProps.get("jms_mod_name"+ str(var1))
				jms_sub_m=(jms_mod_name+'.jms_sub_mod_name')
				jms_sub_mod_name=configProps.get(jms_sub_m)
				print("hhhhh" + jms_mod_name + str(var1))
				JM = getJMSModule(jms_mod_name,allJMSResources)
				print(JM)
				if JM == True:
					print(JM)
					jms_srv_n=(jms_mod_name+'.jms_srvr_name')
					jms_srv_name=configProps.get(jms_srv_n)
					jms_per_st=(jms_mod_name+'.jms_srvr_persis_store_name')
					jms_page_dir1=(jms_mod_name+'.jms_srvr_pag_dir1')
					jms_page_dir2=(jms_mod_name+'.jms_srvr_pag_dir2')
					thr_high=(jms_mod_name+'.jms_srvr_by_threshold_high')
					thr_low=(jms_mod_name+'.jms_srvr_by_threshold_low')
					mssg_size=(jms_mod_name+'.jms_srvr_max_msg_size')
					targetms=configProps.get("jms_targetManageServerName")
					print("hhhhh" + jms_sub_mod_name + str(var1))
			
					i=1
					print("iiiiiii"+str(i))
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
						print "after file store"
						print targetms+str(i)
						createJMSsrvr(jms_srv_name+str(i),targetms+str(i),persis_store+str(i),page_dir,thrs_high,thrs_low,msg_size)
						print "after jms scerver"
						i = i + 1
						
					print "before jms mode"	
					createJMSModule(jms_mod_name,targetms,jms_sub_mod_name,jms_srv_name,total_servers)
					print "before que mode"
					
				print "after jms mode"	
				total_jque=configProps.get(jms_mod_name+'.queue_topics')
				jms_q_name=(jms_mod_name+'.jms_queue_name')
				jms_j_name=(jms_mod_name+'.jms_jndi_name')
				jms_quetype=(jms_mod_name+'.jms_queuetype')
				jms_RedelDelay=(jms_mod_name+'.jms_setRedeliveryDelay')
				jms_RedelLimit=(jms_mod_name+'.jms_setRedeliveryLimit')
				jms_ExpPolicy=(jms_mod_name+'.jms_setExpirationPolicy')	
				print "dddddddddddddddddddd" +jms_RedelDelay
				print "dddddddddddddddddddd" +jms_RedelLimit
				print "dddddddddddddddddddd" +jms_ExpPolicy
				j=1
				print("jjjjjjjjjj"+ str(j))
				while(j <= int(total_jque)):
					jms_queue_name = configProps.get(jms_q_name+str(j))
					jms_jndi_name = configProps.get(jms_j_name+str(j))
					jms_queuetype = configProps.get(jms_quetype+str(j))
					jms_RedeliveryDelay = configProps.get(jms_RedelDelay+str(j))
					jms_RedeliveryLimit = configProps.get(jms_RedelLimit+str(j))
					jms_ExpirationPolicy = configProps.get(jms_ExpPolicy+str(j))
					print "yyyyyyyyyyyyyy" +jms_RedeliveryDelay
					print "yyyyyyyyyyyyyy" +jms_RedeliveryLimit
					print "yyyyyyyyyyyyyy" +jms_ExpirationPolicy
					createJMSQueue(jms_sub_mod_name,jms_mod_name,jms_queue_name,jms_jndi_name,jms_queuetype,jms_RedeliveryDelay,jms_RedeliveryLimit,jms_ExpirationPolicy)
					j = j + 1
					
				total_conf=configProps.get(jms_mod_name+'.connectionfactory')
				jCF=(jms_mod_name+'.jmsCF')
				jCFJNDI=(jms_mod_name+'.jmsCFJNDI')
				
				k = 1
				print("kkkkkkkkkk"+str(k))
				while(k <= int(total_conf)):
					jmsCF = configProps.get(jCF+str(k))
					jmsCFJNDI = configProps.get(jCFJNDI+str(k))
					print("rrrrrr"+str(k))
					createJMSConnectionFactory(jms_mod_name,jmsCF,jmsCFJNDI,jms_sub_mod_name)
					k = k + 1
					print("aaaa:"+ str(a))	
				a = a+1
				print("aaaa:"+str(a))
		save()
		activate(200000,block='true')
		disconnect()
		
	except :
			print '  ACIVATION FAILED....'
			dumpStack()
main(sys.argv)
