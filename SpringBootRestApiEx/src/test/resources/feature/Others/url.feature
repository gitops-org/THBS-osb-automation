@url
Feature: Demo2 Karate against Rest

Background:
    Given url baseUrl
    And def url = baseUrl
    
Scenario: Verify that the below service list all the employees
Given path '/user/'
When method get
Then status 200



Scenario: Verify that the Post Request
Given path '/user/'
And request {id:'', name:'raghuvee', age:22, salary:1111}
When method POST


Scenario: Testing a POST endpoint with request body
Given url  'http://localhost:8083/SpringBootRestApi/api/user/'
And request {id:'', name:'kumi', age:'27', salary:'10000'}
When method POST
Then status 201
And def user = response


