package com.javatpoint;

import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Locale;

public class Ag_log_Generator {
	
	public static void main(String args[]) throws NumberFormatException, IOException, ParseException {

		FileInputStream fstream = new FileInputStream("D:\\AGLOGS\\AG_log_input.csv");

		DataInputStream in = new DataInputStream(fstream);

		BufferedReader br = new BufferedReader(new InputStreamReader(in));

		String strLine;
		
		while ((strLine = br.readLine()) != null) {
			
			String s1[] = strLine.split(",");

			String SOATransactionID = s1[0];

			String logtime = s1[1];
			
			String Service_Operation = s1[2];
			
			String s33[] = Service_Operation.split("\\.");			
			
			String ServiceName = s33[0];
					
			String OperationName = s33[1];
			
			String ResponseTime = s1[3];
									
			//Date parsing code
			
			float timeElasped = Float.parseFloat(ResponseTime);
			
			int ResponseTime_ms = (int) (timeElasped * 1000);
			
			String string = "January 2, 2010";
			DateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.ENGLISH);
			java.util.Date date = format.parse(logtime);
			//System.out.println(date);
			;
			//Sun: Oct 22 2017 05:53:06.378
			
			SimpleDateFormat sm = new SimpleDateFormat("EEE: MMM dd yyyy HH:mm:ss.SSS");
			String strDate = sm.format(date);
			
			System.out.println("Oct 22 05:53:06 highgate-mnt "+strDate+" [info][O2AccessGateway][O2AccessGatewayWebServicesCustomer][response] tid:(521542039) | SOATransactionID: "+SOATransactionID+" | SOAConsumerTransactionID: 10cced4a-18fd-476c-899a-0789b315ced0 | providerID: o2 | applicationID: opp | originatorIP: 52.50.134.247 | Operation: "+OperationName+" | Destination: http://soaaccessnewvip.london.02.net:80/services/"+ServiceName+" | Time Elapsed: "+ResponseTime_ms);
			
			
			//System.out.println(SOATransactionID+","+logtime+","+ServiceName+","+OperationName+","+timeElasped+"--->"+ResponseTime_ms+","+date+"--->"+strDate);
			

		}

}

}