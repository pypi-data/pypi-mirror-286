通知注册状态 | 产品API | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fnrs)  
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

通知注册状态
========================

2024年4月24日 07:15  
支付宝使用**notifyRegistrationStatus** API 向商家发送注册结果。

结构
=========

一条消息由头和体组成。以下部分专注于体的结构。关于头的结构，请参阅：

*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着必须使用双引号（" "）包围字段值。示例：

*   如果字段的数据类型为Integer，其值为20，设置为"20"。
*   如果字段的数据类型为Boolean，其值为true，设置为"true"。
### 请求参数  
显示全部  
#### referenceMerchantId 字符串  
由收单方分配的二级商户ID。  
关于此字段的更多信息  
*   最大长度：64个字符  
#### registrationRequestId 字符串  
用于唯一标识注册请求的ID。  
关于此字段的更多信息  
*   最大长度：64个字符  
#### referenceStoreId 字符串  
由收单方分配的，用于识别与商户关联的商店的ID。  
关于此字段的更多信息  
*   最大长度：32个字符  
#### registrationResult RegistrationResult 对象  
钱包注册结果信息  
显示子参数  
#### pspRegistrationResultList Array<PSPRegistrationResult> 对象  
来自Alipay+ MPP（Alipay+ 移动支付提供商）的注册结果。  
显示子参数
### 响应参数  
显示全部  
#### result 结果对象 **必需**  
请求结果包含状态和错误代码等信息。  
显示子参数  
API 探索器
### 请求  
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
10  
11  
12  
13  
14  
15  
16  
{  
"registrationRequestId": "202009181105860200000600142\*\*\*\*",  
"referenceMerchantId": "218812000019\*\*\*\*",  
"referenceStoreId": "34\*\*\*\*",  
"pspRegistrationResultList": \[  
{  
"pspName": "AlipayCN",  
"registrationResult": {  
"registrationStatus": "APPROVED"  
}  
}  
\],  
"registrationResult": {  
"registrationStatus": "COMPLETED"  
}  
}  
请注意，以下内容是以希伯来文呈现的，但根据上下文，这似乎是一个JSON格式的请求体，用于描述一个注册请求的结果。以下是中文翻译：

### 请求  
请求体  
{
"registrationRequestId": "202009181105860200000600142****",  
"referenceMerchantId": "218812000019****",  
"referenceStoreId": "34****",  
"pspRegistrationResultList": [
{
"pspName": "支付宝CN",  
"registrationResult": {  
"registrationStatus": "已批准"  
}  
}
],
"registrationResult": {  
"registrationStatus": "已完成"  
}
}

在这个请求体中：
- `registrationRequestId` 是注册请求的ID。
- `referenceMerchantId` 是参考商户ID。
- `referenceStoreId` 是参考商店ID。
- `pspRegistrationResultList` 是一个列表，包含了支付服务提供商（PSP）的注册结果。在这个例子中，只有一个PSP，即“支付宝CN”，其注册状态为“已批准”。
- `registrationResult` 是整个注册流程的结果，状态为“已完成”。
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
注意：以上内容为示例，实际响应可能包含更多数据。在蚂蚁金服的业务中，"resultCode" 为 "SUCCESS" 表示操作成功，"resultStatus" 的 "S" 通常代表正常状态，"resultMessage" 则是描述操作结果的简短信息，这里是 "成功"。具体的数据结构和含义会根据不同的接口和服务有所不同。
### 结果/错误代码  
| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 注册成功，无需进一步操作。 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。  
![图片3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)  

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)  

#### 这个页面有帮助吗？