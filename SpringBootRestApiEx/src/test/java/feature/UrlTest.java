package feature;

import org.junit.runner.RunWith;
 
import com.intuit.karate.junit4.Karate;

import cucumber.api.CucumberOptions;
 
@RunWith(Karate.class)
@CucumberOptions(
	    tags = {"~@Ignore"},
	    		format = { "pretty",
	    "json:target/cucumber.json" },
	    				features = "src/test/resources/feature/table/tabledemo.feature"
	    				//features = {"classpath:feature/"}
	  //refer to Feature file
	)
public class UrlTest {
	
	/*format = { "pretty",
    "json:target/cucumber.json" }*/
	
}