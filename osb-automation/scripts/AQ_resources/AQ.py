#!/usr/bin/python
from java.io import FileInputStream
import time

def makeDeploymentPlanVariable(wlstPlan, name, value, xpath, origin='planbased'):
  """Create a varaible in the Plan.
  This method is used to create the variables that are needed in the Plan in order
  to add an entry for the outbound connection pool for the new data source.
  """
  try:
    variableAssignment = wlstPlan.createVariableAssignment(name, moduleOverrideName, moduleDescriptorName)
    variableAssignment.setXpath(xpath)
    variableAssignment.setOrigin(origin)
    wlstPlan.createVariable(name, value)
  except:
    print('--> was not able to create deployment plan variables successfully')


def getProperties(file):
  try:
    property = FileInputStream(file)
    properties = Properties()
    properties.load(property)
  except:
    print("props file is invalid")
    sys.exit(0)
  return properties


def main(argv):
  #
  # generate a unique string to use in the names
  #
        uniqueString =''
        uniqueString = str(int(time.time()))
        wls_username = argv[2]
        wls_password = argv[3]
        url = argv[4]
        mw_home = argv[5]
  #
  # Create a AQ Data Source.
  #
        try:
                print('--> Load properties for AQ :'+argv[1])
                configProps=getProperties(argv[1]);
                total_jndi_to_create=configProps.get('total.AQjndi')
                print("JNDI Total :"+total_jndi_to_create)
                planPath = configProps.get('shared_AQ_PlanPath')
                appPath = configProps.get('AQ_appPath')
                appName='AqAdapter'
                moduleOverrideName=appName+'.rar'
                moduleDescriptorName='META-INF/weblogic-ra.xml'
                print('--> about to connect to weblogic')
                connect(wls_username, wls_password, url)
                edit()
                #
                # update the deployment plan
                #
                startEdit()
                i=1
                while (i <= int(total_jndi_to_create)):
                  cd('/')
                  print('--> about to update the deployment plan for the AqAdapter')
                  eisName = configProps.get('AQeisName.'+ str(i))
                  print('--> about to create a Adapter JNDI ' + eisName)
                  dsName = configProps.get("AQds."+ str(i))
                  print('--> about to assign a data source ' + dsName)
                  #startEdit()
                  print('--> Using plan ' + planPath)
                  plan = loadApplication(appPath, planPath)
                  print('--> adding variables to plan')
                  print('___ BEGIN change plan')
                  makeDeploymentPlanVariable(plan, 'ConnectionInstance_'+ eisName +'_JNDIName_'+ uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+ eisName + '"]/jndi-name')
                  makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_'+ dsName + '_',dsName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="'+ eisName + '"]/connection-properties/properties/property/[name="xADataSourceName"]/value')
                  print('___ DONE change plan')
                  print('--> saving plan')
                  plan.save();
                  save();
                  print('--> activating changes')
                  activate(block='true');
                  cd('/AppDeployments/AqAdapter/Targets');
                  print('--> redeploying the AqAdapter')
                  redeploy(appName, planPath, targets=cmo.getTargets());
                  print('--> done')
                  i=i+1
        except:
                print('--> something went wrong, bailing out', sys.exc_info()[0])
                stopEdit('y')
                raise SystemExit

main(sys.argv)
