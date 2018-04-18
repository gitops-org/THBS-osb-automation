Feature: Demo for call

Background:

Given url 'http://localhost:8083/SpringBootRestApi/api/user/1'
And def cityCall = call read('classpath:feature/calldemo/callee.feature')


  @ByName
  Scenario: Get By Name
    When method get
    Then status 200
    And def nameOfCalle = cityCall.response.name
    And def cityCallCaller = response
   # And print cityCallCaller
    Then def nameOfCaller = cityCallCaller.name
    And def nameOfCalle = nameOfCaller
    Then print nameOfCalle
    And print nameOfCaller
    And match nameOfCaller == nameOfCalle
   