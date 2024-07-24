| 状态码 | 类型 | 描述 | 处理方式 |
| --- | --- | --- | --- |
| PAYMENT\_IN\_PROCESS | U | 支付正在处理中。 | 获取任何URL（appLinkUrl, normalUrl, schemeUrl）并打开收银台页面。如果没有返回URL，使用新的_paymentRequestId_值再次调用**pay** API。如果问题持续存在，联系支付宝技术支持。 |
| REQUEST\_TRAFFIC\_EXCEED\_LIMIT | U | 请求流量超过限制。 | 重新调用接口以解决问题。如果未解决，联系支付宝技术支持。 |
| UNKNOWN\_EXCEPTION | U | 由于未知原因，API调用失败。 | 重新调用接口以解决问题。如果未解决，联系支付宝技术支持。 |
| USER\_NOT\_EXIST | F | 用户在钱包端不存在。 | 联系支付宝技术支持获取详细原因。 |
| ORDER\_NOT\_EXIST | F | 订单不存在。 | 检查_paymentId_是否正确。 |