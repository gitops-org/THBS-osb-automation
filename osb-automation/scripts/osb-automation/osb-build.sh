cd /home/automation/deploymentAutomation
/home/automation/deploymentAutomation/lib/apache-maven-3.1.1/bin/mvn -f osb-pom-services.xml clean package
cp /home/automation/deploymentAutomation/code/osb/target/*.jar /home/automation/deploymentAutomation/code/osb/osb-releases/

