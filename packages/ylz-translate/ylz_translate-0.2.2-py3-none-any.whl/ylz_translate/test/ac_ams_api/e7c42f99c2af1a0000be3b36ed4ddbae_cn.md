查询注册状态 | 产品API | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_a52690f40beef33d7d37f1bda6f48c27.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_d70d46fd32b98952674df01c03131d87.svg)](/docs/)

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

[查询注册状态通知](/docs/ac/ams/nrs)

[查询注册状态](/docs/ac/ams/irs)

[查询注册信息](/docs/ac/ams/iri)

查询注册状态
------------

2022-12-01 08:40

POST /v1/merchants/inquiryRegistrationStatus

使用**inquiryRegistrationStatus** API查询二级商户的注册状态，通过发送二级商户的信息或商户注册请求ID。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：

*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为String。这意味着必须使用双引号（" "）包围字段值。例如：

*   如果字段的数据类型为Integer，其值为20，则设置为"20"。 
*   如果字段的数据类型为Boolean，其值为true，则设置为"true"。 

### 请求参数

#### referenceMerchantId 字符串

由收单方分配的二级商户ID。

关于此字段的更多信息

*   最大长度：64 个字符

#### registrationRequestId 字符串

用于唯一标识注册请求的ID。

关于此字段的更多信息

*   最大长度：64 个字符

#### referenceStoreId 字符串

由收单方分配的用于识别与商家关联的店铺的ID。

关于此字段的更多信息

*   最大长度：32 个字符

### 响应参数

显示全部

#### result Result 对象 **必需**

请求结果包含状态和错误代码等信息。

显示子参数

#### registrationResult RegistrationResult 对象

钱包返回的注册结果信息。

显示子参数

#### pspRegistrationResultList Array<PSPRegistrationResult> 对象

来自 Alipay+ MPP（Alipay+ 移动支付提供商）的注册结果。

显示子参数

API 探索器

### 请求

URL

北美

开放北美全球蚂蚁金服API - 商户查询注册状态

请求体

Copy

```json
{
  "referenceMerchantId": "218812000019****",
  "referenceStoreId": "34****"
}
```

请注意，此API用于查询商户的注册状态。请求体中包含以下参数：

- `referenceMerchantId`：参考商户ID，此处显示为星号（****）以保护隐私。
- `referenceStoreId`：参考门店ID，同样显示为星号（****）。

请确保在实际使用时替换这些ID为有效的商户和门店标识。

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

8

9

10

```json
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
```

请注意，JSON键未被翻译，以遵循您的指示。翻译后的文档保留了原始markdown格式，并确保语句通顺。

很抱歉，我看到您输入的内容似乎是以希伯来文字符重复组成的，这可能是一个输入错误。如果您能提供需要翻译的英文或中文Markdown文档，我将非常乐意帮助您进行翻译。请确保文档内容是与蚂蚁金服的业务或金融技术相关，以便我提供专业且准确的翻译。

更多信息
------------

请查看以下列表，了解主要参数的重要细节：

*   虽然 _registrationRequestId_、_referenceMerchantId_ 和 _referenceStoreId_ 均为可选，但我们建议提供 _referenceMerchantId_ 或 _referenceStoreId_。
*   如果初次注册时提供了错误信息，允许为相同的二级商户进行重新注册。当请求包含 _requestId_ 时，将返回注册结果。如果请求中没有 _requestId_ 但包含 _referenceMerchantId_，则返回当前二级商户所有钱包的状态。

不同情况的响应
-----------------

本节提供了查询注册状态时不同情况的响应。

PARAM\_ILLEGAL

复制

找不到记录

此消息表示在查询或检索数据时，没有找到匹配的记录。在数据库或系统中，可能由于指定的ID、键值或其他标识符不存在，导致返回此错误代码。请检查输入的参数是否正确，或者确认所查找的资源是否已存在或已被删除。

钱包端待处理

复制

很抱歉，您似乎没有提供任何文档内容需要翻译。请提供具体的markdown格式文档，我将很乐意帮您翻译。

返回的钱包状态为`APPROVED`，注册状态为`COMPLETED`。

示例代码

复制

返回的钱包状态为null，注册状态为COMPLETED。

示例代码

复制

### 结果/错误代码

| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 注册成功，无需进一步操作。 |
| INVALID\_CLIENT | F | 客户端无效。 | 检查\_clientId\_是否正确。 |
| MEDIA\_TYPE\_NOT\_ACCEPTABLE | F | 服务器不支持客户端可接受的媒体类型。 | 检查媒体类型是否正确。 |
| METHOD\_NOT\_SUPPORTED | F | 服务器不支持请求的HTTP方法。 | 检查HTTP方法是否正确。 |

|
| 重复请求不一致 | F | 重复请求的数据不一致。 | 更改 _registrationRequestId_ 并重新调用接口。

 |
| 记录未找到 | F | 系统无法找到给定的 _referenceMerchantId_ 和/或 _referenceStoreId_ 对应的注册记录。 | 未找到注册记录。请检查 _referenceMerchantId_ 或 _referenceStoreId_ 是否正确。

 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。

![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面是否有帮助？