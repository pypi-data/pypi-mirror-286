October 26, 2021
================

Online payments
---------------

*   Added the following new APIs in online payments:

*   notifyAuthorization
*   inquiryRefund
*   declare
*   inquiryDeclarationRequests

In-store payments
-----------------

*   Added the following new API in in-store payments:

*   inquiryRefund

August 12, 2021
===============

Online payments
---------------

*   Removed the **inquiryUserInfo** interface.
*   Added the _paymentNotifyUrl_ field in the **pay** (Auto Debit) interface.

August 9, 2021
==============

Online payments
---------------

*   Added the `MULTIPLE_REFUNDS_NOT_SUPPORTED` error code in the **refund** interface.

In-store payments
-----------------

*   Added the `MULTIPLE_REFUNDS_NOT_SUPPORTED` error code in the **refund** interface.

July 30, 2021
=============

Online payments
---------------

*   Removed the _orderCodeForm.codeDetails.codeValueType_ field in the following API:

*   pay (Cashier Payment)
*   pay (Auto Debit)