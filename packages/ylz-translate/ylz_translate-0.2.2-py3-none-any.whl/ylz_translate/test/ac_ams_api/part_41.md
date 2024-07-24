*   Request parameters:

*   paymentMethod.paymentMethodId
*   env
*   env.terminalType
*   settlementStrategy.settlementCurrency

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   INVALID\_MERCHANT\_STATUS
*   MERCHANT\_KYB\_NOT\_QUALIFIED
*   USER\_PAYMENT\_VERIFICATION\_FAILED

*   Removed the following error codes:

*   USER\_NOT\_EXIST
*   ORDER\_NOT\_EXIST

**Updated** **the** **_notifyPayment_** **document:**

*   Removed the following fields:

*   Request parameters:

*   notifyType: OFFLINE\_PAYMENT\_CODE
*   result.resultStatus: U

*   Modified the following fields from Optional to Required:

*   Request parameters:

*   paymentCreateTime
*   paymentId
*   result.resultMessage

*   Added the error codes of _pay (Cashier Payment)_ and _pay (Auto Debit)_.

**Updated** **the** **_inquiryPayment_** **document:**

*   Removed the following fields:

*   Response parameters: