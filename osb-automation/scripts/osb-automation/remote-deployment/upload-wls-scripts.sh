env=$1
/usr/local/bin/python3.5 /home/automation/deploymentAutomation/scripts/osb-automation/checkout-config.py $1
file=/home/automation/deploymentAutomation/scripts/osb-automation/osb-tmp/env_details/$env-server.properties
. $file

password=`echo $password|base64 -d`

echo "Uploading WLS Scripts to the target server  ... "+$host
sshpass -p $password rsync -r /home/automation/deploymentAutomation/scripts/osb-automation/remote-deployment/wls-scripts/osb-automation/wls-scripts/* $username@$host:/home/oracle/auto1/
echo "Successfully uploaded WLS scripts ..."
