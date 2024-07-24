| 错误代码 | 类型 | 描述 | 解决方案 |
| --- | --- | --- | --- |
| ORDER\_IS\_CANCELED | F | 您发起的请求具有与之前已支付但被取消的交易相同的paymentRequestId。 | 使用新的_paymentRequestId_重新发起支付。 |
| ORDER\_IS\_CLOSED | F | 您请求的paymentRequestId已被用于一个已关闭的交易。 | 使用新的_paymentRequestId_发起支付。 |
| PARAM\_ILLEGAL | F | 必需参数未传递，或存在非法参数。例如，非数字输入，无效日期，或参数的长度和类型错误。 | 检查并验证当前API所需的请求字段（包括头部字段和正文字段）是否正确传递并有效。 |