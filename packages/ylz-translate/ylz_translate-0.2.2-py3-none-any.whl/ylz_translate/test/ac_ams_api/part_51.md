*   Added a new field and enumeration (appId and MINI\_APP) are added to the following APIs:

*   pay (Cashier Payment)
*   pay (Auto Debit)
*   consult

March 8, 2021
=============

Online payments
---------------

*   Removed the following fields in the _Settlement Summary_ file:

*   transactionAmountValue
*   transactionCurrency

In-store payments
-----------------

*   Removed the following fields in the _Settlement Summary_ file:

*   transactionAmountValue
*   transactionCurrency

*   Removed INVALID\_CODE of error codes in the following APIs:

*   pay (User-presented Mode Payment)
*   pay (Order Code Payment)
*   pay (Entry Code Payment)

*   Added the `INVALID_PAYMENT_CODE` error code in the **pay** (User-presented Mode Payment) interface.

February 26, 2021
=================

Online payments
---------------

*   Added the following new APIs in _online payments_:

*   registration
*   notifyRegistrationStatus
*   inquiryRegistrationStatus
*   inquiryRegistrationInfo