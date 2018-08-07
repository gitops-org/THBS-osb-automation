service=$1
servicename=$2
resourcename=$3
env=$4
domain_path=$5

. /home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/env_details/$env-server.properties

password=`echo $password|base64 -d`

echo "Uploading service config to .."$host

if [ "$service" == "S" ]
then
	sshpass -p $password rsync -r /home/automation/deploymentAutomation/scripts/osb-automation/service-config/$servicename $username@$host:$domain_path/services-config
	echo "Uploaded service config : "+$servicename
fi

if [ "$service" == "F" ]
then
	sshpass -p $password rsync -az /home/automation/deploymentAutomation/scripts/osb-automation/service-config/$servicename $username@$host:$domain_path/services-config/$resourcename
	 echo "Uploaded service config file :  servicepath :"+$servicename+" file path "+$resourcename
fi
