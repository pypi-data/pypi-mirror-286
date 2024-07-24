*   Request parameters:

*   isAuthorization
*   paymentFactor.isPaymentEvaluation
*   paymentMethod.paymentMethodMetaData
*   paymentVerificationData
*   payToMethod

*   Response parameters:

*   authExpiryTime
*   challengeActionForm.challengeRenderValue
*   orderCodeForm

*   Added the _settlementStrategy_ field.
*   Modified the _order.env_ and the _order.env.userAgent_ fields from Optional to Required.

December 28, 2021
=================

Online payments
---------------

**Updated the** **_pay (Cashier Payment)_** **document:**

Request parameters

*   Removed the following fields:

*   merchant.store
*   order.env.storeTerminalId
*   order.env.storeTerminalRequestTime
*   payToMethod
*   paymentMethod.paymentMethodId
*   paymentMethod.paymentMethodMetaData
*   isAuthorization
*   paymentVerificationData
*   paymentFactor

*   Modified the following fields from Optional to Required:

*   order.env
*   settlementStrategy.settlementCurrency

Response parameters