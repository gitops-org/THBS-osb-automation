Feature: Demo for mocking a service
Background:
Given url 'http://localhost:8083/SpringBootRestApi/api/user/'
And def UserService = Java.type('com.websystique.springboot.service.UserServiceImpl')

 Scenario: Get By Name
    When method get
    Then status 200
Given table data =
  | id | name | age | salary  |
  |  1 | Sam  | 30  | 70000.0 |
  |  2 | Tom  | 40  | 50000.0 |
  |  3 |Jerome| 45  | 30000.0 |
  |  4 |Silvia| 50  | 40000.0 |
    
And def result = new UserService().findAllUsers();
And def created = response
And print '******************************************************************' + created
#for each iterating through the data
And match each response == { id: '#number', name: '#string',age: '#number',salary: '#number' }
And match response[*].name contains ['Sam', 'Tom','Jerome']

 
Scenario Outline: 1.4
Given url 'http://localhost:8083/SpringBootRestApi/api/user/1'
When method get
Then print response
And def created = response
And print '******************************************************************************************'+created.name
#And assert response[0].salary == <salary>
And match created.salary contains <salary>
Examples:
| id | name | age | salary  |
|  1 | Sam  | 30  | 70000.0 |


 