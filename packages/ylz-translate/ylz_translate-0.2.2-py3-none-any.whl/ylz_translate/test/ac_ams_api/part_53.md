*   Updated the descriptions of the _transactionId_, _originalTransactionId_, and _originalTransactionRequestId_ fields for adding the auth/capture scenario for the _Settlement Items_ file.
*   Updated the descriptions of the _transactionId_, _originalTransactionId_, and _originalTransactionRequestId_ fields for adding the auth/capture scenario for the _Transaction_ _Items_ file.

June 9, 2020
============

Online payments
---------------

*   Removed the note about the _extend_ field for the **applyToken** interface.
*   Updated the file name for the case that no transaction exists is updated for the _Settlement Items_, _Settlement Summary_, and T_ransaction Items_ files.
*   Added the following error codes for the **pay** interface:

*   USER\_NOT\_EXIST
*   NO\_PAY\_OPTION
*   PAYMENT\_NOT\_EXIST
*   ORDER\_NOT\_EXIST
*   ORDER\_IS\_CLOSED

*   Added the following error code for the **notifyPayment** interface:

*   ORDER\_IS\_CLOSED