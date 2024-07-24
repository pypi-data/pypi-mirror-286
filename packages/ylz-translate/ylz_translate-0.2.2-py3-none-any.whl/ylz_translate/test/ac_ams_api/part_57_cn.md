*   键未找到
*   访问被拒绝
*   API无效
*   客户端无效
*   方法不支持
*   媒体类型不可接受

2020年3月3日
============

在线支付
---------

*   从**pay**，**notifyPayment**，**inquiryPayment**和**refund**接口中移除了以下参数：

    *   总结算金额
    *   结算汇率

店内支付
---------

*   更新了**pay**，**notifyPayment**，**inquiryPayment**和**refund**接口的以下参数：

    *   将_totalSettlementAmount_修改为_grossSettlementAmount_

2020年2月25日
==============

在线支付与店内支付
-------------------

*   添加到**pay**，**inquiryPayment**和**refund**接口响应中的以下参数：

    *   总结算金额
    *   结算汇率

*   添加到**notifyPayment**接口请求中的以下参数：

    *   总结算金额
    *   结算汇率