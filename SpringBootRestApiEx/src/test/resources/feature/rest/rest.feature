@rest
Feature: Demo Karate against Soap and Rest

Scenario: Verify that the below service list all the employees
Given url 'http://localhost:8083/SpringBootRestApi/api/user/1'
When method get
Then status 200


Scenario: Testing a POST endpoint with request body
Given url  'http://localhost:8083/SpringBootRestApi/api/user/'
And request {id:'', name:'kumarududa', age:'27', salary:'10000'}
When method POST
Then status 201
And def user = response


Scenario: Verify that the below service list all the employees
Given url 'http://localhost:8083/SpringBootRestApi/api/user/'
When method get
Then status 200

Scenario: Testing a DELETE endpoint with request body
Given url  'http://localhost:8083/SpringBootRestApi/api/user/3'
When method DELETE
And def user = response

Scenario: Verify that the below service list all the employees
Given url 'http://localhost:8083/SpringBootRestApi/api/user/'
When method get
Then status 200




