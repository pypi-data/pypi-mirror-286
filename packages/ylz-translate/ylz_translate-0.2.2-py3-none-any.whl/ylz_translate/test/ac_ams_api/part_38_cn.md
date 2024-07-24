2022年7月5日
============

在线支付
---------

*   更新了以下接口的错误代码：**咨询**、**申请令牌**、**撤销**、**支付（收银台支付）**、**支付（自动扣款）**、**支付通知**、**查询支付**、**取消**、**退款**、**查询退款**、**退款通知**、**申报**、**查询申报请求**。

店内支付
---------

*   更新了以下接口的错误代码：**支付（用户出示模式支付）**、**支付（订单码支付）**、**支付（入场码支付）**。

2022年5月20日
============

在线支付
---------

添加了`consult (Cashier Payment)`和`notifyRefund` API。

更新了`pay (Cashier Payment)` API：

*   在请求参数中添加了`paymentMethod.paymentMethodMetaData`字段。
*   在`paymentMethod.paymentMethodType`字段中添加了一些新的枚举值。
*   修改了`settlementStrategy.settlementCurrency`字段的描述。
*   添加了以下错误代码：