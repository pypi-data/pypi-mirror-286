|
| INVALID\_CARD\_NUMBER | F | The number of the card used for the transaction is invalid. | 

Check whether the value of _paymentMethod.paymentMethodMetaData.cardno_ is correct:

*   If not correct, pass in the correct value and try again.
*   If correct, this card is not supported by the transaction, use another card to pay the transaction.



 |
| CARD\_NOT\_SUPPORTED | F | The card used for the transaction is not supported. | 

Use another card to pay the transaction.



 |
| DO\_NOT\_HONOR | F | The payment is declined by the issuing bank. | 

Retry the payment using a different card or contact the issuing bank.



 |
| INVALID\_AMOUNT | F | The transaction was declined by the issuing bank due to various reasons. For example, the specified amount is invalid or exceeds the maximum amount limit. | 

Contact Alipay Technical Support for detailed reasons.



 |

To view the latest updates to the documentation, visit [Release notes](https://global.alipay.com/docs/releasenotes).