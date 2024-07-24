*   KEY\_NOT\_FOUND
*   ACCESS\_DENIED
*   API\_INVALID
*   CLIENT\_INVALID
*   METHOD\_NOT\_SUPPORTED
*   MEDIA\_TYPE\_NOT\_ACCEPTABLE

March 3, 2020
=============

Online payments
---------------

*   Removed the following parameters from the **pay**, **notifyPayment**, **inquiryPayment**, and **refund** interfaces:

*   totalSettlementAmount
*   settlementQuote

In-store payments
-----------------

*   Updated the following parameter for the **pay**, **notifyPayment**, **inquiryPayment**, and **refund** interfaces:

*   Modified _totalSettlementAmount_ to _grossSettlementAmount_

February 25, 2020
=================

Online payments & In-store payments
-----------------------------------

*   Added the following parameters to the response of the **pay**, **inquiryPayment**, and **refund** interfaces:

*   totalSettlementAmount
*   settlementQuote

*   Added the following parameters to the request of the **notifyPayment** interface:

*   totalSettlementAmount
*   settlementQuote