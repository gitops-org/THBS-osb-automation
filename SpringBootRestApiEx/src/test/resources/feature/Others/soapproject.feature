@soapUrl
Feature: sample karate test script that includes SOAP calls
    to the following demo service:
   http://172.30.64.98:7045/services/SendMessage_1_1/proxyservices/SendMessage_1_1?wsdl


Background:
Given url 'http://172.30.64.98:7045/services/SendMessage_1_1/proxyservices/SendMessage_1_1'


Scenario: soap 1.1
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sen="http://soa.o2.co.uk/sendmessagedata_1">
   <soapenv:Header/>
   <soapenv:Body>
      <sen:queryReceiptStatus>
         <sen:queryTransactionId>1</sen:queryTransactionId>
         <!--Optional:-->
         <sen:applicationReference>2</sen:applicationReference>
         <!--Optional:-->
         <sen:subMerchantId>1</sen:subMerchantId>
      </sen:queryReceiptStatus>
   </soapenv:Body>
</soapenv:Envelope>
"""
When soap action 'http://localhost:8000/services/sdp/Spa_2_0'
And def error = 'Network unreachable or Timed out or communication error'
And def res = response/Envelope/Header/SOATransactionID
And assert res != null
And def faultstring = response/Envelope/Body/Fault/faultstring
#And print res
#And print faultstring
And match faultstring == error
#And assert equals faultstring == correctString
#And match res == 'c8a2ecea-c29f-49fc-8bab-48ae9cc069a1'


Scenario: soap 2 example
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sen="http://soa.o2.co.uk/sendmessagedata_1">
   <soapenv:Header/>
   <soapenv:Body>
      <sen:queryReceiptStatus>
         <sen:queryTransactionId>1</sen:queryTransactionId>
         <!--Optional:-->
         <sen:applicationReference>2</sen:applicationReference>
         <!--Optional:-->
         <sen:subMerchantId>1</sen:subMerchantId>
      </sen:queryReceiptStatus>
   </soapenv:Body>
</soapenv:Envelope>
"""
And def expected = 'env:Server'
When soap action 'http://localhost:8000/services/sdp/Spa_2_0'
And def id = response/Envelope/Header/SOATransactionID
And assert id != null
And def actual = response/Envelope/Body/Fault/faultcode
And print actual
And match actual == expected


Scenario: soap 3 example
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sen="http://soa.o2.co.uk/sendmessagedata_1">
   <soapenv:Header/>
   <soapenv:Body>
      <sen:queryReceiptStatus>
         <sen:queryTransactionId>1</sen:queryTransactionId>
         <!--Optional:-->
         <sen:applicationReference>2</sen:applicationReference>
         <!--Optional:-->
         <sen:subMerchantId>1</sen:subMerchantId>
      </sen:queryReceiptStatus>
   </soapenv:Body>
</soapenv:Envelope>
"""
And def expected = 'env:Server'
And header Content-Type = 'application/soap+xml; charset=utf-8'
#And def expected = {soapenv:Envelope={soapenv:Header={cor:SOATransactionID=0adf65e2-f256-4cff-93c5-793c8f188ba0}, soapenv:Body={soapenv:Fault={faultcode=env:Server, faultstring=Network unreachable or Timed out or communication error, detail={ns1:queryReceiptStatusFault={xcore:SOAFaultOriginator=Route To SMSMT_QueryReceiptStatus, xcore:SOAFaultCode=sendmessage-36120-2000-F, xcore:faultDescription=Network unreachable or Timed out or communication error, xcore:faultTrace=BEA-380002:Tried all: '1' addresses, but could not connect over HTTP to server: '172.30.64.98', port: '8087', xcore:SOATransactionID=0adf65e2-f256-4cff-93c5-793c8f188ba0}}}}}}
When soap action 'http://localhost:8000/services/sdp/Spa_2_0'
And def id = response/Envelope/Header/SOATransactionID
And assert id != null
And def actual = response/Envelope/Body/Fault/faultcode 
And print actual
And match actual == expected



Scenario: soap 3 example
Given request
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sen="http://soa.o2.co.uk/sendmessagedata_1">
   <soapenv:Header/>
   <soapenv:Body>
      <sen:queryReceiptStatus>
         <sen:queryTransactionId>1</sen:queryTransactionId>
         <!--Optional:-->
         <sen:applicationReference>2</sen:applicationReference>
         <!--Optional:-->
         <sen:subMerchantId>1</sen:subMerchantId>
      </sen:queryReceiptStatus>
   </soapenv:Body>
</soapenv:Envelope>
"""
And header Content-Type = 'application/soap+xml; charset=utf-8'
#And def expected = {soapenv:Envelope={soapenv:Header={cor:SOATransactionID=0adf65e2-f256-4cff-93c5-793c8f188ba0}, soapenv:Body={soapenv:Fault={faultcode=env:Server, faultstring=Network unreachable or Timed out or communication error, detail={ns1:queryReceiptStatusFault={xcore:SOAFaultOriginator=Route To SMSMT_QueryReceiptStatus, xcore:SOAFaultCode=sendmessage-36120-2000-F, xcore:faultDescription=Network unreachable or Timed out or communication error, xcore:faultTrace=BEA-380002:Tried all: '1' addresses, but could not connect over HTTP to server: '172.30.64.98', port: '8087', xcore:SOATransactionID=0adf65e2-f256-4cff-93c5-793c8f188ba0}}}}}}
When soap action 'http://localhost:8000/services/sdp/Spa_2_0'
And  print response








