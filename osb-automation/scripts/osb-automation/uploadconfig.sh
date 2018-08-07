service=$1
servicename=$2
resourcename=$3
env=$4

. /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/$env/envconfig/$env-server.properties

password=`echo $password|base64 -d`

echo "Uploading service config to .."$host

if [ "$service" == "S" ]
then
	sshpass -p $password rsync -r /home/automation/deploymentAutomation/scripts/osb-automation/service-config/servicesconfig/$servicename $username@$host:/home/oracle/automation/servicesconfig/
	echo "Uploaded service config : "+$servicename
fi

if [ "$service" == "F" ]
then
	sshpass -p $password rsync /home/automation/deploymentAutomation/scripts/osb-automation/service-config/servicesconfig/$servicename/$resourcename $username@$host:/home/oracle/automation/servicesconfig/$servicename
	 echo "Uploaded service config file : "+$resourcename
fi
