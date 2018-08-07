username=$1
password=$2
url=$3

cd /u01/app/oracle/Middleware/wlserver_10.3/server/bin/
. ./setWLSEnv.sh
java weblogic.WLST ~/automation/FJMS/fjms.py /home/oracle/automation/FJMS/fsjms.property $username $password $url

