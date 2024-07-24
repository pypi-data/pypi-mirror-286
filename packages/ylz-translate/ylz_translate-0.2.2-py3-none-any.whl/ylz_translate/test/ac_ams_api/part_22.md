| Code | Value | Message | Further action |
| --- | --- | --- | --- |
| SUCCESS | S | Success | The payment is successful, no further action is needed.
 |
| ACCESS\_DENIED | F | Access is denied. | Contact Alipay Technical Support for detailed reasons.

 |
| CURRENCY\_NOT\_SUPPORT | F | The currency is not supported. | Contact Alipay Technical Support for detailed reasons.

 |
| EXPIRED\_CODE | F | The payment code is expired. | The user needs to refresh the payment code.

 |
| FRAUD\_REJECT | F | The transaction cannot be further processed because of risk control. If the user has already paid for the transaction, the transaction will be refunded. | Contact Alipay Technical Support when one of the following conditions is met:

*   You want to make an appeal. 
*   The user does not receive the refund within two weeks.  

 |
| INVALID\_ACCESS\_TOKEN | F | The access token is expired, revoked, or does not exist. | Check whether _accessToken_ is correct. If not correct, pass in the correct value. If correct, contact Alipay Technical Support for detailed reasons.