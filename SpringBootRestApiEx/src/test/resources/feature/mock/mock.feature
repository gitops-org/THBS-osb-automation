Feature: Demo for mocking a service

Background:
#Given url 'http://localhost:8083/SpringBootRestApi/api/user/1'

#mocking a service URL
Given url baseUrl + 'user/1'

And def UserService = Java.type('com.websystique.springboot.service.UserServiceImpl')
  Scenario: Get By Name
    When method get
    Then status 200
    And def list = new UserService().findAllUsers();
    #And print list
    And match list == '[User [id=1, name=Sam, age=30, salary=70000.0], User [id=2, name=Tom, age=40, salary=50000.0], User [id=3, name=Jerome, age=45, salary=30000.0], User [id=4, name=Silvia, age=50, salary=40000.0]]'
  # mocking the Service
   And def created = response
  And print '******************************************************************' + created.name
  And match created.name == 'Sam'
