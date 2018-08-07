from java.util import Properties
from java import io
from java.io import FileInputStream
from java.io import File
from java.lang import Exception
from java.lang import Throwable
import os.path
import sys

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


def createJMSsrvr(jms_srv_name,target_name,persis_store,page_dir, thrs_high, thrs_low, msg_size):
        cd('/')
        srvr = create(jms_srv_name, "JMSServer")
        cd('/Deployments/'+jms_srv_name)
        srvr.setPersistentStore(getMBean('/FileStores/'+persis_store))
        srvr.setPagingDirectory(page_dir)
        srvr.addTarget(getMBean("/Servers/"+target_name))
        srvr.setBytesThresholdLow(long(thrs_low))
        srvr.setBytesThresholdHigh(long(thrs_high))
        srvr.setMaximumMessageSize(long(msg_size))

def createJMSModule(jms_mod_name,targetms,jms_sub_mod_name,jms_queue_target):
                # Build JMS Module - target preferrable cluster
                cd('/')
                cmo.createJMSSystemResource(jms_mod_name)
                print("jms_mod_name : "+jms_mod_name)
                cd('/SystemResources/'+jms_mod_name)
                set('Targets',jarray.array([ObjectName('com.bea:Name='+targetms+',Type=Server')], ObjectName))
                print "@@@ created JMS module ..."

                # Create and configure JMS Subdeployment for this JMS System Module
                cmo.createSubDeployment(jms_sub_mod_name)
                cd('SubDeployments')
                print("jms_queue_target : "+jms_queue_target)
                cd(jms_sub_mod_name)
				targets_jms=jms_queue_target.split(",")
                list=[]
                for target in targets_jms:
                        s='com.bea:Name='+target+',Type=JMSServer'
                        print("targets :"+s)
                        list.append(ObjectName(str(s)))
                set('Targets',jarray.array(list, ObjectName))
                print "@@@ created JMS subdeployment..."

def createJMSConnectionFactory(jms_mod_name,jmsCF,jmsCFJNDI,isXAVal):
                cd('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name)
                cmo.createConnectionFactory(jmsCF)
                cd('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name+'/ConnectionFactories/'+ jmsCF)
                cmo.setJNDIName(jmsCFJNDI)
                cd('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name+'/ConnectionFactories/'+ jmsCF)
                cmo.setSubDeploymentName(jms_sub_mod_name)
                #cmo.setDefaultTargetingEnabled(bool("true"))
                print "@@@ created JMS Connection Factory..."

def createJMSQueue(jms_sub_mod_name,jms_mod_name,jms_queue_name,jms_jndi_name,jms_queue_target,jms_isDistributed,jms_isForeign,foreign_init_context):
        try:
                newQueue = getMBean("/JMSSystemResources/"+jms_mod_name+"/JMSResource/"+jms_mod_name+"/Queues/"+jms_queue_name)
                if newQueue is None:
                        jmsResource = getMBean('/JMSSystemResources/'+jms_mod_name+'/JMSResource/'+jms_mod_name)
                        if jms_isDistributed == 'true':
                                print("Creating Uniform Distributed JMS Queue")
                                newQueue = jmsResource.createUniformDistributedQueue(jms_queue_name)
                                newQueue.setJNDIName(jms_jndi_name)
                                newQueue.getDeliveryParamsOverrides().setRedeliveryDelay(100);
                                newQueue.getDeliveryFailureParams().setRedeliveryLimit(5);
                                newQueue.getDeliveryFailureParams().setExpirationPolicy('Log');
                        elif jms_isForeign == 'true':
                                print("Creating Foreign JMS ")
                                newQueue  =  jmsResource.createForeignServer(jms_queue_name)
                                newQueue.setConnectionURL(jms_jndi_name)
                                newQueue.setInitialContextFactory(foreign_init_context)
                                if jms_queue_target == '':
                                        newQueue.setDefaultTargetingEnabled(bool("true"))
                        else:
                                print("Creating Jms Queue")
                                newQueue = jmsResource.createQueue(jms_queue_name)
                                newQueue.setJNDIName(jms_jndi_name)
                        print("JNDIName : "+jms_jndi_name)
                        print("JNDI connection URL :"+jms_jndi_name)
                        newQueue.setSubDeploymentName(jms_sub_mod_name)
                else:
                        print "*** JMS Queue already exists... Skipping"
                print "@@@ created JMS Request Queue..."
        except :

                print dumpStack()


#--------------------------------------------------------------------------------------------------------
envproperty=""

if (len(sys.argv) > 1):
        envproperty=sys.argv[1]
else:
        print "Environment Property file not specified"
        sys.exit(2)


propInputStream=FileInputStream(envproperty)
configProps=Properties()
configProps.load(propInputStream)

adminUser=sys.argv[2]
adminPassword=sys.argv[3]
adminURL=sys.argv[4]

connect(adminUser,adminPassword,adminURL)

edit()
startEdit()

print "#=============# JMS SERVER and PERSISITENT STORE CONFIGURATION #=============#"
total_fstore=configProps.get("total_fstore")
total_jque=configProps.get("total_jque")
total_jmssrvr=configProps.get("total_jmssrvr")
total_servers=configProps.get("total_servers")


print("Total JMS queue: "+total_jque)
print("Total JMS Server : "+total_jmssrvr)
print("Totalserver : "+total_servers)

#persis_store='FileStore_Konnect'
#jms_srvr_name='osb_server'

j=1
while (j <= int(total_jmssrvr)):
        jms_srv_name=configProps.get("jms_srvr_name"+ str(j))
        trg=configProps.get("jms_srvr_target"+ str(j))
        persis_store=configProps.get("jms_srvr_persis_store_name"+str(j))
        page_dir=configProps.get("jms_srvr_pag_dir"+str(j))
        thrs_high=configProps.get("jms_srvr_by_threshold_high"+str(j))
        thrs_low=configProps.get("jms_srvr_by_threshold_low"+str(j))
        msg_size=configProps.get("jms_srvr_max_msg_size"+str(j))
        createFlstr(persis_store,page_dir,trg)
        createJMSsrvr(jms_srv_name,trg,persis_store,page_dir,thrs_high,thrs_low,msg_size)
        j = j+1
#==========================================================================================#
clusterName = configProps.get("clusterName")
jms_mod_name = configProps.get("jms_mod_name")
jms_sub_mod_name = configProps.get("jms_sub_mod_name")
jms_srv_name = configProps.get("jms_srvr_name1")
targetms = configProps.get("jms_targetManageServerName")
jmsCF = configProps.get("jmsCF")
jmsCFJNDI = configProps.get("jmsCFJNDI")
isXAVal = configProps.get("isXAVal")
jms_queue_name1= configProps.get("jms_queue_name1")
jms_jndi_name= configProps.get("jms_jndi_name1")
jms_queue_target= configProps.get("jms_queue_target1")
jms_isDistributed=False
jms_isForeign=False

createJMSModule(jms_mod_name,targetms,jms_sub_mod_name,jms_queue_target)
if jms_isForeign != "true" :
        createJMSConnectionFactory(jms_mod_name,jmsCF,jmsCFJNDI,isXAVal)
q=1

while (q <= int (total_jque)):
        print("Queue props index : "+str(q))
        jms_queue_name = configProps.get("jms_queue_name"+str(q))
        jms_jndi_name = configProps.get("jms_jndi_name"+str(q))
        jms_queue_target =configProps.get("jms_queue_target"+str(q))
        jms_isDistributed = configProps.get("jms_isDistributed"+str(q))
        print("distri :"+str(jms_isDistributed))
        jms_isForeign = configProps.get("jms_isForeign"+str(q))
        print("ForeignJMS : "+str(jms_isForeign))
        foreign_init_context=configProps.get("foreign_context"+str(q))
        createJMSQueue(jms_sub_mod_name,jms_mod_name,jms_queue_name,jms_jndi_name,jms_queue_target,jms_isDistributed,jms_isForeign,foreign_init_context)
        q=q+1

try :
        activate()
except :
        print '  ACIVATION FAILED....'
        print dumpStack()
        exit()
