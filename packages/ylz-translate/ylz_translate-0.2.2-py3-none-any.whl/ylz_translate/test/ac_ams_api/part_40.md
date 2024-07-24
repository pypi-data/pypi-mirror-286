*   Added the _redirectActionForm_ field in the response parameters of the **inquiryPayment** interface.

February 21, 2022
=================

Online payments
---------------

*   Added the `USER_NOT_EXIST` error code in the _pay (Auto Debit)_ document.

February 15, 2022
=================

Online payments
---------------

*   Removed the **initAuthentication** and **verifyAuthentication** interfaces.

January 19, 2022
================

Online payments
---------------

**Updated** **the** **_pay_** **_(_****_Auto Debit_****_)_** **document:**

*   Removed the following fields:

*   Request parameters:

*   merchant.store
*   order.env.storeTerminalId
*   order.env.storeTerminalRequestTime
*   payToMethod
*   paymentMethod.paymentMethodMetaData
*   isAuthorization
*   paymentVerificationData
*   paymentFactor

*   Response parameters:

*   authExpiryTime
*   challengeActionForm
*   redirectActionForm
*   orderCodeForm

*   Modified the following fields from Optional to Required: