<?xml version="1.0" encoding="UTF-8"?>
<WebServiceRequestEntity>
   <description></description>
   <name>manageCreditScore</name>
   <tag></tag>
   <elementGuidId>4582557c-e845-4ce2-bfd5-0e8a08a495b4</elementGuidId>
   <selectorMethod>BASIC</selectorMethod>
   <useRalativeImagePath>false</useRalativeImagePath>
   <httpBody></httpBody>
   <httpBodyContent></httpBodyContent>
   <httpBodyType></httpBodyType>
   <restRequestMethod></restRequestMethod>
   <restUrl></restUrl>
   <serviceType>SOAP</serviceType>
   <soapBody>&lt;soapenv:Envelope 	xmlns:soapenv=&quot;http://schemas.xmlsoap.org/soap/envelope/&quot; xmlns:man=&quot;http://soa.three.ie/managecreditscoredata_1_0&quot;>
&lt;soapenv:Header>
&lt;cor:debugFlag xmlns:cor=&quot;http://soa.o2.ie/coredata_1_0&quot;>true&lt;/cor:debugFlag>
&lt;/soapenv:Header>soapenv:Header>
&lt;soapenv:Body>
&lt;man:updateCreditScore>
&lt;man:accountNumber>289108781&lt;/man:accountNumber>
&lt;man:creditScoreDetails>
&lt;man:serviceCategory>voice&lt;/man:serviceCategory>
&lt;man:decisionCode>RECOMMENDED DEPOSIT&lt;/man:decisionCode>
&lt;man:score>1&lt;/man:score>
&lt;man:numberofDevices>20&lt;/man:numberofDevices>
&lt;man:externalRefNumber>4&lt;/man:externalRefNumber>
&lt;man:agentID>1226&lt;/man:agentID>
&lt;man:isInternationalRoaming>true&lt;/man:isInternationalRoaming>
&lt;/man:creditScoreDetails>
&lt;/man:updateCreditScore>
&lt;/soapenv:Body>
&lt;/soapenv:Envelope>
</soapBody>
   <soapHeader></soapHeader>
   <soapRequestMethod>SOAP</soapRequestMethod>
   <soapServiceFunction>updateCreditScore</soapServiceFunction>
   <verificationScript>import static org.assertj.core.api.Assertions.*

import com.kms.katalon.core.testobject.ResponseObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS
import com.kms.katalon.core.webservice.verification.WSResponseManager

import groovy.json.JsonSlurper
import internal.GlobalVariable as GlobalVariable
</verificationScript>
   <wsdlAddress>http://localhost:7001/services/managecreditscore_1_0?wsdl</wsdlAddress>
</WebServiceRequestEntity>
