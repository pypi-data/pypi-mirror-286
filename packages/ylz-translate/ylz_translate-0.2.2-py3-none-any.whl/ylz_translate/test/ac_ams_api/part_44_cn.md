*   添加了以下错误代码：

*   CLIENT\_FORBIDDEN\_ACCESS\_API
*   INVALID\_CLIENT\_STATUS
*   OAUTH\_FAILED
*   UNKNOWN\_CLIENT  

2022年1月5日
===============

在线支付
--------------

*   在以下接口中添加了\_grossSettlementAmount_和\_settlementQuote_字段：

*   notifyPayment
*   inquiryPayment
*   refund
*   inquiryRefund

*   更新了\_pay_（_收银台支付_）文档：
*   添加了以下错误代码：

*   INVALID\_MERCHANT\_STATUS
*   MERCHANT\_KYB\_NOT\_QUALIFIED
*   NO\_PAY\_OPTIONS

*   移除了以下错误代码：

*   SUCCESS
*   ORDER\_NOT\_EXIST  

店内支付
-------------

*   在**inquiryRefund**接口中添加了\_grossSettlementAmount_和\_settlementQuote_字段。

**更新了** **_pay (用户出示模式支付)_** **文档：**

*   移除了以下字段：

*   请求参数：