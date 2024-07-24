The unique ID that is assigned by Alipay to identify a payment.

More information about this field

*   Maximum length: 64 characters

#### declarationAmount Amount object REQUIRED

The accumulated transaction declaration amount, which cannot be greater than the total transaction amount. Only China customs declaration is supported. The default currency is `CNY` (Chinese Renminbi).

Note: This field can be obtained from the _customsDeclarationAmount_ field in the **notifyPayment** request and **inquiryPayment** response.

Show child parameters

#### customs CustomsInfo object REQUIRED

The customs information

Show child parameters

#### merchantCustomsInfo MerchantCustomsInfo object REQUIRED

The merchant information that is registered in the customs system.

Show child parameters

#### splitOrder Boolean  REQUIRED