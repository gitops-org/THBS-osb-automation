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

		domainName=configProps.get("domain.name")
		print("domain : "+domainName)

		connect(wls_username,wls_password,url)
		
		edit()
		startEdit()
		
		total_multiDS=configProps.get("total_multiDS")
		total_servers=configProps.get("total_servers")

		i=1
		while(i<=int(total_multiDS)):
			mdsName=configProps.get("mds_name"+str(i))
			print("Multi DS :"+mdsName)
			mdsJndiName=configProps.get("mds_jndiname"+str(i))
			algorithmType=configProps.get("mds_algorithmType"+str(i))
			dataSourceList=configProps.get("mds_dslist"+str(i))
			print(dataSourceList)
			
			
			cd('/')
			# creates a MultiDataSource named .MDS1.
			cmo.createJDBCSystemResource(mdsName)
			cd('/JDBCSystemResources/'+mdsName+'/JDBCResource/'+mdsName)
			cmo.setName(mdsName)
			cd('/JDBCSystemResources/'+mdsName+'/JDBCResource/'+mdsName+'/JDBCDataSourceParams/'+mdsName)

			# sets the JNDI name of the multi datasource to 'MDS1'
			set('JNDINames',jarray.array([String(mdsJndiName)], String))
			print algorithmType
			# sets the algorithm type to failover
			# Refer this link for valid values
			cmo.setAlgorithmType(algorithmType)

			# IMPORTANT -> Adds two datasources 'DS1' and 'DS2' to the multi datasource
			cmo.setDataSourceList(dataSourceList)
			cd('/JDBCSystemResources/'+mdsName)

			totalTargets=configProps.get("total_servers")
			Targets_server=configProps.get("Targets_server")
			print Targets_server
			list=[]
			M=1
			while(M <= int(totalTargets)):
				print"in mode"
				s='com.bea:Name='+Targets_server+str(M)+',Type=Server'
				print("targets :"+s)
                                list.append(ObjectName(str(s)))
				M=M+1
			set('Targets',jarray.array(list, ObjectName))
			save();
			i=i+1
		save();
		print('--> activating changes')
		activate(block='true')
		print('--> Completed')

	except:
		print('Error Occured Unable to continue')
		dumpStack()

main(sys.argv)
