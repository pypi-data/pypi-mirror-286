概览 | 产品API | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_a52690f40beef33d7d37f1bda6f48c27.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_d70d46fd32b98952674df01c03131d87.svg)](/docs/zh-cn/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fapi_fund)

[返回首页](../../zh-cn/)

产品API

[支付宝API](/docs/zh-cn/ac/ams/api)

[概览](/docs/zh-cn/ac/ams/api_fund)

[幂等性](/docs/zh-cn/ac/ams/idempotency)

[消息编码](/docs/zh-cn/ac/ams/me)

[使用SDK进行请求签名和验证签名](/docs/zh-cn/ac/ams/signature_sdk)

[请求签名和验证签名](/docs/zh-cn/ac/ams/digital_signature?pageVersion=34)

[API变更历史](/docs/zh-cn/ac/ams/changehistory)

在线支付

店内支付

概览
====

2024-05-13 07:36

支付宝在线和店内支付产品提供了一组API，允许与支付宝进行集成。您可以使用`POST`方法发送HTTPS请求并接收相应的响应。

以下部分介绍了[消息结构](#tLLkc)和端到端的[消息传输工作流程](#4DTQ1)。

版本管理
==========

当前API版本为`v1`。版本号在URL中指定，例如`https://{域名}/ams/api/v1/payments/pay`。

环境
==========

您可以根据所在地区选择以下列出的域名之一。建议使用加速域名以实现更快地访问支付宝。如果在设置加速域名时遇到问题，请联系支付宝技术支持。

| **地区** | **普通域名** | **加速域名（推荐）** |
| --- | --- | --- |
| 北美 | <https://open-na.alipay.com> | <https://open-na-global.alipay.com> |
| 亚洲 | <https://open-sea.alipay.com> | <https://open-sea-global.alipay.com> |
| 欧洲 | <https://open-eu.alipay.com>（仅限店内支付） | <https://open-de-global.alipay.com> |

表1. 地区域名

消息结构
==========

在进行任何支付操作之前，了解支付宝API的工作原理以及请求和响应的结构至关重要。本节将介绍您的系统与支付宝之间在线消息的一般信息，如消息结构和消息传输工作流程。消息指的是请求消息或响应消息。

请求结构
---------

以下图表展示了请求消息的结构：

![Image 3: 1675842578786-11a67339-2e94-4bae-9955-15ac8cbcd3c1.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1698201692215-d6848f32-110a-4c25-a930-0deff8bed9cf.png)

图1. 请求结构

### URL

请求URL为`https://{域名}/ams/api/{版本}/{端点}`，其结构如下：

*   **域名**: 由钱包后端分配的标准[域名](https://global.alipay.com/docs/ac/ams/api#call)。
*   **版本**: API的版本，例如 `v1` 或 `v2`。
*   **端点**: 接口的端点，例如 `/v1/payments/pay`。

接口可以通过其端点唯一标识。例如，`/v1/payments/pay` 与 `/v2/payments/pay` 是不同的。

### HTTPS 方法

POST

### 请求头

请求头主要包含以下字段。  
**注意**: 字段名称不区分大小写。



| **头字段** | **必需** | **代码示例** |
| --- | --- | --- |
| 签名 | 是 | `signature: algorithm=RSA256, keyVersion=1, signature=****` |
| Content-Type | 否 | `Content-Type: application/json; charset=UTF-8` |
| client-id | 是 | `client-id: ****` |
| request-time | 是 | `request-time: 1685599933871` |
| agent-token | 否 | `agent-token: ****` |



表2. 请求头

每个头字段的详细信息，请参阅以下描述。

#### 签名 必需

签名(_signature_)包含由逗号(,)分隔的键值对。每个键值对是一个等式，由键和等号(=)后的值组成。有关如何生成签名的详细信息，请参阅[生成签名](https://global.alipay.com/docs/ac/ams/digital_signature#gNWs0)部分。

可以配置以下键：

*   **algorithm**：指定用于生成签名的数字签名算法。支持RSA256。
*   **keyVersion**：指定用于生成或验证签名的密钥版本。默认情况下，值为与_Client-Id_关联的最新密钥版本。
*   **signature**：包含请求的签名值。

示例：

复制

    Signature: algorithm=RSA256, keyVersion=1,
    signature=KEhXthj4bJ801Hqw8kaLvEKc0Rii8KsNUazw7kZgjxyGSPuOZ48058UVJUkkR21iD9JkHBGR
    rWiHPae8ZRPuBagh2H3qu7fxY5GxVDWayJUhUYkr9m%2FOW4UQVmXaQ9yn%2Fw2dCtzwAW0htPHYrKMyrT
    pMk%2BfDDmRflA%2FAMJhQ71yeyhufIA2PCJV8%2FCMOa46303A0WHhH0YPJ9%2FI0UeLVMWlJ1XcBo3Jr
    bRFvcowQwt0lP1XkoPmSLGpBevDE8%2FQ9WnxjPNDfrHnKgV2fp0hpMKVXNM%2BrLHNyMv3MkHg9iTMOD%
    2FFYDAwSd%2B6%2FEOFo9UbdlKcmodJwjKlQoxZZIzmF8w%3D%3D

#### 内容类型（Content-Type）可选

_Content-Type_ 指示请求正文的媒体类型，如[RFC2616](https://datatracker.ietf.org/doc/html/rfc2616)中定义。其中，_charset_ 用于生成/验证签名。

内容类型：application/json; charset=UTF-8

#### 客户端ID（client-id）必需

_client-id_ 用于标识客户端，并与用于签名的密钥相关联。关于如何获取客户端ID的详细信息，请参阅[Antom仪表板](https://global.alipay.com/docs/dashboard_en)。

#### 请求时间（request-time）必需

_request-time_ 指定请求发送的时间戳。此字段的值必须精确到毫秒。使用编程语言中的相应方法获取时间戳：

*   Java: `System.currentTimeMillis()`
*   Python: `round(time.time() * 1000)`
*   .Net: `DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()`
*   PHP: `round(microtime(true) * 1000)`

请求时间：1685599933871

#### 代理令牌（agent-token）可选

_agent-token_ 是支付宝颁发给ISV的代理令牌，用于授权ISV调用API。当处理由ISV发起的API调用时，支付宝会验证_agent-token_ 的值是否有效。

**注意：**

*   从Antom仪表盘获取此参数的值。
*   目前，Antom仪表盘自动生成的 `_agent-token_` 值是一个48位的字符串，而此参数的最大长度为128位。

### 请求体

请求体包含JSON格式的详细请求信息。请求体内的字段根据服务的不同而变化。更多信息，请参阅特定API规范的说明。

响应结构
--------------

响应结构如下图所示：

![图片4: 图像](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1675842622240-a4c513d4-908b-4384-b038-3f016f88612e.png)

图2. 响应结构

### 响应头

响应头携带有关响应的信息，主要包括以下字段。

**注意**：字段名称不区分大小写。



| **响应头字段** | **必需** | **代码示例** |
| --- | --- | --- |
| signature | 是 | `signature: algorithm=RSA256, keyVersion=1, signature=****` |
| Content-Type | 否 | `Content-Type: application/json; charset=UTF-8` |
| client-id | 是 | `client-id: ****` |
| response-time | 是 | `response-time: 2019-04-04T12:08:56+05:30` |



表3. 响应头

每个头字段的详细信息，请参阅以下描述。

#### 签名 必需

_signature_ 包含以逗号(,)分隔的键值对。每个键值对是一个等式，由键和用等号(=)连接的值组成。关于如何生成签名的详细信息，请参阅[生成签名](https://global.alipay.com/docs/ac/ams/digital_signature#gNWs0)部分。

可以配置以下键：

*   **algorithm**：指定用于生成签名的数字签名算法。支持RSA256。
*   **keyVersion**：指定用于生成或验证签名的密钥版本。默认情况下，值为与_client-id_关联的最新密钥版本。
*   **signature**：包含请求的签名值。

示例：

复制

    Signature: algorithm=RSA256, keyVersion=1,
    signature=KEhXthj4bJ801Hqw8kaLvEKc0Rii8KsNUazw7kZgjxyGSPuOZ48058UVJUkkR21iD9JkHBGR
    rWiHPae8ZRPuBagh2H3qu7fxY5GxVDWayJUhUYkr9m%2FOW4UQVmXaQ9yn%2Fw2dCtzwAW0htPHYrKMyrT
    pMk%2BfDDmRflA%2FAMJhQ71yeyhufIA2PCJV8%2FCMOa46303A0WHhH0YPJ9%2FI0UeLVMWlJ1XcBo3Jr
    bRFvcowQwt0lP1XkoPmSLGpBevDE8%2FQ9WnxjPNDfrHnKgV2fp0hpMKVXNM%2BrLHNyMv3MkHg9iTMOD%
    2FFYDAwSd%2B6%2FEOFo9UbdlKcmodJwjKlQoxZZIzmF8w%3D%3D

#### Content-Type 可选

**内容类型（Content-Type）** 指示请求正文的媒体类型，如 [RFC2616](https://datatracker.ietf.org/doc/html/rfc2616) 中定义。其中，_charset_ 用于生成/验证签名。

例如：

```
Content-Type: application/json; charset=UTF-8
```

#### 客户端ID（client-id）**必需**

_client-id_ 用于标识客户端，并与用于签名的密钥相关联。关于如何获取客户端ID的详细信息，请参阅 [Antom 控制台](https://global.alipay.com/docs/dashboard_en#Ozw86)。

#### 响应时间（Response-time）**必需**

_Response-time_ 指定发送响应的时间，遵循 [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) 标准。

注意：此字段必须精确到秒。

```
response-time: 2019-04-04T14:08:56+05:30
```

### 响应正文

响应正文包含对客户端的响应信息。这一部分的字段根据服务而变化。然而，始终包含 `result` 字段，它表示 API 调用的结果。

当结果状态 (`resultStatus`) 为失败时，结果代码 (`resultCode`) 是一个错误代码，结果消息 (`resultMessage`) 是一个用于故障排查的错误消息。有关如何解决错误的更多信息，请参阅特定 API 的结果/错误代码部分。



| **字段** | **数据类型** | **必需** | **描述** |
| --- | --- | --- | --- |
| resultStatus | 字符串 | 否 | 结果状态。有效值为：* `S`：成功 * `F`：失败 * `U`：未知 |
| resultCode | 字符串（64） | 否 | 结果代码 |
| resultMessage | 字符串（256） | 否 | 详细描述结果代码和状态的结果消息 |



表4. 响应体

消息传输工作流程
======================

整个交互序列如下所示：

![Image 5: 消息传输工作流程.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1625112891563-6fb47fb0-262b-4bc8-9ba5-5aa376faac8a.png)

图3. 消息传输工作流程

总体流程
------------

按照以下总体流程调用 API。

### 准备工作

为了防止在响应中可能遇到的一些错误，请考虑以下因素：

*   为了避免在响应中可能出现的错误，了解[API幂等性](https://global.alipay.com/docs/ac/ams/idempotency)的概念。
*   对包含特殊字符的请求进行编码。

### 1. 构建请求

按照[请求结构](https://global.alipay.com/docs/ac/ams/api_fund#F18BS)构建请求，例如，在请求头中添加_client-Id_，_request-time_，_signature_等字段。

为了确保消息传输的安全，构建请求时请执行以下安全措施：

*   签名请求消息。所有请求和响应都需要进行消息签名和签名验证。更多信息，请参阅[签名请求和验证签名](https://global.alipay.com/docs/ac/ams/digital_signature)。
*   对请求进行编码，以防止请求中包含的特殊字符可能导致的错误或歧义。详情请参阅[消息编码](https://global.alipay.com/docs/ac/ams/me)。

### 2\. 发送请求

你可以使用你偏好的平台或工具发送请求，例如，通过Postman或cURL命令。

### 3\. 检查响应

响应通常以JSON或XML格式返回。关于响应的详细信息，请参阅[响应结构](#aL4jO)部分。收到响应后，验证响应的签名。

### 4\. 检查状态码

响应数据根据服务的不同而变化。但是，包含API调用结果的`result`字段始终存在。如果发生错误，会返回一个错误响应，其中的`result`对象会提供错误代码和错误消息，以便您排查问题。

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

![图片6](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![图片7](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面是否有帮助？

#### 本页内容

[版本管理](#CrBl2 "版本管理")

[环境](#Clzkg "环境")

[消息结构](#tLLkc "消息结构")

[请求结构](#F18BS "请求结构")

[URL](#fXagV "URL")

[HTTPS方法](#dMgcH "HTTPS方法")

[请求头](#ML5ur "请求头")

[签名](#3RxeL "签名")

[Content-Type](#d8Mc5 "Content-Type")

[client-id](#GMh3X "client-id")

[请求时间](#gMZMn "请求时间")

[代理令牌](#sjPLz "代理令牌")

[请求体](#oNtxc "请求体")

[响应结构](#aL4jO "响应结构")

[响应头](#WWH90 "响应头")

[签名](#xkB9Q "签名")

[Content-Type](#tyqeW "Content-Type")

[client-id](#QihCq "client-id")

[响应时间](#xZUui "响应时间")

[响应体](#eNUbf "响应体")

[消息传输工作流程](#4DTQ1 "消息传输工作流程")

[整体流程](#2tmDE "整体流程")

[准备工作](#3ck4x "准备工作")

[1\. 构建请求](#NrdHS "1. 构建请求")

[2\. 发送请求](#GdgFY "2. 发送请求")

[3\. 检查响应](#UaWGd "3. 检查响应")

[4\. 检查状态码](#dqcPN "4. 检查状态码")