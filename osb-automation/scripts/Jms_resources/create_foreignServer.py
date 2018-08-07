#!/usr/bin/python
from java.util import Properties
from java import io
from java.io import FileInputStream
from java.io import File
from java.lang import Exception
from java.lang import Throwable
import os.path
import sys

def getJMSModulePath(jms_module_name):
        jms_module_path = "/JMSSystemResources/"+jms_module_name+"/JMSResource/"+jms_module_name
        return jms_module_path

def createFSJMSModule(jms_module_name,target_name):
        cd('/')
        print "inside createFSJMSModule"
        module = create(jms_module_name, "JMSSystemResource")
        cluster = getMBean("Clusters/"+target_name)
        module.addTarget(cluster)

def createJMSFS(jms_module_name,cnurl,jms_fs_name,ini_fac):
        print "inside createJMSFS"
        jms_module_path = getJMSModulePath(jms_module_name)
        cd(jms_module_path)
        cmo.createForeignServer(jms_fs_name)
        cd(jms_module_path+'/ForeignServers/'+jms_fs_name)
        cmo.setInitialContextFactory(ini_fac)
        cmo.setConnectionURL(cnurl)
        cmo.setDefaultTargetingEnabled(bool("true"))
        cmo.unSet('JNDIPropertiesCredentialEncrypted')

def getFSpath(jms_module_name,jms_fs_name):
        print "inside getFSpath"
        jms_module_path = getJMSModulePath(jms_module_name)
        jms_fs_path = jms_module_path+'/ForeignServers/'+jms_fs_name
        return jms_fs_path

def createFSdest(jms_module_name,jms_fs_name,jms_dest_name,ljndi,rjndi):
        print "inside createFSdest"
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

def createFSconf(jms_module_name,jms_fs_name,jms_fconf_name,cljndi,crjndi):
        print "inside createFSconf"
        jms_fs_path = getFSpath(jms_module_name,jms_fs_name)
        cd(jms_fs_path)
        cmo.createForeignConnectionFactory(jms_fconf_name)
        cd(jms_fs_path+'/ForeignConnectionFactories/'+jms_fconf_name)
        cmo.setLocalJNDIName(cljndi)
        cmo.setRemoteJNDIName(crjndi)

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


############## MAIN SCRIPT starts  ##########
def main():
        envproperty='/home/oracle/automation/JMS/foreign_server/jms-fserver.properties'

        #adminUser=configProps.get("adminUser")
        #adminPassword=configProps.get("adminPassword")
        #adminURL=configProps.get("adminURL")

        adminUser="wlsdeploy"
        adminPassword="wlsdeploy@123"
        adminURL="t3://10.5.213.83:7001"
        try:
                connect(adminUser,adminPassword,adminURL)
                configProps=getProperties(envproperty)
                #propInputStream=FileInputStream(envproperty)
                #configProps=Properties()
                #configProps.load(propInputStream)

                edit()
                startEdit()

                ##############################################
                #FOREIGN JMS SERVER CONFIGURATION
                ##############################################
                total_dest=configProps.get("total_dest")
                total_fconf=configProps.get("total_fconf")
                print("total components : "+total_dest+":"+total_fconf)

                cluster_target_name=configProps.get("clusterName")

                print("JMS MODULE CREATION")
                trg=configProps.get("clusterName")
                fs_mod_name=configProps.get("fsjms_mod_name")
                createFSJMSModule(fs_mod_name,trg)
                fr_server=configProps.get("fr_server")
                cnfurl=configProps.get("cnfurl")
                ini_context=configProps.get("initialContextFactory")
                createJMSFS(fs_mod_name,cnfurl,fr_server,ini_context)

                d=1
                while(d<=int(total_dest)):
                        print("JMS DEST CREATION ")
                        d_name=configProps.get("destname"+ str(d))
                        d_ljndi=configProps.get("dest_ljndi"+ str(d))
                        d_rjndi=configProps.get("dest_rjndi"+ str(d))
                        print d_ljndi,' == ', d_rjndi
                        createFSdest(fs_mod_name,fr_server,d_name,d_ljndi,d_rjndi)
                        d=d+1

                cf=1
                while(cf<=int(total_fconf)):
                        print("JMS CONN FACT")
                        j_conf=configProps.get("fconf_name"+ str(cf))
                        cn_ljndi=configProps.get("fconf_ljndi"+ str(cf))
                        cn_rjndi=configProps.get("fconf_rjndi"+ str(cf))
                        createFSconf(fs_mod_name,fr_server,j_conf,cn_ljndi,cn_rjndi)
                        cf=cf+1

                # ####   MAIN SCRIPT END ########################################
                save()
                activate(block="true")
                disconnect()
        except:
                print '  ACIVATION FAILED....'
                dumpStack()
main()
