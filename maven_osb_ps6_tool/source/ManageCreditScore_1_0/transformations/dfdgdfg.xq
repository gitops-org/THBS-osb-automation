(:: pragma bea:global-element-parameter parameter="$updateCreditScoreResponse" element="ns0:updateCreditScoreResponse" location="../../SouthBoundInterfaces/manageCreditScore/managecreditscoredata_1_0.xsd" ::)
(:: pragma bea:global-element-return element="ns1:updateCreditScoreResponse" location="../../NorthBoundInterfaces/managecreditscoredata_1_0.xsd" ::)

declare namespace ns1 = "http://soa.three.ie/managecreditscoredata_1_0";
declare namespace ns0 = "http://soa.o2.ie/adapter/services/managecreditscoredata_1_0";
declare namespace xf = "http://tempuri.org/ManageCreditScore_1_0/transformations/dfdgdfg/";

declare function xf:dfdgdfg($updateCreditScoreResponse as element(ns0:updateCreditScoreResponse),$incomingRequest as element(*))
    as element(ns1:updateCreditScoreResponse) {
        <ns1:updateCreditScoreResponse>
            <ns1:accountNumber>{ data($incomingRequest/ns1:updateCreditScore/ns1:accountNumber) }</ns1:accountNumber>
        </ns1:updateCreditScoreResponse>
};

declare variable $updateCreditScoreResponse as element(ns0:updateCreditScoreResponse) external;
declare variable $incomingRequest as element(*) external;

xf:dfdgdfg($updateCreditScoreResponse,$incomingRequest)
