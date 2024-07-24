2021年10月26日
===============

在线支付
--------

*   在在线支付中添加了以下新API：

    *   notifyAuthorization
    *   inquiryRefund
    *   declare
    *   inquiryDeclarationRequests

店内支付
--------

*   在店内支付中添加了以下新API：

    *   inquiryRefund

2021年8月12日
===============

在线支付
--------

*   移除了**inquiryUserInfo**接口。
*   在**pay**（自动扣款）接口中添加了_paymentNotifyUrl_字段。

2021年8月9日
==============

在线支付
--------

*   在**refund**接口中添加了`MULTIPLE_REFUNDS_NOT_SUPPORTED`错误代码。

店内支付
--------

*   在**refund**接口中添加了`MULTIPLE_REFUNDS_NOT_SUPPORTED`错误代码。

2021年7月30日
=============

在线支付
--------

*   从以下API中移除了_orderCodeForm.codeDetails.codeValueType_字段：

    *   pay（收银员支付）
    *   pay（自动扣款）