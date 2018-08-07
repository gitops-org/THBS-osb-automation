test_mode=$1
domain=$2
servicenames=$3
cd "/home/automation/deploymentAutomation/scripts/test-automation/"
cd "/home/automation/deploymentAutomation/scripts/test-automation/test-scripts/test-automation/Release-1.3/AutomationUtility"
echo $servicenames
java -jar testAutomate.jar /home/automation/deploymentAutomation/scripts/test-automation/test-scripts/test-automation/Release-1.3/AutomationUtility/automationUtility.properties $test_mode $domain $servicenames
