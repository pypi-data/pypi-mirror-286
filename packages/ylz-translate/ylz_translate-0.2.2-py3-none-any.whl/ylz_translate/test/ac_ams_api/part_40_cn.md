2022年2月21日
============

在线支付
--------

*   在**查询支付**接口的响应参数中添加了 `_redirectActionForm_` 字段。

2022年2月15日
============

在线支付
--------

*   在**支付（自动扣款）**文档中添加了 `USER_NOT_EXIST` 错误代码。

2022年1月19日
============

在线支付
--------

**更新了** **_pay_** **_(_****_自动扣款_****_)_** **文档：**

*   移除了以下字段：

*   请求参数：

    *   merchant.store
    *   order.env.storeTerminalId
    *   order.env.storeTerminalRequestTime
    *   payToMethod
    *   paymentMethod.paymentMethodMetaData
    *   isAuthorization
    *   paymentVerificationData
    *   paymentFactor

*   响应参数：

    *   authExpiryTime
    *   challengeActionForm
    *   redirectActionForm
    *   orderCodeForm

*   将以下字段从可选修改为必填：