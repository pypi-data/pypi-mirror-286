*   添加了 _originalTransactionRequestId_ 到以下文件：

    *   结算项目
    *   交易项目

店内支付
--------

*   添加了 _originalTransactionRequestId_ 到以下文件：

    *   结算项目
    *   交易项目

2020年4月17日
==============

在线支付 & 店内支付
--------------------

*   从以下接口中移除了 _actualPaymentAmount_ 和 _paymentQuote_ 字段：

    *   pay（收银台支付）
    *   pay（协议支付）
    *   pay（用户出示模式支付）
    *   pay（订单码支付）
    *   pay（入口码支付）
    *   notifyPayment
    *   inquiryPayment

店内支付
--------

*   修改了以下接口的 _paymentExpiryTime_ 字段描述：

    *   pay（订单码支付）
    *   pay（入口码支付）

2020年3月20日
==============

在线支付
--------

*   移除了 **授权查询** 接口。

2020年3月12日
==============