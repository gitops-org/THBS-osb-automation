package com.javatpoint;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Locale;

import java.util.*;

import java.io.FileWriter;
import java.io.IOException;  

public class Log_gen2 {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		//int ResponseTime_ms = (int) (timeElasped * 1000);
		
		String input_date = "Tue: Jan 09 2018 03:13:20.001";		
		int log_lines = 100000;		
				
		String[] OperationNames ={"SendMessage_1_1-sendSMS","ManagePostpayTariff_2_0-getContractRevisions","ManageCreditAgreement_1_0-getCreditAgreementDetails_1","SendMessage_1_1-sendNotificationMessage_1","SendMessage_1_1-queryReceiptStatus","ManageMSISDN_1_0-getMSISDN_1","ViewConnectionStatus_1_0-getMSISDN","SendMessage_1_1-sendDynamicSMS","ManagePostpayTariff_2_0-getBusinessPolicies","ManagePostpayTariff_2_0-getValidTariffs"};
		
		
		try {
			
		//System.out.println("Output Date is ---> "+ output_date + "SOA Transaction Id--->" + uuid);
		
		FileWriter fw=new FileWriter("D:\\ag\\AG3.log");
			
		for(int i=0;i<log_lines;i++){
			
			
			String output_date = dateFunction(input_date);
			String SOATransactionID = UUID.randomUUID().toString();
			
			Random random=new Random();
			int num = random.nextInt(90) + 10;
			int ResponseTime = 2000;
			
			if(i<50000){						
			ResponseTime = ResponseTime+num;
			}
			else if(i>50000 && i<75000){
			ResponseTime = 2300;			
			ResponseTime = ResponseTime+num;				
			}
			else if(i>75000){
			ResponseTime = 400;			
			ResponseTime = ResponseTime+num;				
			}
			
			//System.out.println("Oct 22 05:53:06 highgate-mnt "+output_date+" [info][O2AccessGateway][O2AccessGatewayWebServicesCustomer][response] tid:(521542039) | SOATransactionID: "+SOATransactionID+" | SOAConsumerTransactionID: 10cced4a-18fd-476c-899a-0789b315ced0 | providerID: o2 | applicationID: opp | originatorIP: 52.50.134.247 | Operation: "+OperationName+" | Destination: http://soaaccessnewvip.london.02.net:80/services/"+ServiceName+" | Time Elapsed: "+ResponseTime);			
			//default 
			
			String ServiceName = null;			
			String OperationName = null;
			
			
			if(i<=10){
				String s33[] = OperationNames[0].split("\\-");				
				ServiceName = s33[0];				
				OperationName = s33[1];
			}			
			else {			
				int lastDigit = i % 10; 
				String s44[] = OperationNames[lastDigit].split("\\-");
				ServiceName = s44[0];				
				OperationName = s44[1];
				//System.out.println("Actual number is "+ i + " the last digit is " + lastDigit);
			}
									
			fw.write("Jan 09 05:53:06 highgate-mnt "+output_date+" [info][O2AccessGateway][O2AccessGatewayWebServicesCustomer][response] tid:(521542039) | SOATransactionID: "+SOATransactionID+" | SOAConsumerTransactionID: 10cced4a-18fd-476c-899a-0789b315ced0 | providerID: o2 | applicationID: opp | originatorIP: 52.50.134.247 | Operation: "+OperationName+" | Destination: http://soaaccessnewvip.london.02.net:80/services/"+ServiceName+" | Time Elapsed: "+ResponseTime+ System.getProperty( "line.separator" ));
			
			input_date = output_date;
						
		}
		
		fw.close(); 
		
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	private static String dateFunction(String inputdate) throws ParseException{
		
		DateFormat format = new SimpleDateFormat("EEE: MMM dd yyyy HH:mm:ss.SSS", Locale.ENGLISH);		
		Date date = format.parse(inputdate);		
		Calendar calendar = new GregorianCalendar();
		calendar.setTime(date);		
	    calendar.add(Calendar.MILLISECOND, 31);
	    Date addMilliSeconds = calendar.getTime();	    
		String newDate = format.format(addMilliSeconds);		
		return newDate;		
	}

}
