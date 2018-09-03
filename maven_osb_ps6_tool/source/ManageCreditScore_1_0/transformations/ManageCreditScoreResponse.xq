(:: pragma bea:global-element-parameter parameter="$updateCreditScore1" element="ns0:updateCreditScore" location="../../SouthBoundInterfaces/manageCreditScore/managecreditscoredata_1_0.xsd" ::)
(:: pragma bea:global-element-return element="ns1:updateCreditScoreResponse" location="../../NorthBoundInterfaces/managecreditscoredata_1_0.xsd" ::)

declare namespace ns1 = "http://soa.three.ie/managecreditscoredata_1_0";
declare namespace ns0 = "http://soa.o2.ie/adapter/services/managecreditscoredata_1_0";
declare namespace xf = "http://tempuri.org/ManageCreditScore_1_0/transformations/ManageCreditScoreResponse/";

declare function xf:ManageCreditScoreResponse($updateCreditScore1 as element(ns0:updateCreditScore))
    as element(ns1:updateCreditScoreResponse) {
        <ns1:updateCreditScoreResponse>
            <ns1:accountNumber>{ data($updateCreditScore1/ns0:accountNumber) }</ns1:accountNumber>
        </ns1:updateCreditScoreResponse>
};

declare variable $updateCreditScore1 as element(ns0:updateCreditScore) external;

xf:ManageCreditScoreResponse($updateCreditScore1)
