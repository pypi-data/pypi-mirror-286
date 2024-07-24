*   Modified the following to the response of the **pay** interface:

*   Removed _paymentActionForm_
*   challengeActionForm: added
*   redirectActionForm: added
*   orderCodeForm: added

*   Modified the following to the request of the **pay** interface:

*   order.referenceOrderId: updated to optional

*   Modified the following to the request of the **notifyPayment** interface:

*   paymentCodeForm: removed

*   Modified the following to the response of the **inquiryPayment** interface:

*   paymentActionForm: removed
*   redirectActionForm: added

November 6, 2019
================

Online payments & In-store payments
-----------------------------------

*   Modified the `INVALID_SIGNATURE` result code to `SIGNATURE_INVALID` for the following interfaces:

*   pay (Cashier Payment)
*   pay (User-presented Mode Payment)
*   pay (Order Code Payment)
*   notifyPayment
*   inquiryPayment
*   cancel
*   refund
*   consult
*   applyToken
*   revoke
*   Authorization Inquiry