咨询
====

2024-04-24 07:05

POST /v1/authorizations/consult

使用此API获取用户授权。成功调用此API后，您将获取授权URL，并可将用户重定向到该URL以同意授权。用户同意授权后，钱包会将用户重定向回一个由`authRedirectUrl`、`authCode`和`authState`值构造的重定向URL，例如：https://www.merchant.com/authorizationResult?authCode=3AB2F588D14B43238637264FCA5AAF35&authState=663A8FA9-D836-48EE-8AA1-1FF682989DC7。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：

*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**: 将每个字段（不包括数组）的数据类型设置为字符串。这意味着字段值必须用双引号（" "）括起来。示例：

*   如果字段的数据类型是整数，其值为20，应设置为"20"。
*   如果字段的数据类型是布尔值，其值为true，应设置为"true"。

### 请求参数

#### customerBelongsTo 字符串  必填

用户使用的钱包。查看[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)以检查有效值。

关于此字段的更多信息：

*   最大长度：64 个字符

#### authClientId 字符串 

用户授予资源访问权限的二级商户的唯一ID。该值由发起方指定，需要在支付宝中注册。

注释：

*   如果您是拥有二级商户的收单机构，请指定此字段。
*   对于Alipay+ MPP（多渠道支付），此字段的值与**pay**（自动扣款）接口中的referenceMerchantId字段相同。

关于此字段的更多信息

*   最大长度：64个字符

#### authRedirectUrl **URL** **必需**

用户同意授权后被重定向的URL。此值由商户提供。

关于此字段的更多信息

*   最大长度：1024个字符

#### scopes **Array<String>** **必需**

授权范围。有效值包括：

*   `BASE_USER_INFO`: 表示可以获取唯一用户ID。
*   `USER_INFO`: 表示可以获取完整的用户信息，例如用户名、头像等其他用户信息。
*   `AGREEMENT_PAY`: 表示用户同意授权自动扣款，商家可以使用访问令牌自动从用户账户中扣款。

关于此字段的更多信息

*   最大元素数量：4

#### authState 字符串  必需

商家生成的唯一ID，代表咨询请求。当用户同意授权时，此字段与重定向URL中的字段需要保持一致。

关于此字段的更多信息

*   最大长度：256个字符

#### terminalType 字符串  必需

商家服务所适用的终端类型。有效值包括：

*   `WEB`: 客户端终端类型为通过网络浏览器打开的网站。
*   `WAP`: 客户端终端类型为通过移动浏览器打开的HTML页面。
*   `APP`: 客户端终端类型为移动应用程序。
*   `MINI_APP`: 商户端的终端类型为手机上的小程序。

#### osType 字符串

操作系统类型。有效值包括：

*   `IOS`: 表示操作系统为苹果的iOS。
*   `ANDROID`: 表示操作系统为谷歌的Android。

注意：当`terminalType`为`APP`、`WAP`或`MINI_APP`时，此字段是必需的。

#### osVersion 字符串

操作系统版本。

当`terminalType`的值为`APP`或`WAP`且您有此信息时，指定此参数。提供此信息可以改善用户的支付体验。

关于此字段的更多信息：

*   最大长度：16个字符

#### merchantRegion 字符串

商家或二级商家经营业务所在的国家或地区。该参数遵循[ISO 3166国家代码](https://www.iso.org/obp/ui/#search)标准，是一个2字母的国家/地区代码。目前仅支持`US`、`JP`、`PK`和`SG`。

注意：当使用全球收单网关（GAGW）产品时，此字段是必需的。

关于此字段的更多信息：

*   最大长度：2个字符

### 响应参数

显示全部

#### result 结果对象 **必需**

指示此API是否调用成功。如果API调用成功，可以获取授权URL。

显示子参数

#### schemeUrl URL

当目标应用已安装时，用于在Android或iOS系统中重定向用户打开应用的URL方案。

注意：当_result.resultCode_的值为`S`时，至少需要返回`schemeUrl`、`applinkUrl`和`normalUrl`之一。

关于此字段的更多信息：

*   最大长度：2048个字符

#### applinkUrl URL

当目标应用已安装时，用于重定向用户打开应用的URL，或者当目标应用未安装时，用于打开WAP页面的URL。对于Android，该URL是一个原生应用链接。对于iOS，该URL是一个通用链接。

注意：当result.resultCode的值为`S`时，需要返回至少一个schemeUrl、applinkUrl或normalUrl。

关于此字段的更多信息：

*   最大长度：2048个字符

#### appIdentifier 字符串

Android的包名，用于在Android应用中打开收银页面。

注意：当result.resultCode的值为`S`且terminalType为APP或WAP时，此字段将返回。

关于此字段的更多信息：

*   最大长度：128个字符

#### normalUrl URL

用于在默认浏览器或内嵌WebView中重定向用户到WAP或WEB页面的URL。

注意：当result.resultCode的值为`S`时，需要返回至少一个schemeUrl、applinkUrl或normalUrl。

更多关于此字段的信息

*   最大长度：2048 个字符

#### authCodeForm - AuthCodeForm 对象

授权二维码的信息。

当支付方式支持通过扫描二维码授权时，此参数会被返回。


API 探索器

示例代码在沙箱中运行

### 请求

URL

北美地区

<https://open-na-global.alipay.com/ams/api/v1/authorizations/consult>

支付方式

![Image 3: AlipayCN](https://gw.alipayobjects.com/mdn/rms_b3f2c2/afts/img/A*g-x4R5biJnsAAAAAAAAAAAAAARQnAQ) AlipayCN

终端类型

![Image 4: APP](https://gw.alipayobjects.com/mdn/rms_b3f2c2/afts/img/A*sHjISq1PKn8AAAAAAAAAAAAAARQnAQ) APP

集成角色

收购方-商户 直接商户

请求体

```json
{
  "authRedirectUrl": "https://www.alipay.com",
  "authState": "STATE_694020584437",
  "customerBelongsTo": "ALIPAY_CN",
  "authClientId": "SM_001",
  "osType": "ANDROID",
  "scopes": [
    "AGREEMENT_PAY"
  ],
  "terminalType": "APP"
}
```

### 响应

响应体

```json
{
  "normalUrl": "https://openauth.****.com/authentication.htm?authId=FBF16F91-28FB-47EC-B9BE-27B285C23CD3",
  "result": {
    "resultCode": "SUCCESS",
    "resultMessage": "success.",
    "resultStatus": "S"
  }
}
```

结果处理逻辑
--------------------

对于不同的请求结果，需要执行不同的操作。详细如下：

* 如果result.resultStatus的值为`S`，则授权URL已成功通过响应中的schemeUrl、applinkUrl或normalUrl字段获取。商家可以将用户重定向到这个URL，以同意授权给予相应的资源访问权限。
* 如果result.resultStatus的值为`U`，API调用状态未知。您可以再次调用此API以重试过程。
* 如果result.resultStatus的值为`F`，则未能获取授权URL。通常，这可能是由于系统缺陷或系统故障导致。请检查错误代码并采取相应措施或联系支付宝技术支持。

### 结果/错误代码

| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 接口调用成功。从响应中获取schemeUrl、applinkUrl或normalUrl。 |
| ACCESS\_DENIED | F | 访问被拒绝。 | 请联系支付宝技术支持获取详细原因。 |
| CLIENT\_FORBIDDEN\_ACCESS\_API | F | 客户端无权使用此API。 | 请联系支付宝技术支持获取详细原因。 |
| INVALID\_ACCESS\_TOKEN | F | 访问令牌已过期、被撤销或不存在。 | 检查accessToken是否正确。如果不正确，请传入正确的值。如果正确，请联系支付宝技术支持以获取详细原因。 |
| INVALID\_API | F | 调用的API无效或未激活。 | 联系支付宝技术支持解决问题。 |
| INVALID\_CLIENT\_STATUS | F | 客户端状态无效。 | 联系支付宝技术支持获取详细原因。 |
| INVALID\_SIGNATURE | F | 签名验证失败。用于签署请求的私钥与Antom Dashboard的公钥不匹配。 | 检查用于签署请求的私钥是否与Antom Dashboard的公钥匹配。以下签名参考信息可能有用：<br>*   请求头中的[签名](https://global.alipay.com/docs/ac/ams/api_fund)字段<br>*   如何[计算签名](https://global.alipay.com/docs/ac/ams/digital_signature) |
| KEY\_NOT\_FOUND | F | 未找到支付宝或商家的私钥或公钥。 | 检查私钥或公钥是否存在。如果不存在，请在Antom仪表盘上传私钥。 |
| MERCHANT\_NOT\_REGISTERED | F | 商家未注册。 | 请使用注册接口注册商家。如果调用注册接口失败，请联系支付宝技术支持。 |
| NO\_INTERFACE\_DEF | F | API未定义。 | 检查URL是否正确。请参考API文档中的端点信息。 |
| NO\_PAY\_OPTIONS | F | 该API不支持此支付方式。 | 检查传递的支付方式是否为customerBelongsTo参数的有效值。如果输入的值正确，请联系支付宝技术支持了解详细原因。 |
| OAUTH\_FAILED | F | OAuth流程失败。 | 请联系支付宝技术支持获取详细原因。 |
| PARAM\_ILLEGAL | F | 必需的参数未传递，或者存在非法参数。例如，非数字输入、无效日期，或者参数的长度和类型错误。 | 检查并确认当前API的必需请求字段（包括头部字段和正文字段）是否正确传递并有效。 |
| PAYMENT\_NOT\_QUALIFIED | F | 商家不具备支付资格，可能是因为未注册、未签订自动扣款协议，或者被禁止支付。 | 联系支付宝技术支持获取详细原因。 |
| PROCESS\_FAIL | F | 发生了一般的业务处理失败。 | 不要重试，通常需要人工干预。建议联系支付宝技术支持来解决问题。 |
| RISK\_REJECT | F | 请求因风险控制被拒绝。 | 提示用户请求被拒绝，因为风险控制未通过。 |
| SYSTEM\_ERROR | F | 系统错误发生。 | 不要重试，联系支付宝技术支持获取更多详细信息。 |
| UNKNOWN\_CLIENT | F | 客户端未知。 | 联系支付宝技术支持获取详细原因。 |
| REQUEST\_TRAFFIC\_EXCEED\_LIMIT | U | 请求流量超过限制。 | 重新调用接口以解决问题。如果未解决，联系支付宝技术支持。 |
| UNKNOWN\_EXCEPTION | U | 由于未知原因，API调用失败。 | 重新调用接口以解决问题。如果未解决，联系支付宝技术支持。 |

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

