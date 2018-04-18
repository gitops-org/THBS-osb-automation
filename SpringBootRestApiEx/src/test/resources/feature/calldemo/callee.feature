Feature: Demo for call

Background:

Given url  'http://localhost:8083/SpringBootRestApi/api/user/1'



  @ByName
  Scenario: Get By Name
    When method get
    Then status 200
    And def name = response


 