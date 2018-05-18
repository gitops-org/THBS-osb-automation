package com.javatpoint;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.util.Scanner;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;

public class ApacheHttpClientPost {

    public static void main(String[] args) {
        String path="C:/Users/girish_mohan/Downloads/datasam.txt", filecontent="";
        ApacheHttpClientPost apacheHttpClientPost = new ApacheHttpClientPost();
        try {
            DefaultHttpClient httpClient = new DefaultHttpClient();
            HttpPost postRequest = new HttpPost("http://172.30.64.36:9200/application-2018.01.08/_search");
            //http://172.30.64.36:9200/application-2018.01.08/_search
            //http://localhost:9200/versioneg/message/_percolate
            System.out.println(postRequest.toString());
            filecontent=apacheHttpClientPost.readFileContent(path);
           // System.out.println(filecontent);
            StringEntity input = new StringEntity(filecontent);
            input.setContentType("application/json");
            postRequest.setEntity(input);
            HttpResponse response = httpClient.execute(postRequest);
            if (response.getStatusLine().getStatusCode() != 200) {
                throw new RuntimeException("Failed : HTTP error code : " + response.getStatusLine().getStatusCode());
            }
            BufferedReader br = new BufferedReader(new InputStreamReader((response.getEntity().getContent())));
            String output;
            System.out.println("Output from Server .... \n");
            while ((output = br.readLine()) != null) {

                System.out.println(output);
            }
            httpClient.getConnectionManager().shutdown();
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
       
        
        
        /*try {

    		DefaultHttpClient httpClient = new DefaultHttpClient();
    		HttpGet getRequest = new HttpGet("http://172.30.64.36:9200/application-2018.01.08/_search?");
    		getRequest.addHeader("accept", "application/json");

    		HttpResponse response = httpClient.execute(getRequest);

    		if (response.getStatusLine().getStatusCode() != 200) {
    			throw new RuntimeException("Failed : HTTP error code : "
    			   + response.getStatusLine().getStatusCode());
    		}

    		BufferedReader br = new BufferedReader(
                             new InputStreamReader((response.getEntity().getContent())));

    		String output;
    		System.out.println("Output from Server .... \n");
    		while ((output = br.readLine()) != null) {
    			System.out.println(output);
    		}

    		httpClient.getConnectionManager().shutdown();

    	  } catch (ClientProtocolException e) {

    		e.printStackTrace();

    	  } catch (IOException e) {

    		e.printStackTrace();
    	  }*/

    }

    private String readFileContent(String pathname) throws IOException {

        File file = new File(pathname);
        StringBuilder fileContents = new StringBuilder((int)file.length());
        Scanner scanner = new Scanner(file);
        String lineSeparator = System.getProperty("line.separator");

        try {
            while(scanner.hasNextLine()) {        
                fileContents.append(scanner.nextLine() + lineSeparator);
            }
            return fileContents.toString();
        } finally {
            scanner.close();
        }
    }
}