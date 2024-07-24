*   Removed the following fields:

*   result.resultStatus: S 
*   paymentTime
*   authExpiryTime
*   challegeActionForm
*   redirectActionForm.method: SCAN
*   orderCodeForm.paymentMethodType
*   settlementQuote
*   grossSettlementAmount

*   Modified the following fields from Optional to Required:

*   orderCodeForm.expireTime
*   orderCodeForm.codeDetails
*   result.resultMessage

*   Added the _userLoginId_ field in the **applyToken** interface.
*   Added the following fields in the **pay** (Cashier Payment) and **pay** (Auto Debit) interfaces:

*   schemeUrl
*   applinkUrl
*   normalUrl
*   appIdentifier

*   Added the new enumeration values of `BPI` and `RABBIT_LINE_PAY` in the following APIs:

*   pay (Cashier Payment): paymentMethod.paymentMethodType

*   Added the new enumeration value of `RABBIT_LINE_PAY` in the following APIs:

*   pay (Auto Debit): paymentMethod.paymentMethodType
*   consult: customerBelongsTo
*   applyToken: customerBelongsTo