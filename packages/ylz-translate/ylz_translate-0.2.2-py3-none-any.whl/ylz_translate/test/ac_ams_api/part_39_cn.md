*   `无效的支付方式元数据`
*   `错误的BLIK码`
*   `结算合同不匹配`

更新了`notifyPayment`文档：

*   在`notifyType`字段中添加了新的枚举值`PAYMENT_PENDING`。

更新了`inquiryPayment`文档：

*   在`paymentStatus`字段中添加了新的枚举值`PENDING`。

更新了退款文档：

*   在请求参数中添加了`refundNotifyUrl`字段。
*   添加了错误代码：`REFUND_IN_PROCESS`

2022年4月1日
============

在线支付
---------

*   在以下接口的请求参数中添加了`merchantRegion`字段：

    *   pay（收银台支付）
    *   consult
    *   applyToken

店内支付
---------

*   在以下接口的请求参数中添加了`merchantRegion`字段：

    *   pay（用户出示模式支付）
    *   pay（订单码支付）
    *   pay（订单码支付）

2022年3月16日
============

在线支付
---------