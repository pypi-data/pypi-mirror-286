|
| REPEAT\_REQ\_INCONSISTENT | F | The amount or currency is different from the previous request. | Ensure all the fields in the requests are the same or use a new _paymentRequestId_ to initiate the payment again.

 |
| RISK\_REJECT | F | The transaction cannot be further processed because of risk control. If the user has already paid for the transaction, the transaction will be refunded. | If the user does not receive the refund within two weeks, contact Alipay Technical Support.

 |
| SETTLE\_CONTRACT\_NOT\_MATCH | F | No matched settlement contract can be found. | Check the following for a solution:

1.  Specify one settlement currency from the multiple currencies that the merchant signed up for.
2.  Check if the settlement currency is specified in the settlement contracts.
3.  The merchant didn't sign a settlement contract. Contact Alipay Technical Support.

 |
| SYSTEM\_ERROR | F | A system error occurred. | Do not retry, and contact Alipay Technical Support for more details.