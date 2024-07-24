请求参数：

*   是否授权：isAuthorization
*   付款评估：paymentFactor.isPaymentEvaluation
*   支付方式元数据：paymentMethod.paymentMethodMetaData
*   支付验证数据：paymentVerificationData
*   支付到方法：payToMethod

响应参数：

*   授权过期时间：authExpiryTime
*   挑战动作表单：challengeActionForm.challengeRenderValue
*   订单代码表单：orderCodeForm

*   添加了 _settlementStrategy_ 字段。
*   将 _order.env_ 和 _order.env.userAgent_ 字段从可选改为必需。

2021年12月28日
===============

在线支付
--------

**更新了** **_pay (收银台支付)_** **文档：**

请求参数

*   删除以下字段：

*   商户店铺：merchant.store
*   订单环境中的商店终端ID：order.env.storeTerminalId
*   订单环境中的商店终端请求时间：order.env.storeTerminalRequestTime
*   支付到方法：payToMethod
*   支付方式ID：paymentMethod.paymentMethodId
*   支付方式元数据：paymentMethod.paymentMethodMetaData
*   是否授权：isAuthorization
*   支付验证数据：paymentVerificationData
*   付款因素：paymentFactor

*   将以下字段从可选改为必需：

*   订单环境：order.env
*   结算货币：settlementStrategy.settlementCurrency

响应参数