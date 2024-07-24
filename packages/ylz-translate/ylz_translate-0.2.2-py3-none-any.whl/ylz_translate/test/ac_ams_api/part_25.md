|
| ORDER\_IS\_CANCELED | F | The request you initiated has the same paymentRequestId as the previously paid transaction, which is canceled. | Use a new _paymentRequestId_ to initiate the payment again.

 |
| ORDER\_IS\_CLOSED | F | The paymentRequestId of your request is already used for a transaction, which is closed. | Use a new _paymentRequestId_ to initiate a payment.

 |
| PARAM\_ILLEGAL | F | The required parameters are not passed, or illegal parameters exist. For example, a non-numeric input, an invalid date, or the length and type of the parameter are wrong. | Check and verify whether the required request fields (including the header fields and body fields) of the current API are correctly passed and valid.