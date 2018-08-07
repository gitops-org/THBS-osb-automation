cd /u01/app/oracle/Middleware/wlserver_10.3/server/bin/
. ./setWLSEnv.sh
java weblogic.WLST ~/automation/JMS/foreign_server/create_foreignServer.py /home/oracle/automation/FJMS/fsjms.property wlsdeploy wlsdeploy@123 t3://10.5.213.83:7001

