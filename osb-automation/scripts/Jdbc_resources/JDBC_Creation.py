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
  """Create a varaible in the Plan.
  This method is used to create the variables that are needed in the Plan in order
  to add an entry for the outbound connection pool for the new data source.
  """

  try:
    wlstPlan.createVariable(name,value)
    wlstPlan.showVariables()
    variableAssignment = wlstPlan.createVariableAssignment(name,'DbAdapter.rar' , 'META-INF/weblogic-ra.xml')
    variableAssignment.setXpath(xpath)
    variableAssignment.setOrigin(origin)
    #wlstPlan.createVariable(name, value)

  except:
    print('--> was not able to create deployment plan variables successfully')



def createDbAdapterJNDI(dsName,eisName,isXA,planPath,appPath,uniqueString):
        try:
                print('--> about to update the deployment plan for the DbAdapter')
                print('--> Using plan ' + planPath)
                print('--> Using plan ' + appPath)
                plan = loadApplication(appPath, planPath)
                print('--> adding variables to plan: '+uniqueString)
                makeDeploymentPlanVariable(plan, 'ConnectionInstance_eis/DB/' + dsName + '_JNDIName_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/jndi-name')
                if(isXA=='true'):
                                makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="xADataSourceName"]/value')
                else:
                                makeDeploymentPlanVariable(plan, 'ConfigProperty_xADataSourceName_Value_' + uniqueString, eisName, '/weblogic-connector/outbound-resource-adapter/connection-definition-group/[connection-factory-interface="javax.resource.cci.ConnectionFactory"]/connection-instance/[jndi-name="' + eisName + '"]/connection-properties/properties/property/[name="DataSourceName"]/value')
                print('--> saving plan')
                plan.save();
        except:
                print('--> something went wrong, bailing out')
                stopEdit('y')


def createJDBCDataSource(dsName,dsFileName,dsDatabaseName,datasourceTarget,dsJNDIName,dsDriverName,dsURL,dsUserName,dsPassword,dsTestQuery):
        try:
                startEdit()
                cd('/')
                cmo.createJDBCSystemResource(dsName)
                print('/JDBCSystemResources/'+dsName+'/JDBCResource/'+dsName)
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
                #set('Targets',jarray.array([ObjectName('com.bea:Name='+datasourceTarget+',Type=Cluster')],ObjectName))
                set('Targets',jarray.array([ObjectName('com.bea:Name='+datasourceTarget+',Type=Server')],ObjectName))
                print("datasourceTarget : "+datasourceTarget)
                save();
        except:
                print('--> something went wrong, bailing out')
                stopEdit('y')


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

                domainName=configProps.get("domain.name")
                print("domain : "+domainName)

                connect(wls_username,wls_password,url)
                edit()
                planPath = get('/AppDeployments/DbAdapter/PlanPath')
                appPath = get('/AppDeployments/DbAdapter/SourcePath')

                total_jdbcDS=configProps.get("total_jdbcDS")
                print("Total count :"+total_jdbcDS)
                j=1
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
                        createJDBCDataSource(dsName,dsFileName,dsDatabaseName,datasourceTarget,dsJNDIName,dsDriverName,dsURL,dsUserName,dsPassword,dsTestQuery)

                        #Creating a DbAdapter JNDI...
                        if(eisName==''):
                                print('JNDI name not provided...Outbound connection name will not be created...')
                        else:
                                uniqueString=uniqueString+str(j)
                                createDbAdapterJNDI(dsName,eisName,isXA,planPath,appPath,uniqueString)
                                print('--> done')

                        j = j+1
                activate(block='true');

        except:
                print('Error Occured Unable to continue')
                dumpStack()

main(sys.argv)
