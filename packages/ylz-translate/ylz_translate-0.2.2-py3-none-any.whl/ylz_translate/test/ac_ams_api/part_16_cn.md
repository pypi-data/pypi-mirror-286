*   请求头中的[签名](https://global.alipay.com/docs/ac/ams/api_fund)字段
*   如何[计算签名](https://global.alipay.com/docs/ac/ams/digital_signature) 

|
| 错误代码 | 错误类型 | 错误信息 | 解决方案 |
| --- | --- | --- | --- |
| KEY\_NOT\_FOUND | F | 未找到支付宝或商家的私钥或公钥。 | 检查私钥或公钥是否存在。如果不存在，请在Antom仪表盘上传私钥。 |

|
| MEDIA\_TYPE\_NOT\_ACCEPTABLE | F | 服务器不支持客户端可接受的媒体类型。 | 检查媒体类型是否正确，并使用支付宝接受的媒体类型。

 |
| MERCHANT\_NOT\_REGISTERED | F | 商家未注册。 | 请使用注册接口注册商家。如果调用注册接口失败，请联系支付宝技术支持。

 |
| METHOD\_NOT\_SUPPORTED | F | 服务器不支持请求的HTTP方法。仅支持POST方法。 | 确保HTTP方法为POST。 |