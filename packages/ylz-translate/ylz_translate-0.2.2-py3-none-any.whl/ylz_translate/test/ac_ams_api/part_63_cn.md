* 对**查询支付**接口的响应进行了以下修改：

  * 更新了`paymentAmount`的描述，并将其设为必填字段
  * 移除了`payToAmount`
  * 添加了`actualPaymentAmount`
  * 更新了`paymentQuote`
  * 移除了`nonGuaranteeCouponValue`

* 对**取消**接口的请求进行了以下修改：

  * 添加了`paymentRequestId`

* 对**退款**接口的请求进行了以下修改：

  * 移除了`refundStrategyType`
  * 移除了`asyncRefund`
  * 添加了`isAsyncRefund`
  * 更新了`extendInfo`的长度为512个字符

要查看文档的最新更新，请访问[版本说明](https://global.alipay.com/docs/releasenotes)。

![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)