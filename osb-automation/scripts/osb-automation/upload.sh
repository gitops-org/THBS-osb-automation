build_number=$1
service_name=$2
env=$3


releasepath="/home/automation/deploymentAutomation/code/osb/osb-releases/osb.source-1.0-"$build_number".jar"
unset http_proxy
curl -v -u deployment:deployment123 --upload-file $releasepath http://10.5.194.176:8081/repository/ESB_$env/$service_name/$service_name-$build_number.jar


