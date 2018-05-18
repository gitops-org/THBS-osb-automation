/**
 * 
 */
package com.javatpoint;

/**
 * @author girish_mohan
 *
 */
import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.json.CDL;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class JsonToCsv {
    public static void main(String myHelpers[]){
        String jsonString = "{\"infile\": [{\"field1\": 11,\"field2\": 12,\"field3\": 13},{\"field1\": 21,\"field2\": 22,\"field3\": 23},{\"field1\": 31,\"field2\": 32,\"field3\": 33}]}";

        JSONObject output;
        try {
            output = new JSONObject(jsonString);


            JSONArray docs = output.getJSONArray("infile");

            File file=new File("C:\\Users\\girish_mohan\\Downloads\\testing.csv");
            System.out.println("Creating a new file");
            String csv = CDL.toString(docs);
            FileUtils.writeStringToFile(file, csv);
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }        
    }

}