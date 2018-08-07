username=$1
password=$2
url=$3

cd /u01/app/oracle/Middleware/wlserver_10.3/server/bin/
. ./setWLSEnv.sh
java weblogic.WLST ~/automation/DB/JDBC_Creation.py /home/oracle/automation/DB/db_details.property $username $password $url

