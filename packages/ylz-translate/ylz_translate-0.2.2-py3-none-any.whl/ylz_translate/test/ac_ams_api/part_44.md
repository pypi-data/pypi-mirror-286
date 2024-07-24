*   Added the following error codes:

*   CLIENT\_FORBIDDEN\_ACCESS\_API
*   INVALID\_CLIENT\_STATUS
*   OAUTH\_FAILED
*   UNKNOWN\_CLIENT  
    

January 5, 2022
===============

Online payments
---------------

*   Added the _grossSettlementAmount_ and _settlementQuote_ fields in the following interfaces:

*   notifyPayment
*   inquiryPayment
*   refund
*   inquiryRefund

*   Updated the _pay_ _(Cashier Payment)_ document:
*   Added the following error codes:

*   INVALID\_MERCHANT\_STATUS
*   MERCHANT\_KYB\_NOT\_QUALIFIED
*   NO\_PAY\_OPTIONS

*   Removed the following error codes:

*   SUCCESS
*   ORDER\_NOT\_EXIST  
    

In-store payments
-----------------

*   Added the _grossSettlementAmount_ and _settlementQuote_ fields in the **inquiryRefund** interface.

**Updated** **the** **_pay (User-presented Mode Payment)_** **document****:**

*   Removed the following fields:

*   Request parameters: