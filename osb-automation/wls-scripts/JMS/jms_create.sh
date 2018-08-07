username=$1
password=$2
url=$3
cd /u01/app/oracle/Middleware/wlserver_10.3/server/bin/
. ./setWLSEnv.sh
java weblogic.WLST ~/automation/JMS/jms.py /home/oracle/automation/JMS/jms.property $username $password $url
exit 1

