@testcase
Feature: sample karate test script that includes SOAP calls
    to the following demo service:
  http://soaref.ref.o2.co.uk/services/sdp/Spa_2_0?wsdl


Background:
Given url 'http://soaref.ref.o2.co.uk/services/sdp/Spa_2_0?wsdl'

Scenario: Get Service Provider Categories
Given request 
"""
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:spad="http://soa.o2.co.uk/sdp/spadata_2" xmlns:cor="http://soa.o2.co.uk/coredata_1">
<soapenv:Header>
<cor:debugFlag>true</cor:debugFlag>
</soapenv:Header>
<soapenv:Body>
<spad:getServiceProviderCategories>
<spad:msisdn>447804311160</spad:msisdn>
<!--Optional:-->
</spad:getServiceProviderCategories>
</soapenv:Body>
</soapenv:Envelope>

"""
And configure ssl = { keyStore: 'classpath:certstore.pfx', keyStorePassword: 'certpassword', keyStoreType: 'pkcs12' };
# soap action performed
When soap action 'http://localhost:8000/services/sdp/Spa_2_0'

#setting the actual values
And def expectedCode = 'SPA0000S'
And def expectedDescription = 'The request is completed successfully'
And def expectedSpidDescription = 'O2 (UK) Limited - DISE'
And def expectedSpid = '535'
And def expectedPaymentType = 'POSTPAY'
And def expectedCategory = 'O2 CORPORATE DISE'
And def expectedStatus = 'A'
And def expectedOperatorID = 'O2'

#SOA transactionId null check  

Then def res = response/Envelope/Header/SOATransactionID
And assert res != null

# checking the actual code with expected code
And def actualCode = response/Envelope/Body/getServiceProviderCategoriesResponse/code
And match actualCode == expectedCode

#checking the description
And def actualDescription = response/Envelope/Body/getServiceProviderCategoriesResponse/description
And match actualDescription == expectedDescription

#checking the spidDescription
And def actualSpidDescription = response/Envelope/Body/getServiceProviderCategoriesResponse/spidDescription
And match actualSpidDescription == expectedSpidDescription

#checking the spid
And def actualSpid = response/Envelope/Body/getServiceProviderCategoriesResponse/spid
And match actualSpid == expectedSpid

#checking the paymentType
And def actualPaymentType = response/Envelope/Body/getServiceProviderCategoriesResponse/paymentType
And match actualPaymentType == expectedPaymentType

#checking the category
And def actualCategory = response/Envelope/Body/getServiceProviderCategoriesResponse/category
And match actualCategory == expectedCategory

#checking the status
And def actualStatus = response/Envelope/Body/getServiceProviderCategoriesResponse/status
And match actualStatus == expectedStatus

#checking the OperatorID
And def actualOperatorID = response/Envelope/Body/getServiceProviderCategoriesResponse/operatorID
And match actualOperatorID == expectedOperatorID
