* 移除了以下字段：

  * result.resultStatus: S
  * paymentTime
  * authExpiryTime
  * challegeActionForm
  * redirectActionForm.method: SCAN
  * orderCodeForm.paymentMethodType
  * settlementQuote
  * grossSettlementAmount

* 将以下字段从可选修改为必需：

  * orderCodeForm.expireTime
  * orderCodeForm.codeDetails
  * result.resultMessage

* 在**applyToken**接口中添加了_userLoginId_字段。
* 在**pay**（收银台支付）和**pay**（自动扣款）接口中添加了以下字段：

  * schemeUrl
  * applinkUrl
  * normalUrl
  * appIdentifier

* 在以下API中添加了新的枚举值`BPI`和`RABBIT_LINE_PAY`：

  * pay（收银台支付）: paymentMethod.paymentMethodType

* 在以下API中添加了新的枚举值`RABBIT_LINE_PAY`：

  * pay（自动扣款）: paymentMethod.paymentMethodType
  * consult: customerBelongsTo
  * applyToken: customerBelongsTo

请注意，以上翻译保留了原始Markdown格式，并未翻译JSON键，且保留了空白行。