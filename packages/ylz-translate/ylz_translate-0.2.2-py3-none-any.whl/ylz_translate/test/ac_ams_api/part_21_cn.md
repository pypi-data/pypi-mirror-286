*   `S`: 当返回此值时，API调用成功。
*   `F`: 当返回此值时，API调用失败。根据相应的结果消息采取行动，或使用新的`paymentRequestId`值再次调用API。如果问题持续存在，请联系支付宝技术支持。
*   `U`: 当返回此值时，检查结果代码：

    *   结果代码不是`PAYMENT_IN_PROCESS`：API调用失败。使用新的`paymentRequestId`值再次调用此API。
    *   结果代码是`PAYMENT_IN_PROCESS`：检查是否返回了一个或多个URL（appLinkUrl，normalUrl，schemeUrl）：

        *   返回了一个或多个URL：交易创建成功。将用户重定向到URL指定的地址以完成支付。
        *   没有返回URL：交易创建失败。使用新的`paymentRequestId`值再次调用**pay** API。如果问题持续存在，请联系支付宝技术支持。

### 结果/错误代码