#!/bin/sh
#!/usr/bin/expect

env=$1

file=/home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/envconfig/$env-server.properties
. $file

echo $wls_url;
echo $username
echo $host
echo $password

echo $wls_username
echo $wls_password
echo $wls_url

password=$password

flag="true"

if [ "$fjms" == "$flag" ]
then
	echo "FJMS Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/weblogic_resources/release/fsjms.property $username@$host:/home/oracle/automation/FJMS/	
	#./scp-conn.exp $host $username $password /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/fjms/release/fsjms.property /home/oracle/automation/FJMS/
	#./fjms-conn.exp $host $username $password $wls_username $wls_password $wls_url
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/FJMS/jms_create_fserver.sh $wls_username $wls_password $wls_url"
fi

if [ "$db" == "$flag" ]
then
	echo "DB Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/weblogic_resources/release/db_details.property $username@$host:/home/oracle/automation/DB/
	#./scp-conn.exp $host $username $password /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/db/release/details.properties /home/oracle/automation/DB/
	#./db-conn.exp $host $username $password $wls_username $wls_password $wls_url
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/DB/db_create.sh $wls_username $wls_password $wls_url"
fi

if [ "$jms" == "$flag" ]
then
	echo "JMS Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/weblogic_resources/release/jms.property $username@$host:/home/oracle/automation/DB/
	#./scp-conn.exp $host $username $password /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/jms/release/jms.properties /home/oracle/automation/DB/
	#./jms-conn.exp $host $username $password $wls_username $wls_password $wls_url
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/JMS/jms_create.sh $wls_username $wls_password $wls_url"
fi

if [ "$aq" == "$flag" ]
then
	echo "AQ Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/weblogic_resources/release/aq_details.property $username@$host:/home/oracle/automation/AQ/
	#./scp-conn.exp $host $username $password /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/aq/release/AQ_details.property /home/oracle/automation/AQ/
	#./aq-conn.exp $host $username $password $wls_username $wls_password $wls_url
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/AQ/aq_create.sh $wls_username $wls_password $wls_url"
else
	echo "none of the conditions are successfull .."
fi

