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

public class Log_Generator {

	public static void main(String[] args) throws IOException {
		// TODO Auto-generated method stub
		
		//int ResponseTime_ms = (int) (timeElasped * 1000);
		
		String input_date = "Mon: Mar 22 2018 11:00:00.000";		
		int log_lines = 1000000;		
				
		String[] OperationNames ={"ManagePostpayBoltons_2_0-getValidBoltons","ManagePostpayTariff_2_0-getContract","Subscriber_2_0-getSubscriberProfile","ViewAllowance_2_0-getNonDataAllowance_2","ManagePostpayBoltons_2_0-getCurrentAndPendingBoltons","ManageContractEligibility_2_0-getUpgradeEligibility_4","ManageOffers_1_0-getOffers","UtilGetMsisdnState_1_0-utilGetMsisdnState","ViewAllowance_2_0-getDataAllowance_1","ManageDevice_1_4-getDeviceProfile","SendMessage_1_1-sendSMS"};
		
		
		try {
			
		//System.out.println("Output Date is ---> "+ output_date + "SOA Transaction Id--->" + uuid);
		
		FileWriter fw=new FileWriter("D:\\AGLOGS\\AG.log");
			
		for(int i=0;i<log_lines;i++){
			
			
			String output_date = dateFunction(input_date);
			String SOATransactionID = UUID.randomUUID().toString();
			
			Random random=new Random();
			int num = random.nextInt(90) + 10;
			int ResponseTime = 2000;
			
			if(i<500000){						
			ResponseTime = ResponseTime+num;
			}
			else if(i>500000 && i<600000){
			ResponseTime = 2300;			
			ResponseTime = ResponseTime+num;				
			}
			else if(i>600000 && i<700000){
			ResponseTime = 2600;			
			ResponseTime = ResponseTime+num;				
			}
			else if(i>700000 && i<800000){
			ResponseTime = 2900;			
			ResponseTime = ResponseTime+num;				
			}
			else if(i>800000){
			ResponseTime = 3200;			
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
									
			fw.write("Jan 12 05:53:06 highgate-mnt "+output_date+" [info][O2AccessGateway][O2AccessGatewayWebServicesCustomer][response] tid:(521542039) | SOATransactionID: "+SOATransactionID+" | SOAConsumerTransactionID: 10cced4a-18fd-476c-899a-0789b315ced0 | providerID: o2 | applicationID: opp | originatorIP: 52.50.134.247 | Operation: "+OperationName+" | Destination: http://soaaccessnewvip.london.02.net:80/services/"+ServiceName+" | Time Elapsed: "+ResponseTime+ System.getProperty( "line.separator" ));
			
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
	    calendar.add(Calendar.MILLISECOND, 7);
	    Date addMilliSeconds = calendar.getTime();	    
		String newDate = format.format(addMilliSeconds);		
		return newDate;		
	}

}
