|
| AUTHENTICATION\_REQUIRED | F | 3D Secure authentication is required. | Reinitiate the payment and redirect the user to perform 3D Secure authentication.

 |
| SELECTED\_CARD\_BRAND\_NOT\_AVAILABLE | F | The card brand that the user selected to pay is not available. | The card brand that the user selected to pay is not available.

 |
| PAYMENT\_PROHIBITED | F | The payment cannot be processed because the goods are prohibited from sale in the country. | You are not allowed to appeal against this transaction.

 |
| INVALID\_EXPIRATION\_DATE | F | The value of paymentMethod.paymentMethodMetaData.expiryYear or paymentMethod.paymentMethodMetaData.expiryDate is invalid. | 

Check whether the value of _paymentMethod.paymentMethodMetaData.expiryYear or paymentMethod.paymentMethodMetaData.expiryDate_ is correct:

*   If not correct, pass in the correct value.
*   If correct, contact Alipay Technical Support for detailed reasons.