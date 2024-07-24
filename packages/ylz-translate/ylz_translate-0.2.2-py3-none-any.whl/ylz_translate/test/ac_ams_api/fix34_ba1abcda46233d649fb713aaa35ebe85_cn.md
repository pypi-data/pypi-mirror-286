
扣款 (Checkout 支付)
==========================

2024-04-25 06:13

POST /v1/payments/capture

**capture** API 用于从用户账户中扣取已授权的支付资金，并将指定的支付金额转移到商家账户。根据不同的场景，授权支付可以以下列方式之一进行扣款：

*   全额扣款：扣取全部支付金额。
*   部分扣款：扣取部分支付金额。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参阅：

*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**: 除数组外，每个字段的数据类型都应设置为字符串。这意味着字段值必须用双引号（" "）括起来。例如：

*   如果字段的数据类型是Integer，其值为20，则应设置为"20"。
*   如果字段的数据类型是Boolean，其值为`true`，则应设置为"true"。

### 请求参数

显示全部

#### captureRequestId 字符串  必填

商家为识别一次扣款请求而分配的唯一ID。支付宝使用此字段进行幂等性控制。

关于此字段的更多信息：

*   这是一个API幂等性字段。对于具有相同`captureRequestId`值的扣款请求，当达到最终状态（S或F）时，应返回相同的结果。
*   最大长度：64个字符

#### paymentId 字符串  必填

支付宝分配的用于识别支付的唯一ID。

更多关于此字段的信息

*   最大长度：64个字符

#### captureAmount Amount 对象 **必需**

商家在交易货币中请求收取的金额。

显示子参数

### 响应参数

显示全部

#### result Result 对象 **必需**

API 调用的结果。

显示子参数

#### captureRequestId 字符串 

商家分配的用于识别捕捉请求的唯一ID。

当捕捉状态成功时，此参数返回。

更多关于此字段的信息

*   最大长度：64个字符

#### captureId 字符串 

支付宝分配的用于识别捕捉的唯一ID。

当捕捉状态成功时，此参数返回。

更多关于此字段的信息

*   最大长度：64个字符

#### paymentId 字符串 

支付宝分配的用于识别支付的唯一ID。

当扣款状态成功时，此参数返回。

此字段的更多信息

*   最大长度：64 个字符

#### captureAmount Amount 对象

商家在交易货币中请求收取的扣款金额。

当扣款状态成功时，此参数返回。

显示子参数

#### captureTime Datetime 

支付宝完成扣款的时间。

当扣款状态成功时，此参数返回。

此字段的更多信息

*   值遵循 [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) 标准格式。例如，"2019-11-27T12:01:01+08:00"。

#### acquirerReferenceNo 字符串 

非支付宝收单方为交易分配的唯一 ID。

此字段的更多信息

*   最大长度：64 个字符

API 探索器

示例代码 在沙箱中运行

### 请求

URL

北美

https://open-na-global.alipay.com/ams/api/v1/payments/capture

请求体

```json
{
  "paymentId": "20220919194010890100111740275820195",
  "captureRequestId": "capture_cangxi_lj_20220920_005914_845",
  "captureAmount": {
    "currency": "HKD",
    "value": "10"
  }
}
```

### 响应

响应体

```json
{
  "acquirerReferenceNo": "2022091919031300010740267587902",
  "result": {
    "resultStatus": "S",
    "resultCode": "SUCCESS",
    "resultMessage": "success."
  },
  "captureTime": "2022-09-19T09:59:17-07:00",
  "paymentId": "20220919194010890100111740275820195",
  "captureRequestId": "capture_cangxi_lj_20220920_005914_845",
  "captureId": "20220919194010890100111740275850565",
  "captureAmount": {
    "currency": "HKD",
    "value": "10"
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
| AUTH\_NOT\_FOUND | F | 未找到支付授权。 | 请咨询支付宝技术支持以获取详细原因。 |
| CAPTURE\_AMOUNT\_EXCEED\_AUTH\_LIMIT | F | 收款总额超过授权支付金额限制。 | 创建一个新的收款请求，金额应小于或等于授权的支付金额，或联系支付宝技术支持。 |
| CAPTURE\_IN\_PROCESS | U | 收款处理中。 | 等待支付宝的通知，或查询收款结果。 |
| CURRENCY\_NOT\_SUPPORT | F | 货币不支持。 | 检查请求中使用的货币，如收款货币。如果问题持续，请联系支付宝技术支持以获取详细原因。 |
| MULTI\_CAPTURE\_NOT\_SUPPORTED | F | 交易不支持多次收款。 | 请咨询支付宝技术支持以获取详细原因。 |
| INVALID\_CONTRACT | F | 合同中的参数值与当前交易不符。 | 检查合同中的参数值是否与当前交易匹配。如果匹配，请联系支付宝技术支持以解决问题。 |
| NO\_PAY\_OPTIONS | F | 无可用的支付方式。 | 请咨询蚂蚁金服技术支持以获取详细原因。 |
| ORDER\_IS\_CANCELED | F | 交易已取消。 | 使用新的*paymentRequestId*发起支付。 |
| ORDER\_STATUS\_INVALID | F | 交易状态异常，无法进行收款。 | 检查交易状态。如果状态匹配，请联系支付宝技术支持进行故障排查。 |
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

