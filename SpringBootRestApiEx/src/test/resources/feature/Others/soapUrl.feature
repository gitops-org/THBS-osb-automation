@soapUrl
Feature: sample karate test script that includes SOAP calls
    to the following demo service:
    http://www.webservicex.com/stockquote.asmx?op=GetQuote


Background:
Given url 'http://www.webservicex.net/BibleWebservice.asmx'


Scenario: soap 1.1
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.webserviceX.NET">
   <soapenv:Header/>
   <soapenv:Body>
      <web:GetBookTitles/>
   </soapenv:Body>
</soapenv:Envelope>
"""
When soap action 'http://www.webserviceX.NET/GetBookTitles'
Then status 200
And def last = //GetBookTitlesResult












