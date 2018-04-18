@testcase
Feature: karate test case for O2 
  http://soaref.ref.o2.co.uk/services/sdp/Spa_2_0?wsdl


Background:
Given url 'http://172.30.64.98:7045/services/sdp/Spa_2_0?wsdl'

Scenario: Get Service Provider Categories
#passing the soap request
Given request 
"""
<soapenv:Envelope 	xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
 	<soap:Header 	xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
 	</soap:Header>
 	<soapenv:Body>
 	<spad:getServiceProviderCategories 	xmlns:spad="http://soa.o2.co.uk/sdp/spadata_2">
 	<spad:msisdn>447521127453</spad:msisdn>
 	</spad:getServiceProviderCategories>
 	</soapenv:Body>
 	
</soapenv:Envelope>

"""
# soap action performed
When soap action 'http://172.30.64.98:7045/services/sdp/Spa_2_0'

#expected outcome
And def expectedCode = 'SPA0000S'
And def expectedDescription = 'The request is completed successfully'
And def expectedSpidDescription = 'O2 (UK) Limited - CUK'
And def expectedSpid = '283'
And def expectedPaymentType = 'POSTPAY'
And def expectedCategory = 'O2 CONSUMER ONLINE'
And def expectedStatus = 'A'
And def expectedOperatorID = 'O2'

#getting the response
And def res = response/Envelope/Header/SOATransactionID
#checking for not null condition on SOATransactionID
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

When method post
Then status 200
