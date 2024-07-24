|
| CLIENT\_INVALID | F | The client ID is invalid. Alipay has restrictions on the client ID. | Check whether the client ID is correct, or contact Alipay Technical Support for detailed reasons.

 |
| DUPLICATED\_DECLARATIONS | F | The same order can only be declared once at the same customs. | Check whether _paymentId_ has been used to declare. Use a different payment ID to initiate the declaration request.

 |
| INVALID\_CONTRACT | F | The parameter values in the contract do not match those in the current transaction. | Check whether the parameter values in the contract match those in the current transaction. If the values match, contact Alipay Technical Support to troubleshoot the issue.

 |
| INVALID\_SIGNATURE | F | The signature is not validated. The private key used to sign a request does not match the public key of Antom Dashboard. | 

Check whether the private key used to sign a request matches the public key of Antom Dashboard. The following signature references are useful: