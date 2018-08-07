#!/bin/sh
#!/usr/bin/expect

env=$1

file=/home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/env_details/$env-server.properties
. $file

echo $wls_url;
echo $username
echo $host
echo $password|base64 -d


echo $wls_username
echo $wls_password|base64 -d
echo $wls_url

password=`echo $password|base64 -d`
wls_password=`echo $wls_password|base64 -d`

flag="true"

if [ "$fjms" == "$flag" ]
then
	echo "FJMS Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/weblogic_resources/release/fsjms.property $username@$host:/home/oracle/automation/FJMS/	
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/FJMS/jms_create_fserver.sh $wls_username $wls_password $wls_url"
fi

if [ "$db" == "$flag" ]
then
	echo "DB Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/weblogic_resources/release/db_details.property $username@$host:/home/oracle/automation/DB/
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/DB/db_create.sh $wls_username $wls_password $wls_url"
fi

if [ "$jms" == "$flag" ]
then
	echo "JMS Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/weblogic_resources/release/jms.property $username@$host:/home/oracle/automation/JMS/
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/JMS/jms_create.sh $wls_username $wls_password $wls_url"
fi

if [ "$aq" == "$flag" ]
then
	echo "AQ Module ..."
	echo "upload property file to dest server .. "+$env
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/weblogic_resources/release/aq_details.property $username@$host:/home/oracle/automation/AQ/
	sshpass -p $password pssh -h hosts.txt -l $username -A -i "~/automation/AQ/aq_create.sh $wls_username $wls_password $wls_url"
else
	echo "none of the conditions are successfull .."
fi


