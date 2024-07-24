* 在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中添加了`merchantRegion`字段。
* 在[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online)API的响应参数中添加了`cardInfo`和`acquirerReferenceNo`字段。
* 在[退款](https://global.alipay.com/docs/ac/ams/refund_online)API的响应参数中添加了`acquirerReferenceNo`字段。
* 在[取消](https://global.alipay.com/docs/ac/ams/paymentc_online)API中添加了错误代码`ORDER_STATUS_INVALID`。
* 修改了[退款](https://global.alipay.com/docs/ac/ams/refund_online)和[取消](https://global.alipay.com/docs/ac/ams/paymentc_online)API中的错误代码`PAYMENT_METHOD_NOT_SUPPORTED`的名称。