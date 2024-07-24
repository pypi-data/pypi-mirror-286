*   authExpiryTime
*   redirectActionForm
*   transaction.transactionType: PAYMENT, CANCEL, AUTHORIZATION, CAPTURE, VOID
*   transactionTime

*   Modified the following fields from Optional to Required:

*   Response parameters:

*   result
*   result.resultMessage
*   transactions.transactionId

*   Added the following two result codes tables:

*   Payment result codes
*   Transaction result codes

*   Removed the following error codes:

*   RISK\_REJECT
*   USER\_KYC\_NOT\_QUALIFIED

**Updated** **the** **_cancel_** **document:**

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

**Updated** **the** **_refund_** **document:**

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   INVALID\_MERCHANT\_STATUS
*   ORDER\_IS\_CLOSED  
    

**Updated** **the** **_inquiryR_****_efund_** **document:**