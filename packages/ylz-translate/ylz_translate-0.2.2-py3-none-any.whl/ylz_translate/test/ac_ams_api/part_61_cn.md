*   更新了**pay**接口的响应内容：

    *   删除了_paymentActionForm_
    *   添加了challengeActionForm
    *   添加了redirectActionForm
    *   添加了orderCodeForm

*   更新了**pay**接口的请求内容：

    *   order.referenceOrderId: 更新为可选参数

*   更新了**notifyPayment**接口的请求内容：

    *   移除了paymentCodeForm

*   更新了**inquiryPayment**接口的响应内容：

    *   移除了paymentActionForm
    *   添加了redirectActionForm

2019年11月6日
===============

在线支付与店内支付
-------------------

*   对以下接口的`INVALID_SIGNATURE`结果代码修改为`SIGNATURE_INVALID`：

    *   pay（收银台支付）
    *   pay（用户出示模式支付）
    *   pay（订单码支付）
    *   notifyPayment
    *   inquiryPayment
    *   cancel
    *   refund
    *   consult
    *   applyToken
    *   revoke
    *   授权查询