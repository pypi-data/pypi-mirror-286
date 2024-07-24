| 错误代码 | 类型 | 描述 | 解决方案 |
| --- | --- | --- | --- |
| INVALID\_CARD\_NUMBER | F | 用于交易的卡号无效。 | <br>检查\_paymentMethod.paymentMethodMetaData.cardno\_的值是否正确：<br> * 如果不正确，请输入正确值并重试。<br> * 如果正确，此卡不支持该交易，使用其他卡进行支付。 |
| CARD\_NOT\_SUPPORTED | F | 用于交易的卡不受支持。 | 使用其他卡进行支付。 |
| DO\_NOT\_HONOR | F | 发卡银行拒绝支付。 | 使用不同卡片重试支付或联系发卡银行。 |
| INVALID\_AMOUNT | F | 发卡银行因各种原因拒绝交易，例如指定金额无效或超过最大金额限制。 | 联系支付宝技术支持获取详细原因。 |

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。