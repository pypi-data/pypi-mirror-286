*   Added the _creditPayPlan_ field to the following interfaces:

*   pay (Cashier Payment)
*   pay (Auto Debit Payment)

In-store payments
-----------------

*   Modified the following to the **notifyPayment** interface:

*   For a payment process with a failed or unknown status, no notification is to be returned to the merchant.

*   Modified the following to the **pay** (User-presented Mode Payment) interface:

*   Additional instructions for the _order_ field are provided.

*   Added the following error codes for the **pay** interface:

*   USER\_NOT\_EXIST
*   NO\_PAY\_OPTION
*   PAYMENT\_NOT\_EXIST
*   ORDER\_NOT\_EXIST
*   ORDER\_IS\_CLOSED

*   Added the following error code for the **notifyPayment** interface:

*   ORDER\_IS\_CLOSED

April 30, 2020
==============

Online payments
---------------

*   Added the _settlementStrategy_ field to the following interfaces:

*   pay (Cashier Payment)
*   pay (Auto Debit Payment)