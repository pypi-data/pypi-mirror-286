查询注册状态 | 产品API | 支付宝文档
===============  
[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)  
[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Firs)  
[返回首页](../../)  
产品API  
[支付宝API](/docs/ac/ams/api)  
在线支付  
店内支付  
支付  
退款  
注册  
[注册](/docs/ac/ams/registration)  
[通知注册状态](/docs/ac/ams/nrs)  
[查询注册状态](/docs/ac/ams/irs)  
[查询注册信息](/docs/ac/ams/iri)  
查询注册状态
=========================  
2022-12-01 08:40  
POST /v1/merchants/inquiryRegistrationStatus  
使用**查询注册状态** API，通过发送二级商户信息或商户注册请求ID来查询二级商户的注册状态。  
结构
=========  
消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：
*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)  
**注意**：除数组外，每个字段的数据类型都应设置为字符串。这意味着字段值必须用双引号（" "）括起来。例如：
*   如果字段的数据类型为Integer，值为20，则设置为"20"。
*   如果字段的数据类型为Boolean，值为true，则设置为"true"。
### 请求参数  
#### referenceMerchantId 字符串  
由收单方分配的二级商户ID。  
关于此字段的更多信息：  
*   最大长度：64个字符  
#### registrationRequestId 字符串  
用于唯一标识注册请求的ID。  
关于此字段的更多信息：  
*   最大长度：64个字符  
#### referenceStoreId 字符串  
收单方分配的，用于识别与商户关联的商店的ID。  
关于此字段的更多信息：  
*   最大长度：32个字符
### 响应参数  
显示全部  
#### result 结果对象 **必需**  
请求结果，包含状态和错误代码等信息。  
显示子参数  
#### registrationResult 注册结果对象  
钱包的注册结果信息。  
显示子参数  
#### pspRegistrationResultList PSP注册结果列表对象  
来自Alipay+ MPP（Alipay+ 移动支付提供商）的注册结果。  
显示子参数  
API 探索器
### 请求  
URL  
北美地区  
https://open-na-global.alipay.com/ams/api/v1/merchants/inquiryRegistrationStatus  

请求体  
复制  
1  
2  
3  
4  
{  
"referenceMerchantId": "218812000019\*\*\*\*",  
"referenceStoreId": "34\*\*\*\*"  
}  

请注意，此文本为示例，实际内容已被省略。请将星号(\*\*\*\*)替换为实际的商户ID和商店ID。该请求用于查询商户的注册状态。
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
8  
9  
10  
{  
"result": {  
"resultStatus": "S",  
"resultCode": "SUCCESS",  
"resultMessage": "成功"  
},  
"registrationResult": {  
"registrationStatus": "PENDING"  
}  
}  
注意：此部分为原文，未翻译。  
```
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
更多信息
----------------  
以下为主要参数的重要细节：  
*   虽然 _registrationRequestId_、_referenceMerchantId_ 和 _referenceStoreId_ 均为可选，但我们建议包含 _referenceMerchantId_ 或 _referenceStoreId_。
*   如果初始注册时信息报告有误，允许对同一二级商户进行重新注册。当请求包含 _requestId_ 时，将返回注册结果。如果没有 _requestId_ 但请求中包含 _referenceMerchantId_，则返回当前二级商户所有钱包的状态。

不同情况的响应
-----------------------------
本节提供了查询注册状态不同情况的回复。

**PARAM\_ILLEGAL**
复制
参数非法或不完整。请检查输入信息并确保所有必需的参数都已正确提供。

**RECORD\_NOT\_FOUND**
复制
未找到记录。该用户或请求的信息在系统中不存在，请核实查询的细节。

**PENDING in the wallet side**
复制
钱包端处理中。注册请求已收到，但还在等待钱包系统的确认和处理。请稍候再试，或检查钱包的状态更新。

**REJECTED**
复制
注册请求被拒绝。可能由于不符合注册条件、信息不正确或系统限制等原因。请检查提供的信息并根据需要重新提交申请。
返回的电子钱包状态为`APPROVED`，注册状态为`COMPLETED`。
示例代码
复制
返回的电子钱包状态为`null`，注册状态为`COMPLETED`。
示例代码
复制

请注意，上述文档片段是关于某个系统或服务的用户钱包状态和注册状态的描述。在实际的蚂蚁金服业务中，这可能指的是用户在蚂蚁金服平台上的账户状态，例如，钱包已经通过审核（APPROVED）且注册流程已完成（COMPLETED）。第二个例子中，可能表示钱包状态未获取到具体信息（可能是暂无状态或未初始化），但注册流程已经完成。这些代码示例可能是API调用的返回结果。
### 结果/错误代码  
| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 注册成功，无需进一步操作。 |
| INVALID\_CLIENT | F | 客户端无效。 | 检查\_clientId\ 是否正确。 |
| MEDIA\_TYPE\_NOT\_ACCEPTABLE | F | 服务器不支持客户端可接受的媒体类型。 | 检查媒体类型是否正确。 |
| METHOD\_NOT\_SUPPORTED | F | 服务器不支持请求的HTTP方法。 | 检查HTTP方法是否正确。 |
| REPEAT\_REQ\_INCONSISTENT | F | 重复请求不一致。 | 更改\_registrationRequestId\ 并再次调用接口。 |
| RECORD\_NOT\_FOUND | F | 系统无法找到给定referenceMerchantId和/或referenceStoreId的注册记录。 | 未找到注册记录。请检查\_referenceMerchantId\ 或\_referenceStoreId\ 是否正确。 |

要查看文档的最新更新，请访问 [版本说明](https://global.alipay.com/docs/releasenotes)。
![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)  
@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)  
#### 这个页面有帮助吗？