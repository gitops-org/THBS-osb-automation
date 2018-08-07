import sys
import os
from java.io import FileInputStream

from com.bea.wli.config.customization import Customization
from com.bea.wli.sb.management.importexport import ALSBImportOperation
from com.bea.wli.sb.management.configuration import ALSBConfigurationMBean
from com.bea.wli.sb.management.configuration import SessionManagementMBean

def customizeOSBService():
        SessionMBean = None
        username = sys.argv[1]
        password = sys.argv[2]
        serverUrl = sys.argv[3]
        customizeFile = sys.argv[4]

        try:
                print("customization file : "+customizeFile)
                connect(username, password, serverUrl)
                domainRuntime()
                sessionName = "customization"
                SessionMBean = findService("SessionManagement", "com.bea.wli.sb.management.configuration.SessionManagementMBean")
                SessionMBean.createSession(sessionName)
                OSBConfigurationMBean = findService(String("ALSBConfiguration.").concat(sessionName),"com.bea.wli.sb.management.configuration.ALSBConfigurationMBean")
                print "ALSBConfiguration MBean found", OSBConfigurationMBean
                iStream = FileInputStream(customizeFile)
                customizationList = Customization.fromXML(iStream)
                OSBConfigurationMBean.customize(customizationList)
                SessionMBean.activateSession(sessionName, "Complete customization using wlst")
                disconnect()

        except:
                print "Unexpected error:", sys.exc_info()[0]
                dumpStack()
                if SessionMBean != None:
                        SessionMBean.discardSession(sessionName)
                raise

def main():
        customizeOSBService()
        print 'Successfully Completed customization'
main()
