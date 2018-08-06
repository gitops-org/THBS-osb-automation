(:: pragma bea:global-element-parameter parameter="$getInsuranceDetails_1" element="ns3:getInsuranceDetails_1" location="../../NorthBoundInterfaces/managepostpayinsurancedata_1_0.xsd" ::)
(:: pragma  parameter="$configXML" type="anyType" ::)
(:: pragma  parameter="$incomingHeader" type="anyType" ::)
(:: pragma bea:global-element-return element="ns2:companionMessage" location="../../SouthBoundInterfaces/cuk/ICD375/SOA_WMQIServices.xsd" ::)

(:: # Date #     # Version #        # Author #          # Change Description # :)
(:: 23/01/2017         1.0.0             Jagadish.G             Initial version :)

declare namespace ns2 = "http://WMQIServices.eai.o2c.ibm.com";
declare namespace ns1 = "http://CommonCompanionElements.eai.o2c.ibm.com";
declare namespace ns4 = "http://gentypes.eai.o2c.ibm.com";
declare namespace ns3 = "http://soa.o2.co.uk/managepostpayinsurancedata_1";
declare namespace ns0 = "http://products.eai.o2c.ibm.com";
declare namespace ns5 = "http://companion.eai.o2c.ibm.com";
declare namespace xf = "http://soa.o2.co.uk/ManagePostpayInsurance_1_0/transformations/getInsuranceDetails_1_request_NBtoSB/";
declare namespace cor="http://soa.o2.co.uk/coredata_1";

declare function xf:getInsuranceDetails_1_request_NBtoSB($getInsuranceDetails_1 as element(ns3:getInsuranceDetails_1),
    $configXML as element(*),
    $incomingHeader as element(*))
    as element(ns2:companionMessage) {
        <ns2:companionMessage>
            <ns2:utilGetInsuranceStatus>
            <ns5:companionHeader>
            <ns5:channel>{data($incomingHeader/cor:applicationID)}</ns5:channel>
           
            {
				if ((fn:string-length(fn:substring-after((data($incomingHeader/cor:SOAConsumerTransactionID )),":")) <=30) and (data($incomingHeader/cor:SOAConsumerTransactionID))) then
				<ns5:userId>{fn:substring-after((data($incomingHeader/cor:SOAConsumerTransactionID)),":")}</ns5:userId>
				else if(fn:string-length(fn:substring-after((data($incomingHeader/cor:SOAConsumerTransactionID)),":")) >30) then
				<ns5:userId>{ fn:substring((fn:substring-after((data($incomingHeader/cor:SOAConsumerTransactionID)),":")),0,31) }</ns5:userId>
				else "" 
			}
            <ns5:versionId>{ data($configXML/versionId) }</ns5:versionId>
            <ns5:replyKey>{ data($incomingHeader/cor:SOATransactionID) }</ns5:replyKey>
            </ns5:companionHeader>
                <ns5:msisdn>{ concat("0",fn:substring(data($getInsuranceDetails_1/ns3:msisdn),3)) }</ns5:msisdn>
            </ns2:utilGetInsuranceStatus>
        </ns2:companionMessage>
};

declare variable $getInsuranceDetails_1 as element(ns3:getInsuranceDetails_1) external;
declare variable $configXML as element(*) external;
declare variable $incomingHeader as element(*) external;

xf:getInsuranceDetails_1_request_NBtoSB($getInsuranceDetails_1,
    $configXML,
    $incomingHeader)