*   请求参数：

    *   paymentMethod.paymentMethodId
    *   env
    *   env.terminalType
    *   settlementStrategy.settlementCurrency

*   响应参数：

    *   result.resultMessage

*   添加了以下错误代码：

    *   INVALID_MERCHANT_STATUS
    *   MERCHANT_KYB_NOT_QUALIFIED
    *   USER_PAYMENT_VERIFICATION_FAILED

*   删除了以下错误代码：

    *   USER_NOT_EXIST
    *   ORDER_NOT_EXIST

**更新了** **_notifyPayment_** **文档：**

*   删除了以下字段：

    *   请求参数：

        *   notifyType: OFFLINE_PAYMENT_CODE
        *   result.resultStatus: U

*   将以下字段从可选修改为必需：

    *   请求参数：

        *   paymentCreateTime
        *   paymentId
        *   result.resultMessage

*   添加了 _pay (Cashier Payment)_ 和 _pay (Auto Debit)_ 的错误代码。

**更新了** **_inquiryPayment_** **文档：**

*   删除了以下字段：

    *   响应参数：