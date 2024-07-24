通知注册状态 | 产品API | 支付宝文档
======================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_a52690f40beef33d7d37f1bda6f48c27.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_d70d46fd32b98952674df01c03131d87.svg)](/docs/)

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
------------

2024-04-24 07:15

支付宝使用**notifyRegistrationStatus** API 向商家发送商家注册的结果。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：

*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着字段值必须用双引号（" "）包围。例如：

*   如果字段的数据类型是整数，值为20，则设置为"20"。
*   如果字段的数据类型是布尔值，值为true，则设置为"true"。

### 请求参数

显示全部

#### referenceMerchantId 字符串

由收单方分配的二级商户ID。

此字段的更多信息：

*   最大长度：64个字符

#### registrationRequestId 字符串

唯一用于识别注册请求的ID。

关于此字段的更多信息：

*   最大长度：64 个字符

#### referenceStoreId 字符串 

由收单方分配的用于识别与商户关联的商店的ID。

关于此字段的更多信息：

*   最大长度：32 个字符

#### registrationResult RegistrationResult 对象 

钱包注册结果信息

显示子参数

#### pspRegistrationResultList PSPRegistrationResult 对象数组 

来自Alipay+ MPP（Alipay+ 移动支付提供商）的注册结果。

显示子参数

### 响应参数

显示全部

#### result Result 对象 **必需**

请求结果，包含状态和错误代码等信息。

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

"referenceMerchantId": "218812000019****", 

"referenceStoreId": "34****", 

"pspRegistrationResultList": [ 

{ 

"pspName": "支付宝CN", 

"registrationResult": { 

"registrationStatus": "批准" 

} 

}, 

], 

"registrationResult": { 

"registrationStatus": "完成" 

} 

}

请注意，这里的翻译已遵循您的要求，保留了原始Markdown格式，没有翻译JSON键，并确保语句通顺。

### 响应

响应体

Copy

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

很抱歉，我看到您输入的内容似乎是以希伯来文字符重复组成的，这可能是一个输入错误。如果您能提供需要翻译的英文或中文Markdown文档，我将非常乐意帮助您进行翻译。请确保文档内容是与蚂蚁金服的业务或金融技术相关，以便我提供专业且准确的翻译。

### 结果/错误代码

| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 注册成功，无需进一步操作。 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。

![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面是否有帮助？