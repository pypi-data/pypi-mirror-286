通知捕获 (结账支付)
======================

2024年4月24日 07:15

**notifyCapture** API 用于在支付宝的捕获处理达到成功或失败的最终状态时，向商家发送捕获结果。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参阅：

*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**: 除数组外，每个字段的数据类型均设置为字符串。这意味着字段值必须用双引号（" "）括起来。示例：

*   如果字段的数据类型为整数，其值为20，则应表示为 "20"。
*   如果字段的数据类型为布尔值，其值为 `true`，则应表示为 "true"。

### 请求参数

显示全部

#### result Result对象 **必需**

支付扣款结果的详细信息，如扣款状态、结果代码和结果消息。

显示子参数

#### notifyType 字符串 **必需**

通知的类型。此API的通知类型为 `CAPTURE_RESULT`。

#### captureRequestId 字符串 **必需**

商家为识别一次扣款请求而分配的唯一ID。

关于此字段的更多信息：

*   最大长度：64个字符

#### paymentId 字符串 **必需**

支付宝为识别一次支付分配的唯一ID。

关于此字段的更多信息

*   最大长度：64 个字符

#### captureId 字符串 必填

支付宝为识别一次扣款操作分配的唯一ID。

关于此字段的更多信息

*   最大长度：64 个字符

#### captureAmount 金额对象 必填

商家在交易货币中请求收取的扣款金额。

显示子参数

#### captureTime 日期时间 

支付宝完成扣款的时间。

#### acquirerReferenceNo 字符串 

非支付宝收单机构为交易分配的唯一ID。

关于此字段的更多信息

*   最大长度：64 个字符

### 响应参数

显示全部

#### result 结果对象 必填

一个固定值，发送给支付宝以确认已收到通知。

显示子参数

API 探索器

### 请求

案例

扣款成功

请求体

```json
{
  "captureAmount": {
    "currency": "BRL",
    "value": "50000"
  },
  "notifyType": "CAPTURE_RESULT",
  "captureId": "2022XXXXXXX",
  "captureRequestId": "Merchant_Request_ID_XXXXXX",
  "captureTime": "2022-11-10T00:34:52-08:00",
  "paymentId": "2022XXXXXXX",
  "result": {
    "resultCode": "SUCCESS",
    "resultMessage": "success.",
    "resultStatus": "S"
  }
}
```

### 响应

响应体

```json
{
  "result": {
    "resultCode": "SUCCESS",
    "resultStatus": "S",
    "resultMessage": "Success"
  }
}
```

### 结果/错误代码

| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 捕获成功，无需进一步操作。 |
| ACCESS\_DENIED | F | 访问被拒绝。 | 请咨询支付宝技术支持以获取详细原因。 |
| AUTH\_CANCELLED | F | 支付授权已取消。 | 使用新的 *paymentRequestId* 启动支付。 |
| AUTH\_EXPIRED | F | 支付授权已过期。 | 使用新的 *paymentRequestId* 启动支付。 |
| AUTH\_NOT\_FOUND | F | 未找到支付授权。 | 请咨询支付宝技术支持以获取详细原因。|
| CAPTURE\_AMOUNT\_EXCEED\_AUTH\_LIMIT | F | 支付金额超过授权限额。 | 创建一个新的扣款请求，金额应小于或等于授权的支付金额，或联系支付宝技术支持。|
| CAPTURE\_IN\_PROCESS | U | 扣款处理中。 | 等待支付宝的通知，或查询扣款结果。|
| CURRENCY\_NOT\_SUPPORT | F | 货币不支持。 | 检查请求中使用的货币，例如扣款货币。如果问题仍然存在，请联系支付宝技术支持以获取详细原因。
| INVALID\_CONTRACT | F | 合同中的参数值与当前交易不符。 | 检查合同中的参数值是否与当前交易匹配。如果匹配，请联系支付宝技术支持以解决问题。 |
| MULTI\_CAPTURE\_NOT\_SUPPORTED | F | 该交易不支持多次扣款。 | 请咨询支付宝技术支持以获取详细原因。 |
| NO\_PAY\_OPTIONS | F | 无可用的支付方式。 | 请咨询蚂蚁金服技术支持以获取详细原因。 |
| ORDER\_IS\_CANCELED | F | 交易已被取消。 | 使用新的*paymentRequestId*发起支付。 |
| ORDER\_STATUS\_INVALID | F | 交易状态异常，无法扣款。 | 检查交易状态。如果状态匹配，请联系支付宝技术支持进行故障排查。 |
| PARAM\_ILLEGAL | F | 必需的参数未传递，或者存在非法参数。例如，非数字输入、无效日期，或者参数的长度和类型错误。 | 检查并确认当前API的必需请求字段（包括头部字段和正文字段）是否正确传递并有效。 |
| PAYMENT\_COUNT\_EXCEED\_LIMIT | F | 支付捕获次数超过了支付方式所设定的限制。 | 联系支付宝技术支持了解具体限制。 |
| PROCESS\_FAIL | F | 支付捕获失败。 | 不要重试，通常需要人工干预。建议联系支付宝技术支持来解决问题。 |
| REPEAT\_REQ\_INCONSISTENT | F | 提交的请求已存在，且本次请求的参数值与已有请求不一致。 | 确保所有请求中的字段相同，或者使用新的*paymentRequestId*来发起支付。 |
| RISK\_REJECT | F | 请求因风险控制被拒绝。 | 通知用户请求因风险控制失败而被拒绝。 |
| USER\_AMOUNT\_EXCEED\_LIMIT | F | 扣款金额超过用户支付限额。 | 使用不超过用户支付限额的金额创建新扣款，或联系用户或发卡银行。 |
| USER\_BALANCE\_NOT\_ENOUGH | F | 用户余额不足进行扣款。 | 联系支付宝技术支持获取详细原因。 |
| USER\_NOT\_EXIST | F | 用户在支付方式侧的账户不存在。 | 联系用户或发卡银行。 |
| USER\_STATUS\_ABNORMAL | F | 用户在支付方式侧的账户状态异常。 | 联系支付宝技术支持了解具体原因。 |
| UNKNOWN_EXCEPTION | U | 由于未知原因，API调用失败。 | 重新调用接口以解决问题。如果问题持续存在，请联系支付宝技术支持。 |

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。
