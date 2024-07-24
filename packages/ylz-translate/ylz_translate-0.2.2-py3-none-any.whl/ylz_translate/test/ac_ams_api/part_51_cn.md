*   添加了新字段和枚举（appId 和 MINI\_APP）到以下API：

  *   pay（收银台支付）
  *   pay（自动扣款）
  *   咨询

2021年3月8日
============

在线支付
---------

*   在《结算汇总》文件中移除了以下字段：

  *   transactionAmountValue
  *   transactionCurrency

店内支付
---------

*   在《结算汇总》文件中移除了以下字段：

  *   transactionAmountValue
  *   transactionCurrency

*   在以下API中移除了错误代码INVALID\_CODE：

  *   pay（用户出示模式支付）
  *   pay（订单码支付）
  *   pay（入口码支付）

*   在**pay**（用户出示模式支付）接口中添加了`INVALID_PAYMENT_CODE`错误代码。

2021年2月26日
================

在线支付
---------

*   在**在线支付**中添加了以下新API：

  *   registration
  *   notifyRegistrationStatus
  *   inquiryRegistrationStatus
  *   inquiryRegistrationInfo