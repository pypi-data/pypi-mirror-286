*   在以下接口中添加了`creditPayPlan`字段：

    *   pay（收银台支付）
    *   pay（自动扣款支付）

店内支付
--------

*   对**notifyPayment**接口进行了以下修改：

    *   对于状态失败或未知的支付流程，不再向商家返回通知。

*   对**pay**（用户出示模式支付）接口进行了以下修改：

    *   对`order`字段提供了额外的说明。
    *   为**pay**接口添加了以下错误代码：

        *   USER\_NOT\_EXIST
        *   NO\_PAY\_OPTION
        *   PAYMENT\_NOT\_EXIST
        *   ORDER\_NOT\_EXIST
        *   ORDER\_IS\_CLOSED

*   为**notifyPayment**接口添加了以下错误代码：

    *   ORDER\_IS\_CLOSED

2020年4月30日
-------------

在线支付
--------

*   在以下接口中添加了`settlementStrategy`字段：

    *   pay（收银台支付）
    *   pay（自动扣款支付）