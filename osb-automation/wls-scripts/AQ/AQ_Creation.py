#!/usr/bin/python
from java.io import FileInputStream
import time

def validate_inputs(args):
        print("1. Validating inputs\n")
        valStatus= False
        arg_count = len(args)-1
        if arg_count > 4:
                print("\nInvalid extra arguments! :"+str(arg_count))
                sys.exit()
        elif arg_count < 4:
                print("\nError! Missing environment argument!. \nPlease provide environment as another argument. \nExample:- python osb-master-final.py test")
                sys.exit()
        elif arg_count == 4:
                print("Valid arguments. Continuing.")
                return True
        else :
                return False


def makeDeploymentPlanVariable(wlstPlan, name, value, xpath, origin='planbased'):
  """Create a variable in the Plan.
  This method is used to create the variables that are needed in the Plan in order
  to add an entry for the outbound connection pool for the new data source.
  """
 
  try:  
    
    wlstPlan.showVariables()
    variableAssignment = wlstPlan.createVariableAssignment(name,'AqAdapter.rar' , 'META-INF/weblogic-ra.xml')
    variableAssignment.setXpath(xpath)
    variableAssignment.setOrigin(origin)
    wlstPlan.createVariable(name, value)

  except:
    print('--> was not able to create deployment plan variables successfully')



def createDbAdapterJNDI(dsName,eisName,dsJNDIName,isXA,planPath,appPath,uniqueString,dbType,PltClasName):
	try:
		print('--> about to update the deployment plan for the AqAdapter')
                print('--> Using plan ' + planPath)
                print('--> Using plan ' + appPath)
		plan = loadApplication(appPath, planPath)
		print('--> adding variables to plan: '+uniqueString)
		makeDeploymentPlanVariable(plan, 'ConnectionInstance_eis/DB/' + dsName + '_JNDIName_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/jndi-name')
		if (dbType=='Oracle'):
			if(isXA=='true'):
					makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, dsJNDIName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="xADataSourceName"]/value')
			else:
					makeDeploymentPlanVariable(plan, 'ConfigProperty_DataSourceName_Value_' + uniqueString, dsJNDIName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="DataSourceName"]/value')
		else:
			if(isXA=='true'):
					makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, dsJNDIName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="xADataSourceName"]/value')
					
					
			else:
					makeDeploymentPlanVariable(plan, 'ConfigProperty_DataSourceName_Value_' + uniqueString, dsJNDIName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="DataSourceName"]/value')
					
					makeDeploymentPlanVariable(plan, 'ConfigProperty_platformClassName_Value_' + uniqueString, PltClasName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="platformClassName"]/value')
		print('--> saving plan')
		plan.save();
		print('--> activating changes')
	except:
		print('--> something went wrong, bailing out')
		stopEdit('y')
		
def connPool(dsName,dsURL,dsDriverName,dsPassword,dsUserName) :

	 DRVPARM='/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName+'/JDBCDriverParams/'+dsName
	 cd(DRVPARM)
	 set('Url',dsURL)
	 set('DriverName',dsDriverName)
	 set('Password',dsPassword)
	 cd(DRVPARM+'/Properties/'+dsName)
	 print DRVPARM+'/Properties/'+dsName
	 cmo.createProperty('user')
	 cd(DRVPARM+'/Properties/'+dsName+'/Properties/user')
	 print DRVPARM+'/Properties/'+dsName+'/Properties/user'
	 print dsUserName
	 cmo.setValue(dsUserName)

def createJDBCDataSource(dsName,datasourceTarget,dsJNDIName,dsDriverName,dsURL,dsUserName,dsPassword,dsTestQuery,isXA,dbType,total_servers):
	try:
		startEdit()
		cd('/')
		print('Naming the datasource')
		cmo.createJDBCSystemResource(dsName)
		RESOURCE='/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName
		cd(RESOURCE)
		set('Name',dsName)
		 
		#Setting JNDI name
		cd(RESOURCE+'/JDBCDataSourceParams/'+dsName)
		print RESOURCE+'/JDBCDataSourceParams/'+dsName
		set('JNDINames',jarray.array([String(dsJNDIName)], String))
		
		connPool(dsName,dsURL,dsDriverName,dsPassword,dsUserName)
		
		#Set Connection Pool specific parameters
		cd(RESOURCE+'/JDBCConnectionPoolParams/'+dsName)
		cmo.setTestConnectionsOnReserve(true)
		cmo.setTestTableName(dsTestQuery)
		
		cd(RESOURCE+'/JDBCDataSourceParams/'+dsName)
		
		if(isXA=='true'):
			cmo.setGlobalTransactionsProtocol('TwoPhaseCommit')
		else:
			cmo.setGlobalTransactionsProtocol('None')
			
		cd('/SystemResources/'+dsName)
		list=[]
		M=1
		while(M <= int(total_servers)):
			print"in mode"
			s='com.bea:Name='+datasourceTarget+str(M)+',Type=Server'
			print("targets :"+s)
                        list.append(ObjectName(str(s)))
			M=M+1
		set('Targets',jarray.array(list, ObjectName))
		#set('Targets',jarray.array([ObjectName('com.bea:Name='+datasourceTarget+',Type=Cluster')],ObjectName))
		#set('Targets',jarray.array([ObjectName('com.bea:Name='+datasourceTarget+',Type=Server')],ObjectName))
		print("datasourceTarget : "+datasourceTarget)
		save();
	except:
		print('--> something went wrong, bailing out')
                stopEdit('y')	

def getJDBCModule(dsName,allJDBCResources):
	print "in getJDBCModule mode"
	for jdbcResource in allJDBCResources:
		JDBC_Mod = str(jdbcResource.getName())
		print ("in JDBC_Mod mode-->"+JDBC_Mod)
		if JDBC_Mod == dsName:
			print ("in jdbc mode"+JDBC_Mod)
			return False
	return True


def main(args):
	try:
		envproperty=""
		validate_inputs(args)
		envproperty=args[1]
		wls_username=args[2]
		wls_password=args[3]
		url=args[4]
		propInputStream = FileInputStream(envproperty)
		configProps = Properties()
		configProps.load(propInputStream)
		uniqueString ='123456'
		uniqueString = str(int(time.time()))

		connect(wls_username,wls_password,url)
		edit()
		planPath = get('/AppDeployments/AqAdapter/PlanPath')
                appPath = get('/AppDeployments/AqAdapter/SourcePath')

		total_jdbcDS=configProps.get("total_jdbcDS")
		total_servers=configProps.get("total_servers")  
		print("Total count :"+total_jdbcDS)
		allJDBCResources = cmo.getJDBCSystemResources()
		j=1
		while (j <= int(total_jdbcDS)):
			print("J-->"+str(j))
			dsName=configProps.get("datasource.name"+str(j))
			#dsDatabaseName=configProps.get("datasource.database.name"+str(j))
			print("dsName"+dsName)
			JDBC = getJDBCModule(dsName,allJDBCResources)
			print("step 1")
			
			if JDBC == True:
			
				dsJNDIName=configProps.get(dsName+'.jndiname')
				dsDriverName=configProps.get(dsName+'.driver.class')
				dsURL=configProps.get(dsName+'.url')
				dsUserName=configProps.get(dsName+'.username')
				dsPassword=configProps.get(dsName+'.password')
				dsTestQuery=configProps.get(dsName+'.test.query')
				dbType=configProps.get(dsName+'.dbType')
				isXA=str(configProps.get(dsName+'.isXA'))
				datasourceTarget=configProps.get("targetservers")
				print "testin1"
				createJDBCDataSource(dsName,datasourceTarget,dsJNDIName,dsDriverName,dsURL,dsUserName,dsPassword,dsTestQuery,isXA,dbType,total_servers)

				noofoutboundconn=configProps.get(dsName+'.noofoutboundconn')
				print("noofoutboundconn-->"+noofoutboundconn)
				i=1
				while (i <= int(noofoutboundconn)):
					uniqueString=uniqueString+str(i)
					print("XXXXXXXXXXX")
					eisName=configProps.get(dsName+'.eisName'+str(i))
					print("xxxx->"+eisName)
					PltClasName=configProps.get(dsName+'.platformClassName'+str(i))	
					print("xxxx->"+PltClasName)
					#Creating a AqAdapter JNDI...
					if(eisName==''):
						print('JNDI name not provided...Outbound connection name will not be created...')
					else:
						print("inside dbdapter")
						createDbAdapterJNDI(dsName,eisName,dsJNDIName,isXA,planPath,appPath,uniqueString,dbType,PltClasName)
						print('--> done')
					i = i+1
				save()
				activate(block='true')	
				print('activation done')
			else:
				dsJNDIName=configProps.get(dsName+'.jndiname')
				dbType=configProps.get(dsName+'.dbType')
				isXA=str(configProps.get(dsName+'.isXA'))
				datasourceTarget=configProps.get("targetservers")
				print "testin1"
				noofoutboundconn=configProps.get(dsName+'.noofoutboundconn')
				print("noofoutboundconn-->"+noofoutboundconn)
				i=1
				while (i <= int(noofoutboundconn)):
					uniqueString=uniqueString+str(i)
					print("XXXXXXXXXXXelase")
					eisName=configProps.get(dsName+'.eisName'+str(i))
					print("xxxxelese->"+eisName)
					PltClasName=configProps.get(dsName+'.platformClassName'+str(i))	
					print("xxxxelse->"+PltClasName)
					#Creating a AqAdapter JNDI...
					if(eisName==''):
						print('JNDI name not provided...Outbound connection name will not be created...')
					else:
						print("inside dbdapter_else")
						createDbAdapterJNDI(dsName,eisName,dsJNDIName,isXA,planPath,appPath,uniqueString,dbType,PltClasName)
						print('--> done')
			
					i = i+1				
			j = j+1
		print("out-")
		cd('/AppDeployments/AqAdapter/Targets')
		print('--> redeploying the AqAdapter')
		redeploy('AqAdapter', planPath, targets=cmo.getTargets())
		print('--> redeploy done')
		print('--> Completed')

	except:
		print('Error Occured Unable to continue')
		dumpStack()

main(sys.argv)
