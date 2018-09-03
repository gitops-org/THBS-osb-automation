(:: pragma bea:global-element-parameter parameter="$updateCreditScore1" element="ns1:updateCreditScore" location="../../NorthBoundInterfaces/managecreditscoredata_1_0.xsd" ::)
(:: pragma  parameter="$configXML" type="anyType" ::)
(:: pragma bea:global-element-return element="ns0:updateCreditScore" location="../../SouthBoundInterfaces/manageCreditScore/managecreditscoredata_1_0.xsd" ::)

declare namespace ns1 = "http://soa.three.ie/managecreditscoredata_1_0";
declare namespace ns0 = "http://soa.o2.ie/adapter/services/managecreditscoredata_1_0";
declare namespace xf = "http://tempuri.org/ManageCreditScore_1_0/transformations/ManageCreditScoreRequest/";

declare function xf:ManageCreditScoreRequest($updateCreditScore1 as element(ns1:updateCreditScore),
    $configXML as element(*))
    as element(ns0:updateCreditScore) {
        <ns0:updateCreditScore>
            <ns0:accountNumber>{ data($updateCreditScore1/ns1:accountNumber) }</ns0:accountNumber>
            <ns0:creditScoreDetails>
                <ns0:serviceCategory>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:serviceCategory) }</ns0:serviceCategory>
                <ns0:decisionCode>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:decisionCode) }</ns0:decisionCode>
                <ns0:score>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:score) }</ns0:score>
                <ns0:numberofDevices>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:numberofDevices) }</ns0:numberofDevices>
                <ns0:externalRefNumber>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:externalRefNumber) }</ns0:externalRefNumber>
                <ns0:agentID>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:agentID) }</ns0:agentID>
                <ns0:isInternationalRoaming>{ data($updateCreditScore1/ns1:creditScoreDetails/ns1:isInternationalRoaming) }</ns0:isInternationalRoaming>
            </ns0:creditScoreDetails>
        </ns0:updateCreditScore>
};

declare variable $updateCreditScore1 as element(ns1:updateCreditScore) external;
declare variable $configXML as element(*) external;

xf:ManageCreditScoreRequest($updateCreditScore1,
    $configXML)
