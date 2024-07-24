July 5, 2022
============

Online payments
---------------

*   Updated the error codes in the interfaces: **consult**, **applyToken**, **revoke**, **pay (Cashier Payment)**, **pay (Auto Debit)**, **notifyPayment**, **inquiryPayment**, **cancel**, **refund**, **inquiryRefund**, **notifyRefund**, **declare**, **inquiryDeclarationRequests**.

In-store payments
-----------------

*   Updated the error codes in the interfaces: **pay (User-presented Mode Payment)**, **pay (Order Code Payment)**, **pay (Entry Code Payment)**.

May 20, 2022
============

Online payments
---------------

Added the `consult (Cashier Payment)` and `notifyRefund` APIs.

Updated the `pay (Cashier Payment)` API:

*   Added the _paymentMethod.paymentMethodMetaData_ field in Request parameters.
*   Added some new enumeration values in the _paymentMethod.paymentMethodType_ field.
*   Modfied the field description of _settlementStrategy.settlementCurrency_.
*   Added the following error codes: