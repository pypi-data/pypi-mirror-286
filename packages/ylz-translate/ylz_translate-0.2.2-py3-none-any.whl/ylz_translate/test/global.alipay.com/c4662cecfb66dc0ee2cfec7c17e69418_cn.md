通知授权 | 产品API | 支付宝文档
===============

[![支付宝，中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![支付宝，中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fnotifyauth)

[返回首页](../../)

产品API
[支付宝API](/docs/ac/ams/api)
在线支付
授权
[咨询](/docs/ac/ams/authconsult)
[通知授权](/docs/ac/ams/notifyauth)
[申请令牌](/docs/ac/ams/accesstokenapp)
[撤销](/docs/ac/ams/authrevocation)
保险箱
支付
订阅
争议
退款
申报
店内支付
通知授权
===================

2024-04-24 07:15

> 支付宝使用**notifyAuthorization**在授权成功或授权取消成功时将授权结果发送给商家。

结构
=========

一条消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：
*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着必须使用双引号（" "）包围字段值。例如：
*   如果字段的数据类型为Integer，其值为20，应设置为"20"。
*   如果字段的数据类型为Boolean，其值为true，应设置为"true"。
### 请求参数  
显示全部  
#### authorizationNotifyType 字符串  必填  
授权通知类型。有效值包括：  
*   `AUTHCODE_CREATED`（仅限自动扣款）：表示用户同意授权自动扣款支付。用户同意授权后，可以从这个通知中获取由钱包生成的授权码，并在**applyToken** API 中使用以获取访问令牌。
*   `TOKEN_CREATED`：表示用户在商户客户端成功发起授权。
*   `TOKEN_CANCELED`：表示用户已在支付方式端成功取消授权。  
关于此字段的更多信息  
*   最大长度：32 个字符  
#### authClientId 字符串  
用户授予资源访问权限的二级商户的唯一ID。值由收单方指定，需要在支付宝中注册。  
注意事项：  
*   当**consult** API 由 Alipay+ MPP 启动时，此字段将返回。
*   对于 Alipay+ MPP，此字段的值与 [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API 中的 _referenceMerchantId_ 的值相同。  
关于此字段的更多信息  
*   最大长度：64 个字符  
#### accessToken 字符串  
用于访问用户资源相应范围的访问令牌。  
注意：当 _authorizationNotifyType_ 的值为 `TOKEN_CANCELED` 或 `TOKEN_CREATED` 时，此字段将返回。  
关于此字段的更多信息  
*   最大长度：128 个字符  
#### authState 字符串  
由收单方生成的字符串，表示咨询请求。此字段的值用于验证是否与**consult**请求中指定的_authState_ 值一致。  
注意：当 _authorizationNotifyType_ 为 `AUTHCODE_CREATED` 和 `TOKEN_CREATED` 时，此字段将返回。  
关于此字段的更多信息
*   最大长度: 256 个字符  
#### authCode 字符串  
授权码，用于获取访问令牌。该值由应用从钱包重定向回的重构重定向URL中获取。  
注意：当 _authorizationNotifyType_ 为 `AUTHCODE_CREATED` 时，此字段返回。  
关于此字段的更多信息  
*   最大长度: 64 个字符  
#### reason 字符串  
授权取消的原因。当用户提供授权取消原因时，此字段会发送给商家。  
注意：当 _authorizationNotifyType_ 为 `TOKEN_CANCELED` 时，此字段返回。  
关于此字段的更多信息  
*   最大长度: 256 个字符  
#### result Result 对象 **必需**  
授权结果。支付宝仅在授权成功或取消授权成功时返回授权通知。因此，仅提供成功的授权结果。  
显示子参数  
#### userLoginId 字符串  
用户在钱包中注册时使用的登录ID。登录ID可以是用户的电子邮件地址或电话号码。  
指定此参数以避免用户手动输入登录ID。  
关于此字段的更多信息  
*   最大长度: 64 个字符  
#### userId 字符串  
支付方式提供者分配给用户以识别其身份的ID。  
关于此字段的更多信息  
*   最大长度: 64 个字符
### 响应参数  
显示全部  
#### result 结果对象 **必需**  
一个固定值，需要发送给支付宝以确认已接收到通知。  
显示子参数  
API 探索器
### 请求  
情况  
已取消的授权结果  
请求体  
复制  
1  
2  
3  
4  
5  
6  
7  
8  
9  
{  
"authorizationNotifyType": "TOKEN\_CANCELED",  
"accessToken": "28100103\_20215703001538122119",  
"result": {  
"resultCode": "SUCCESS",  
"resultMessage": "成功",  
"resultStatus": "S"  
}  
}  
请注意，以上内容为已取消授权的通知。类型为"TOKEN\_CANCELED"，访问令牌（accessToken）为"28100103\_20215703001538122119"。结果部分显示操作成功，结果代码（resultCode）为"SUCCESS"，状态（resultStatus）为"S"，表示该授权已被成功取消。
### 响应  
响应体  
复制  
1  
2  
3  
4  
5  
6  
7  
{  
"result": {  
"resultCode": "SUCCESS",  
"resultStatus": "S",  
"resultMessage": "成功"  
}  
}  
请注意，以下内容为示例逻辑，需要发送一个包含固定值的消息给支付宝，以确认接收到支付宝的通知：  
示例代码  
复制  
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  

结果处理逻辑  
在收到通知后，向支付宝发送以下固定值的消息，以确认已接收到支付宝的通知：  
示例代码  
复制  
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
如果由于操作问题或网络问题，支付宝没有收到商家返回的确认消息，支付宝会间歇性地重新发送通知，直到商家返回所需的消息。首次通知发送后的24小时内会进行重试，最多重试8次，重试间隔依次为0秒、2分钟、10分钟、10分钟、1小时、2小时、6小时和15小时。

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

![图片3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面有帮助吗？