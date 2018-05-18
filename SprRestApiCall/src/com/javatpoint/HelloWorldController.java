package com.javatpoint;


import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.RestTemplate;

import com.iss.model.UserBean;

@RestController
public class HelloWorldController {
	
	final static String uri = "https://gateway.api.cloud.wso2.com:443/t/itcs3463/sunrisers/1.4.3/posts/1";
	
	@RequestMapping(value= {"/hello","/"}, method=RequestMethod.GET)
	public String helloWorld(Model model){
		
		String message="Hello Spring Boot how r u?";
		model.addAttribute("message", message);
		return message;
	}
	public static long count = 0;

	public static long startService() {
    
		return count++;
       
    }
	
	@RequestMapping(value= "/user/menu", method=RequestMethod.GET, produces="application/json")
	public ResponseEntity<UserModel> getUserMenu(){
		UserModel model = new UserModel();
		model.setFirstName("Samantha");
		model.setLastName("Akineni");
		model.setSalary(80000000);
		model.setAge(29);
		return new ResponseEntity<UserModel>(model, HttpStatus.OK);
	}
	
	
	@RequestMapping(value= "/user/details", method=RequestMethod.GET, produces="application/json")
	public static List<UserBean> getDetails() {
		List<UserBean> list = new ArrayList<UserBean>();
		list.add(new UserBean(8, "Samantha", "Actress", 50000000));
		list.add(new UserBean(10, "Anushka", "Actress", 60000000));
		list.add(new UserBean(12, "Kaleena", "Warrior", 40000000));
		list.add(new UserBean(14, "Veronica", "Princess", 50000000));
		System.out.println("server has been hit x times "+startService());
		return list;
	}
	
	@RequestMapping(value = "/user/apicall/{token}", method=RequestMethod.GET, produces="application/json")
	public static ResponseEntity<Object> hitResource(@PathVariable String token)
	{
	    
	    System.out.println(token+"**************************************************");
	    	    
	   RestTemplate restTemplate = new RestTemplate();
	     
	    ResponseEntity<Object> result = null;
		try {
			HttpHeaders headers = new HttpHeaders();
			System.out.println("inside hitResource() try");
			headers.setAccept(Arrays.asList(MediaType.APPLICATION_JSON));
			headers.setContentType(MediaType.APPLICATION_JSON);
			headers.add("client_id", "nqErbH_EDv8tJT0DHJhobE1Szaca");
			headers.add("client_secret", "yYW9usJpR00B9IQGXsJZ1gBfOzga");
			headers.add("grant_type", "client_credentials");
			headers.add("Authorization", "Bearer "+token);
			System.out.println(token+"**************************************************");
			HttpEntity<String> entity = new HttpEntity<String>("parameters", headers);
			 
			result = restTemplate.exchange(uri, HttpMethod.GET, entity, Object.class);
		}
		catch (HttpClientErrorException e) {
		      String errorDetails = e.getResponseBodyAsString();
		      return new ResponseEntity<Object>(errorDetails, HttpStatus.UNAUTHORIZED);
		    }
		System.out.println("outside hitResource() try");
	    return result;
	    
	    
	    
	}
	

	 	@RequestMapping(value = "/wso2/getAccesstoken", method = RequestMethod.GET, produces="application/json")
	 	public static String getAccessToken() throws ClientProtocolException, IOException, JSONException {
	 		String accessToken = null;
	 		HttpClient client = HttpClients.custom().build();
	 		HttpPost post = new HttpPost("https://gateway.api.cloud.wso2.com:443/token");
	 		 String line = "";
	 		System.out.println("inside getAccessToken()");
	 		try {
	 			System.out.println("inside getAccessToken() try");
	            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(1);
	            nameValuePairs.add(new BasicNameValuePair("client_id", "nqErbH_EDv8tJT0DHJhobE1Szaca"));
	            nameValuePairs.add(new BasicNameValuePair("client_secret", "yYW9usJpR00B9IQGXsJZ1gBfOzga"));
	            nameValuePairs.add(new BasicNameValuePair("grant_type", "client_credentials"));
	            post.setEntity(new UrlEncodedFormEntity(nameValuePairs));
	            HttpResponse response = client.execute(post);
	            BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
	            line = "";
	            while ((line = rd.readLine()) != null) {
	                JSONObject jsonObject = new JSONObject(line);
	                accessToken = jsonObject.getString("access_token");
	            }
	        } catch (ClientProtocolException e) {
	            e.printStackTrace();
	        }
	        System.out.println("outside catch "+accessToken);
			return accessToken;
		}
	 	
	 	///********************** method new ***********-------------------------//////////
	 	
	 	
	 	@RequestMapping(value = "/wso2/accessResource", method = RequestMethod.GET, produces="application/json")
	 	public static ResponseEntity<Object> getAccessToResourceWithoutToken() throws ClientProtocolException, IOException, JSONException {
	 		//final String resorceURL = "https://gateway.api.cloud.wso2.com:443/t/itcs3463/sunrisers/1.4.3/posts/1";
	 		System.out.println("inside resource()");
	 		RestTemplate restTemplate = new RestTemplate();
		 	ResponseEntity<Object> result = null;
		 	HttpEntity<String> entity = null;
			try {
				System.out.println("inside try block() get access");
				result = restTemplate.exchange(uri, HttpMethod.GET, entity, Object.class);
				return new ResponseEntity<Object>(result,HttpStatus.OK);
			} catch (HttpClientErrorException e) {
				// TODO Auto-generated catch block
				System.out.println("inside catch block() get access");
				e.getStatusCode();
				result= new ResponseEntity<Object>(result, HttpStatus.UNAUTHORIZED);
			}
			if (Integer.parseInt(result.getStatusCode().toString())==401) {
				System.out.println("inside if loop() get access");
				String accessToken = getAccessToken();
				result = hitResource(accessToken);
				
			}
			System.out.println("outside getAccessToResourceWithoutToken()");
			return result;
		}
	 
}



