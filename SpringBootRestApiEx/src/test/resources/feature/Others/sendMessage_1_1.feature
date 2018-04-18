Feature: sample karate test script that includes SOAP calls
    to the following demo service:
   sendMessage_1_1.feature


Scenario: soap 1.2
Given def myXml =
"""
<root>
  <EntityId>a9f7a56b-8d5c-455c-9d13-808461d17b91</EntityId>
  <Name>test.pdf</Name>
  <Size>100250</Size>
  <Created>2016-12-26 03:36:17.666 PST</Created>
  <Properties/>
</root>
"""
And def documentId = myXml/root/EntityId
Then assert documentId == 'a9f7a56b-8d5c-455c-9d13-808461d17b91'
Then assert true



