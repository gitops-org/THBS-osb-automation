(:: pragma bea:global-element-parameter parameter="$companionMessage" element="ns2:companionMessage" location="../../SouthBoundInterfaces/cuk/ICD375/SOA_WMQIServices.xsd" ::)
(:: pragma bea:global-element-return element="ns3:getInsuranceDetails_1Response" location="../../NorthBoundInterfaces/managepostpayinsurancedata_1_0.xsd" ::)

(:: # Date #     # Version #        # Author #          # Change Description # :)
(:: 2/02/2017         1.0.0             Jagadish.G             Initial version :)

declare namespace ns2 = "http://WMQIServices.eai.o2c.ibm.com";
declare namespace ns1 = "http://CommonCompanionElements.eai.o2c.ibm.com";
declare namespace ns4 = "http://gentypes.eai.o2c.ibm.com";
declare namespace ns3 = "http://soa.o2.co.uk/managepostpayinsurancedata_1";
declare namespace ns0 = "http://products.eai.o2c.ibm.com";
declare namespace ns5 = "http://companion.eai.o2c.ibm.com";
declare namespace xf = "http://tempuri.org/PublishBBProvisionigEvent_1_0/transformations/test/";

declare function xf:test($companionMessage as element(ns2:companionMessage))
    as element(ns3:getInsuranceDetails_1Response) {
        <ns3:getInsuranceDetails_1Response>
            <ns3:insuranceDetails>
            {
                for $insuranceStatus in $companionMessage/ns2:utilGetInsuranceStatusResp/ns2:insuranceStatus
                return
                <ns3:insuranceDetail>
                    <ns3:productID>{ data($insuranceStatus/ns5:productId) }</ns3:productID>
                   {
                   if(data($insuranceStatus/ns1:accountNumber)) then
                   <ns3:accountNumber>{ data($insuranceStatus/ns1:accountNumber) }</ns3:accountNumber>
                   else ""
                   }       
                   <ns3:insuranceCategory>{ data($insuranceStatus/ns5:insuranceCategory) }</ns3:insuranceCategory>
                   <ns3:imei>{ data($insuranceStatus/ns5:insuranceImei) }</ns3:imei>
                   {
                   if(data($insuranceStatus/ns5:handsetMake))then
                    <ns3:handsetMake>{ data($insuranceStatus/ns5:handsetMake) }</ns3:handsetMake>
                   else ""
                   }
                   {
                   if(data($insuranceStatus/ns5:handsetModel))then
                     <ns3:handsetModel>{ data($insuranceStatus/ns5:handsetModel) }</ns3:handsetModel>
                      else ""
                   }
                    
                   {
                   if(data($insuranceStatus/ns5:commercialInsurancePolicyName)) then
                   <ns3:insurancePolicyName>{ data($insuranceStatus/ns5:commercialInsurancePolicyName) }</ns3:insurancePolicyName>
                   else ""
                   }
                   <ns3:insuranceStartTimestamp>{ data($insuranceStatus/ns5:insuranceStartTimestamp) }</ns3:insuranceStartTimestamp>
                   {
                   if(data($insuranceStatus/ns5:insuranceEndTimestamp) )then
                   <ns3:insuranceEndTimestamp>{ data($insuranceStatus/ns5:insuranceEndTimestamp) }</ns3:insuranceEndTimestamp>
                   else ""
                   }
                   {
                   if( data($insuranceStatus/ns5:insuranceCancelRequestTimestamp))then
                   <ns3:insuranceCancelRequestTimestamp>{ data($insuranceStatus/ns5:insuranceCancelRequestTimestamp) }</ns3:insuranceCancelRequestTimestamp>
                   else ""
                   }
                           
                    
                </ns3:insuranceDetail>
                }
            </ns3:insuranceDetails>
        </ns3:getInsuranceDetails_1Response>
};

declare variable $companionMessage as element(ns2:companionMessage) external;

xf:test($companionMessage)