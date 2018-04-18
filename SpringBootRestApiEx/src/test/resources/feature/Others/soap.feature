@soap
Feature: sample karate test script that includes SOAP calls
    to the following demo service:
    http://www.webservicex.com/stockquote.asmx?op=GetQuote

Background:
Given url 'http://www.webservicex.com/globalweather.asmx'
Scenario: soap 1.1
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.webserviceX.NET">
   <soapenv:Header/>
   <soapenv:Body>
      <web:GetCitiesByCountry>
         <!--Optional:-->
         <web:CountryName>India</web:CountryName>
      </web:GetCitiesByCountry>
   </soapenv:Body>
</soapenv:Envelope>
"""
When soap action 'http://www.webserviceX.NET/GetCitiesByCountry'
And def city = //GetCitiesByCountryResult
#And print city
And match city contains " <City>Ahmadabad</City>"


Scenario: soap 1.2
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://www.webserviceX.NET">
   <soapenv:Header/>
   <soapenv:Body>
      <web:GetCitiesByCountry>
         <!--Optional:-->
         <web:CountryName>India</web:CountryName>
      </web:GetCitiesByCountry>
   </soapenv:Body>
</soapenv:Envelope>
"""
When soap action 'http://www.webserviceX.NET/GetCitiesByCountry'
And def city = //GetCitiesByCountryResult
#And print city
And match city contains " <City>Ahmadabad</City>"



