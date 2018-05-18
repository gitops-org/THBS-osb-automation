/**
 * 
 */
package com.javatpoint;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Collections;

import org.apache.http.HttpEntity;
import org.apache.http.HttpHost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.util.EntityUtils;
import org.elasticsearch.client.Response;
import org.elasticsearch.client.RestClient;
/**
 * @author girish_mohan
 *
 */
public class HttpPostforElasticSearch {
	
	public static void main(String [] args) throws IOException, ParseException {
		
		RestClient restClient = RestClient.builder(new HttpHost("172.30.64.36", 9200, "http")).build();
				                         
		HttpEntity entity1 = new StringEntity(
				"{\n" +
						"	\"_source\": { \n" +		
					    "    \"includes\": [ \"SOATransactionID\", \"processName\",\"logtime1\",\"Response_time\" ] \n" +
					    "}, \n" +
					  
					  "    \"query\" : {\n" +
							"	\"match\": { \n" +
							"	\"eventType\": { \n" +
							"	\"query\": \"END\" \n" +
					      "} \n " +
					    "} \n " +
					  "} \n " +
					"} \n " 
				, ContentType.APPLICATION_JSON);
				
				Response response = restClient.performRequest("POST", "/application-2018.01.05/_search?pretty=true&filter_path=hits.hits._source",Collections.singletonMap("pretty", "true"), entity1);

				String str = EntityUtils.toString(response.getEntity());
				storeOutput(str);
				
	}
	

	public static void storeOutput(String str) throws IOException, ParseException {

		AGLogBean ab = new AGLogBean();
		String [] strArr = str.split("\\[|\\]|\\{|\\}");
		for (int i = 0; i < strArr.length; i++) {
			PrintWriter out = new PrintWriter(new FileWriter("D:\\AGLOGS\\ResultLogs.log", true), true);	

			if (strArr[i].contains("SOATransactionID")) {
				String s = strArr[i];
				
				String[] reg = s.split(",");
				for (int j = 0; j < reg.length; j++) {

					String res1 = reg[0].substring(reg[0].indexOf(":")+1, reg[0].length());
					ab.setSoaTransactionID(res1.trim().replaceAll("\"" , ""));
					
					String res2 = reg[1].substring(reg[1].indexOf(":")+1, reg[1].length());
					ab.setProcessName(res2.trim().replaceAll("\"" , ""));
					
					String res3 = reg[2].substring(reg[2].indexOf(":")+1, reg[2].length());
					ab.setAgLogTime(setDateParsing(res3.trim().replaceAll("\"" , "")));
					
					String res4 = reg[3].substring(reg[3].indexOf(":")+1, reg[3].length());
					ab.setResponseTime(Float.parseFloat(res4.trim()));
				}
					  
				      out.write("Jan 12 05:53:06 highgate-mnt "+ab.getAgLogTime()+" [info][O2AccessGateway][O2AccessGatewayWebServicesCustomer][response] tid:(521542039) |"
				      		+ " SOATransactionID: "+ab.getSoaTransactionID()+" |"
				      		+ " SOAConsumerTransactionID: 10cced4a-18fd-476c-899a-0789b315ced0 |"
				      		+ " providerID: o2 | applicationID: opp | originatorIP: 52.50.134.247 |"
				      		+ " Operation: "+ab.getProcessName().substring(ab.getProcessName().indexOf(".")+1,ab.getProcessName().length())+" |"
				      		+ " Destination: http://soaaccessnewvip.london.02.net:80/services/"+ab.getProcessName()+" |"
				      		+ " Time Elapsed: "+ab.getResponseTime()+ System.getProperty( "line.separator" ));
				      out.close();
			}
			
		}
		
	}

	public static String setDateParsing(String date) throws ParseException {
		DateFormat mSDF = new SimpleDateFormat("E: MMM dd yyyy HH:mm:ss.S");
		SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.S");
		return mSDF.format(formatter.parse(date));
	}
}
