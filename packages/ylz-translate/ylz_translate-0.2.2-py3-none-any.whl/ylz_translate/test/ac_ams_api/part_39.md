*   `INVALID_PAYMENT_METHOD_META_DATA`
*   `INCORRECT_BLIKCODE`
*   `SETTLE_CONTRACT_NOT_MATCH`

Updated the notifyPayment document:

*   Added the new enumeration value of `PAYMENT_PENDING` in the _notifyType_ field.

Updated the inquiryPayment document:

*   Added the new enumeration value of `PENDING` in the _paymentStatus_ field.

Updated the refund document:

*   Added the _refundNotifyUrl_ field in Request parameters.
*   Added the error code: `REFUND_IN_PROCESS`

April 1, 2022
=============

Online payments
---------------

*   Added the _merchantRegion_ field in the request parameters of the following interfaces:

*   pay (Cashier Payment)
*   consult
*   applyToken

In-store payments
-----------------

*   Added the _merchantRegion_ field in the request parameters of the following interface:

*   pay (User-presented Mode Payment)
*   pay (Order Code Payment)
*   pay (Order Code Payment)

March 16, 2022
==============

Online payments
---------------