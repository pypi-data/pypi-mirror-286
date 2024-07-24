通知纠纷
==========

2024年4月24日 07:15

### 介绍

`notifyDispute` API 用于向支付宝系统报告和更新关于交易纠纷的状态。当商家需要对已发生的交易纠纷进行反馈或提供新信息时，可以调用此接口。

### 目录

- [调用地址](#调用地址)
- [请求参数](#请求参数)
  - [必填参数](#必填参数)
  - [可选参数](#可选参数)
- [请求示例](#请求示例)
- [响应示例](#响应示例)
- [错误码](#错误码)

### 调用地址

```http
POST https://openapi.alipay.com/gateway.do
```

### 请求参数

#### 必填参数

- `service` - 接口名称，固定值：`notify_dispute`
- `partner` - 合作方ID，由支付宝分配
- `notify_id` - 通知校验ID，由商家通过加密方式生成
- `notify_type` - 通知类型，固定值：`dispute_notify`
- `dispute_id` - 纠纷ID，由支付宝生成
- `dispute_status` - 纠纷状态，例如：`ACCEPTED`, `DEFENDED`, `CLOSED`
- `timestamp` - 请求发送时间，格式：`yyyy-MM-dd HH:mm:ss`

#### 可选参数

- `additional_info` - 额外信息，JSON格式，用于传递纠纷相关详细信息

### 请求示例

```json
POST /gateway.do HTTP/1.1
Content-Type: application/x-www-form-urlencoded

service=notify_dispute
partner=2088102145302467
notify_id=01e90f04b911e816c832b551e828d304
notify_type=dispute_notify
dispute_id=20180420110010000000000000000001
dispute_status=DEFENDED
timestamp=2024-04-24 07:15:00
additional_info={
  "reason": "产品质量问题",
  "evidence_list": [
    {
      "type": "IMAGE",
      "url": "http://example.com/image.jpg"
    },
    {
      "type": "DOCUMENT",
      "url": "http://example.com/document.pdf"
    }
  ]
}
```

### 响应示例

```json
{
  "alipay_sdk": "alipay-sdk-java-dynamicVersionNo",
  "charset": "UTF-8",
  "sign_type": "RSA2",
  "timestamp": "2024-04-24 07:15:00",
  "trade_no": "20180420110010000000000000000001",
  "version": "1.0",
  "result_code": "SUCCESS",
  "result_msg": "操作成功",
  "notify_id": "01e90f04b911e816c832b551e828d304",
  "sign": "HdL9...省略的签名内容..."
}
```

### 错误码

- `DISPUTE_NOT_EXIST` - 纠纷不存在
- `DISPUTE_STATUS_INVALID` - 纠纷状态无效
- `PERMISSION_DENIED` - 无权限操作
- `SYSTEM_ERROR` - 系统错误

---

[返回首页](../../)

**notifyDispute** API 用于支付宝将纠纷信息发送给商家。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：

*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着字段值必须用双引号（" "）包围。例如：

*   如果字段的数据类型为Integer，其值为20，则设置为"20"。
*   如果字段的数据类型为Boolean，其值为`true`，则设置为"true"。

### 请求参数

显示全部

#### paymentRequestId 字符串  必需

商家为识别支付请求分配的唯一ID。

关于此字段的更多信息

*   最大长度：64个字符

#### disputeId 字符串  必需

### 争议ID (disputeId) 字符串 **必需**

支付宝分配的用于识别争议的唯一ID。

更多关于此字段的信息：

*   最大长度：64 个字符

#### 交易ID (paymentId) 字符串 **必需**

支付宝分配的用于识别支付的唯一ID。

更多关于此字段的信息：

*   最大长度：64 个字符

#### 争议时间 (disputeTime) 日期时间

争议创建的日期和时间。

更多关于此字段的信息：

*   值遵循[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)标准格式。例如，"2019-11-27T12:01:01+08:00"。

#### 争议金额 (disputeAmount) Amount 对象

存在争议的交易金额。

当发生争议时，此参数返回。

显示子参数

#### 争议通知类型 (disputeNotificationType) 字符串 **必需**

争议通知的类型。有效值包括：

*   `争议创建`: 表示发生了争议。
*   `争议裁决`: 表示争议已被裁决。
*   `争议取消`: 表示用户已取消争议。
*   `申诉提交`: 表示您已提交争议的申诉材料。
*   `申诉逾期提醒`: 支付宝发出的警告，提示您的申诉在`defenseDueTime`后的24小时内即将逾期。

关于此字段的更多信息

*   最大长度: 30 个字符

#### 争议理由消息 字符串

争议的理由。

关于此字段的更多信息

*   最大长度: 256 个字符

#### 争议裁决时间 日期时间

争议被裁决的日期和时间。

关于此字段的更多信息

*   值遵循[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)标准格式。例如, "2019-11-27T12:01:01+08:00"。

#### 争议裁决金额 金额对象

争议的扣款金额。

当纠纷被裁决时返回此参数。

显示子参数

#### disputeJudgedResult 字符串

纠纷裁决的结果。有效值包括：

*   `ACCEPT_BY_CUSTOMER`：表示纠纷由客户负责。在已捕获的资金解冻后，商家可以处理交易，例如向客户退款。
*   `ACCEPT_BY_MERCHANT`：表示纠纷由商家负责。将从商家结算账户中扣除，已捕获的资金将解冻。

关于此字段的更多信息

*   最大长度：30 个字符

#### defenseDueTime 日期时间

您无法再为纠纷辩护的截止时间。

当 _disputeNotificationType_ 的值为 `DISPUTE_CREATED` 或 `DEFENSE_DUE_ALERT` 时返回此参数。

#### disputeReasonCode 字符串

争议原因代码，表示支付被争议的原因。有关原因代码的详细信息，请参阅[争议原因代码](https://global.alipay.com/docs/ac/dispute/reason_code)。

当_disputeNotificationType_的值为`DISPUTE_CREATED`或`DISPUTE_JUDGED`时，此参数返回。

关于此字段的更多信息：

*   最大长度：64个字符

#### disputeSource 字符串

负责处理争议的卡组织。

当_disputeNotificationType_的值为`DISPUTE_CREATED`或`DISPUTE_JUDGED`时，此参数返回。

关于此字段的更多信息：

*   最大长度：64个字符

### 响应参数

显示全部

#### result 结果对象 必填

一个固定值，发送给支付宝以确认已收到通知。

显示子参数

API 探索器

### 请求

案例

已发生的争议通知

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

{

```json
{
  "currency": "EUR",
  "value": "1000",
  "disputeId": "202209212501310115730104****",
  "disputeNotificationType": "DISPUTE_CREATED",
  "defenseDueTime": "2023-09-20T23:41:32-07:00",
  "disputeTime": "2022-09-20T23:41:32-07:00",
  "disputeReasonCode": "4853",
  "disputeSource": "Mastercard",
  "paymentId": "202209231540108001001888XXXXXX****",
  "paymentRequestId": "requestId_12345****"
}
```

请注意，JSON键未被翻译，以遵循您的指示。这段JSON数据包含以下信息：

- 货币类型（currency）：欧元（EUR）
- 金额（value）：1000
- 争议ID（disputeId）：202209212501310115730104后面有星号隐藏部分
- 争议通知类型（disputeNotificationType）：争议创建（DISPUTE_CREATED）
- 回应截止时间（defenseDueTime）：2023年9月20日23:41:32（太平洋夏令时）
- 争议时间（disputeTime）：2022年9月20日23:41:32（太平洋夏令时）
- 争议原因代码（disputeReasonCode）：4853
- 争议来源（disputeSource）：万事达卡（Mastercard）
- 付款ID（paymentId）：202209231540108001001888XXXXXX后面有星号隐藏部分
- 付款请求ID（paymentRequestId）：requestId_12345后面有星号隐藏部分

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

| 代码 | 值 | 消息 |
| --- | --- | --- |
| SUCCESS | S | 成功 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。

![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面是否有帮助？