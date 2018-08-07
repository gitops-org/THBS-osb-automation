from java.io import FileInputStream

propInputStream = FileInputStream("/home/oracle/automation/DB/MDSdetails.properties")
configProps = Properties()
configProps.load(propInputStream)

domainName=configProps.get("domain.name")
adminURL=configProps.get("admin.url")
adminUserName=configProps.get("admin.userName")
adminPassword=configProps.get("admin.password")

connect(adminUserName, adminPassword, adminURL)
edit()

total_multiDS=configProps.get("total_multiDS")

i=1
while(i<=int(total_multiDS)):
        mdsName=configProps.get("mds_name"+str(i))
        print("Multi DS :"+mdsName)
        mdsJndiName=configProps.get("mds_jndiname"+str(i))
        algorithmType=configProps.get("Load-Balancing")
        dataSourceList=configProps.get("mds_dslist"+str(i))
        print(dataSourceList)

        startEdit()
        cd('/')
        # creates a MultiDataSource named .MDS1.
        cmo.createJDBCSystemResource(mdsName)
        cd('/JDBCSystemResources/'+mdsName+'/JDBCResource/'+mdsName)
        cmo.setName(mdsName)
        cd('/JDBCSystemResources/'+mdsName+'/JDBCResource/'+mdsName+'/JDBCDataSourceParams/'+mdsName)

        # sets the JNDI name of the multi datasource to 'MDS1'
        set('JNDINames',jarray.array([String(mdsName)], String))

        # sets the algorithm type to failover
        # Refer this link for valid values
        cmo.setAlgorithmType(algorithmType)

        # IMPORTANT -> Adds two datasources 'DS1' and 'DS2' to the multi datasource
        cmo.setDataSourceList(dataSourceList)
        cd('/JDBCSystemResources/'+mdsName)

        totalTargets=configProps.get("mds_totalTargets"+str(i))
        j=1
        while(j<=int(totalTargets)):
                print(totalTargets)
                print("mds_target"+str(i)+"_"+str(j))
                targetCluster=configProps.get("mds_target"+str(i)+"_"+str(j))
                print(targetCluster)
                # targets the MDS Server - 'AdminServer'
                set('Targets',jarray.array([ObjectName('com.bea:Name='+targetCluster+',Type=Cluster')], ObjectName))
                #set('Targets',jarray.array([ObjectName('com.bea:Name='+targetCluster+',Type=Server')], ObjectName))
        j=j+1

i=i+1

activate()

print('Exiting...')

exit()
