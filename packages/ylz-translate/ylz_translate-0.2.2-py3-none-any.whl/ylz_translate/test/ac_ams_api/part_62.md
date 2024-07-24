October 24, 2019
================

Online payments & In-store payments
-----------------------------------

*   Modified the following to the request of the **pay** interface:

*   Removed _payToAmount_
*   Removed _paymentQuote_
*   Updated the description of _paymentAmount_ and updated the field to mandatory
*   Updated the sub-fields of _paymentFactor_

*   Modified the following changes to the response of the **pay** interface:

*   Removed _payToAmount_
*   Updated the description of _paymentQuote_
*   Updated the description of _paymentAmount_ and updated the field to mandatory
*   Added _actualPaymentAmount_
*   Removed _nonGuaranteeCouponValue_

*   Updated the following changes to the request of the **notifyPayment** interface:

*   Removed _payToAmount_
*   Updated the description of _paymentQuote_
*   Updated the description of _paymentAmount_ and updated the field to mandatory
*   Added _actualPaymentAmount_
*   Removed _nonGuaranteeCouponValue_