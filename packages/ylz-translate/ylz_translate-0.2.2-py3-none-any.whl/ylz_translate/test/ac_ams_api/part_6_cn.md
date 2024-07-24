#### customsPaymentId 字符串

申报服务提供者向海关提供的支付ID。

注意：当 _result.resultCode_ 为 `S` 时，此字段返回。

关于此字段的更多信息：

*   最大长度：64个字符

#### customsOrderId 字符串

申报服务提供者向海关提供的订单ID。

注意：当 _result.resultCode_ 为 `S` 时，此字段返回。

关于此字段的更多信息：

*   最大长度：64个字符

#### identityCheckResult 字符串

身份检查结果。有效值为：

*   `CHECK_PASSED`：表示买方也是付款人。
*   `CHECK_NOT_PASSED`：表示买方不是付款人。

注意：当 _result.resultCode_ 为 `S` 时，此字段返回。如果未返回此字段，则表示未检查买方的身份。

#### clearingChannel 字符串

清算机构。有效值包括：