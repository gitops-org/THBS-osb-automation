import os
import sys
from java.util import Properties
from java import io
from java.io import FileInputStream
from java.io import File
from java.lang import Exception
from java.lang import Throwable


# don't change these ones
uniqueString         = ''
appName              = 'DbAdapter'
moduleOverrideName   = appName+'.rar'
moduleDescriptorName = 'META-INF/weblogic-ra.xml'

def createJDBCDataSource(dsName,domainName,dsFileName,dsDatabaseName,datasourceTarget,dsJNDIName,dsDriverName,dsURL,dsUserName,dsPassword,dsTestQuery):
	edit()
	startEdit()
	cd('/')
	cmo.createJDBCSystemResource(dsName)
	
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName)
		
	cmo.setName(dsName)
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDataSourceParams/'+dsName )
	set('JNDINames',jarray.array([String('jdbc/' + dsName )], String))
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName )
	cmo.setUrl(dsURL)
	cmo.setDriverName( dsDriverName )
	cmo.setPassword(dsPassword)
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCConnectionPoolParams/'+dsName )
	cmo.setTestTableName(dsTestQuery)
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName+'/Properties/'+dsName )
	cmo.createProperty('user')
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName+'/Properties/'+dsName+'/Properties/user')
	cmo.setValue(dsUserName)
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName+'/Properties/'+dsName )
	cmo.createProperty('databaseName')
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName+'/Properties/'+dsName+'/Properties/databaseName')
	cmo.setValue(dsDatabaseName)
 
	cd('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDataSourceParams/'+dsName )
	cmo.setGlobalTransactionsProtocol('OnePhaseCommit')
 
	cd('/SystemResources/'+dsName )
	set('Targets',jarray.array([ObjectName('com.bea:Name='+datasourceTarget+',Type=Cluster')],ObjectName)) #--> for cluster
	#set('Targets',jarray.array([ObjectName('com.bea:Name='+datasourceTarget+',Type=Server')],ObjectName)) # --> for stand-alone server
	save()
	activate()
	
#
# update the deployment plan
#



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


'''def createDbAdapterJNDI(dsName,eisName,isXA):
	try:
		print('--> about to update the deployment plan for the DbAdapter')
		startEdit()
		planPath = get('/AppDeployments/DbAdapter/PlanPath')
		appPath = get('/AppDeployments/DbAdapter/SourcePath')
		print('--> Using plan ' + planPath)
		print('--> Using plan ' + appPath)
		plan = loadApplication(appPath, planPath)
		print('--> adding variables to plan')
		makeDeploymentPlanVariable(plan, 'ConnectionInstance_eis/DB/' + dsName + '_JNDIName_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/jndi-name')
		if(isXA=='true'):
			makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="dataSourceName"]/value')
		else:
			makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="dataSourceName"]/value')
		print('--> saving plan')
		plan.save();
		save();
		print('--> activating changes')
		activate(block='true');
		cd('/AppDeployments/DbAdapter/Targets');
		print('--> redeploying the DbAdapter')
		redeploy(appName, planPath, targets=cmo.getTargets());
		print('--> done')
	except:
		print('--> something went wrong, bailing out')
		stopEdit('y')
		raise SystemExit
'''
 
  #
  # disconnect from the admin server
  #

	
def main(argv):
	propInputStream = FileInputStream(argv[1])
	configProps = Properties()
	configProps.load(propInputStream)
	adminUserName=argv[2]
	adminPassword=argv[3]
	adminURL=argv[4]
	domainName=argv[5]
	total_jdbcDS=configProps.get("total_jdbcDS")  
	j=1
	connect(adminUserName, adminPassword, adminURL)

	while (j <= int(total_jdbcDS)):
		dsName=configProps.get("datasource.name"+str(j))
		dsFileName=configProps.get("datasource.filename"+str(j))
		dsDatabaseName=configProps.get("datasource.database.name"+str(j))
		datasourceTarget=configProps.get("datasource.target"+str(j))
		dsJNDIName=configProps.get("datasource.jndiname"+str(j))
		dsDriverName=configProps.get("datasource.driver.class"+str(j))
		dsURL=configProps.get("datasource.url"+str(j))
		dsUserName=configProps.get("datasource.username"+str(j))
		dsPassword=configProps.get("datasource.password"+str(j))
		dsTestQuery=configProps.get("datasource.test.query"+str(j))
		eisName=configProps.get("eisName"+str(j))
		isXA=str(configProps.get("isXA"+str(j)))
		print('isXA:'+isXA)
		# Creating a Datasource...
		createJDBCDataSource(dsName,domainName,dsFileName,dsDatabaseName,datasourceTarget,dsJNDIName,dsDriverName,dsURL,dsUserName,dsPassword,dsTestQuery)
		#Creating a DbAdapter JNDI...
		'''if(eisName==''):
			print('JNDI name not provided...Outbound connection name will not be created...')
		else:
			#createDbAdapterJNDI(dsName,eisName,isXA)
		j=j+1'''
	disconnect()
	
#Calling main()

main(sys.argv)
