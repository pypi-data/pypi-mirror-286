|
| PAYMENT\_IN\_PROCESS | U | The payment is being processed. | Get any of the URLs (appLinkUrl, normalUrl, schemeUrl) and open the cashier page. If no URL is returned, call the **pay** API again with a new _paymentRequestId_ value. If the issue persists, contact Alipay Technical Support.

 |
| REQUEST\_TRAFFIC\_EXCEED\_LIMIT | U | The request traffic exceeds the limit. | Call the interface again to resolve the issue. If not resolved, contact Alipay Technical Support.

 |
| UNKNOWN\_EXCEPTION | U | An API call has failed, which is caused by unknown reasons. | Call the interface again to resolve the issue. If not resolved, contact Alipay Technical Support.

 |
| USER\_NOT\_EXIST | F | The user does not exist on the wallet side. | Contact Alipay Technical Support for detailed reasons.

 |
| ORDER\_NOT\_EXIST | F | The order does not exist. | Check whether _paymentId_ is correct.