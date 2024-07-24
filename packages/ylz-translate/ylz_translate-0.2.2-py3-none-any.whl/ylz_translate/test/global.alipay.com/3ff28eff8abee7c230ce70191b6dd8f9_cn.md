通知扣款（结账支付） | 产品API | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fnotify_capture)  
[返回首页](../../)

产品API  
[支付宝API](/docs/ac/ams/api)  
在线支付  
授权  
安全存储  
支付  
[查询（结账支付）](/docs/ac/ams/consult)  
[支付（结账支付）](/docs/ac/ams/payment_cashier)  
[创建支付会话（结账支付）](/docs/ac/ams/session_cashier)  
[扣款（结账支付）](/docs/ac/ams/capture)  
[支付（协议支付）](/docs/ac/ams/payment_agreement)  
[创建支付会话（EasySafePay）](/docs/ac/ams/createpaymentsession_easypay)  
[支付通知](/docs/ac/ams/paymentrn_online)  
[通知扣款（结账支付）](/docs/ac/ams/notify_capture)  
[查询支付](/docs/ac/ams/paymentri_online)  
[取消支付](/docs/ac/ams/paymentc_online)  
订阅  
争议  
退款  
申报  
店内支付  
通知扣款（结账支付）
==================

2024年4月24日 07:15

**notifyCapture** API 用于在扣款处理达到成功或失败的最终状态时，由支付宝向商家发送扣款结果。

结构
===

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参阅：

*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)
**注意**: 将每个字段（不包括数组）的数据类型设置为字符串。这意味着字段值必须用双引号（" "）括起来。例如：

*   如果字段的数据类型为整数，其值为20，应表示为"20"。
*   如果字段的数据类型为布尔值，其值为`true`，应表示为"true"。
### 请求参数  
显示全部  
#### result 结果对象 **必需**  
支付扣款结果的详细信息，如扣款状态、结果代码和结果消息。  
显示子参数  
#### notifyType 字符串 **必需**  
通知的类型。此API的通知类型为 `CAPTURE_RESULT`。  
#### captureRequestId 字符串 **必需**  
商家为识别一次扣款请求而分配的唯一ID。  
关于此字段的更多信息  
*   最大长度：64 个字符  
#### paymentId 字符串 **必需**  
支付宝为识别一次支付而分配的唯一ID。  
关于此字段的更多信息  
*   最大长度：64 个字符  
#### captureId 字符串 **必需**  
支付宝为识别一次扣款而分配的唯一ID。  
关于此字段的更多信息  
*   最大长度：64 个字符  
#### captureAmount 金额对象 **必需**  
商家在交易货币中请求收取的扣款金额。  
显示子参数  
#### captureTime 日期时间  
支付宝执行支付扣款的时间。  
#### acquirerReferenceNo 字符串  
非支付宝收单方为交易分配的唯一ID。  
关于此字段的更多信息  
*   最大长度：64 个字符
### 响应参数  
显示全部  
#### result 结果对象 **必需**  
一个固定值，用于向支付宝确认已接收到通知。  
显示子参数  
API 探索器
### 请求  
情况  
捕获成功  
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
"resultMessage": "成功。",  
"resultStatus": "S"  
}  
}  
请注意：此请求体表示一个成功的捕获交易，涉及金额为50,000巴西雷亚尔（BRL）。通知类型为"CAPTURE_RESULT"，捕获ID和请求ID分别为"2022XXXXXXX"和"Merchant_Request_ID_XXXXXX"。交易时间是2022年11月10日00:34:52（UTC-8时区）。支付ID同样为"2022XXXXXXX"。结果部分显示操作结果码为"SUCCESS"，表示交易成功，结果状态为"S"，即成功状态。其余的"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"部分在示例中没有提供具体信息，通常可能包含额外的交易细节或安全信息。
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
请注意，以上内容为示例，实际的响应可能包含更详细的数据。在蚂蚁金服的业务中，这样的响应通常表示一个操作或请求已经成功完成。"resultCode"为"SUCCESS"表明操作成功，"resultStatus"的"S"代表状态正常，"resultMessage"则提供了简要的成功信息。在处理实际的API响应时，开发者会根据这些字段来判断请求的结果。
### 结果/错误代码  
| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 捕获成功，无需进一步操作。 |
| ACCESS\_DENIED | F | 访问被拒绝。 | 联系支付宝技术支持获取详细原因。 |
| AUTH\_CANCELLED | F | 支付授权已取消。 | 使用新的 _paymentRequestId_ 启动支付。 |
| AUTH\_EXPIRED | F | 支付授权已过期。 | 使用新的 _paymentRequestId_ 启动支付。 |
| AUTH\_NOT\_FOUND | F | 支付授权未找到。 | 联系支付宝技术支持获取详细原因。 |
| CAPTURE\_AMOUNT\_EXCEED\_AUTH\_LIMIT | F | 捕获总额超过授权支付金额限制。 | 创建新的捕获请求，金额应小于或等于授权支付金额，或联系支付宝技术支持。 |
| CAPTURE\_IN\_PROCESS | U | 捕获处理中。 | 等待支付宝的通知或查询捕获结果。 |
| CURRENCY\_NOT\_SUPPORT | F | 货币不受支持。 | 检查请求中使用的货币，如捕获货币。如果问题持续，请联系支付宝技术支持获取详细原因。 |
| INVALID\_CONTRACT | F | 合同中的参数值与当前交易不符。 | 检查合同中的参数值是否与当前交易匹配。如果值匹配，请联系支付宝技术支持解决问题。 |
| MULTI\_CAPTURE\_NOT\_SUPPORTED | F | 交易不支持多次捕获。 | 联系支付宝技术支持获取详细原因。 |
| NO\_PAY\_OPTIONS | F | 无可用的支付方式。 | 联系蚂蚁金服技术支持获取详细原因。 |
| ORDER\_IS\_CANCELED | F | 交易已取消。 | 使用新的 _paymentRequestId_ 启动支付。 |
| ORDER\_STATUS\_INVALID | F | 交易状态异常，无法进行收款。 | 检查交易状态，如果存在问题，请联系支付宝技术支持协助解决。 |
| PARAM\_ILLEGAL | F | 缺少必需参数或存在非法参数，例如非数字输入、无效日期或参数长度及类型错误。 | 检查并确认当前API的必要请求字段（包括头部字段和正文字段）是否正确传递并有效。 |
| PAYMENT\_COUNT\_EXCEED\_LIMIT | F | 收款次数超过支付方式设定的限制。 | 联系支付宝技术支持了解具体限制。 |
| PROCESS\_FAIL | F | 收款失败。 | 不要重试，通常需要人工干预。建议联系支付宝技术支持排查问题。 |
| REPEAT\_REQ\_INCONSISTENT | F | 提交的请求已存在，且本次请求的参数值与已有请求不一致。 | 确保所有请求字段一致，或使用新的\_paymentRequestId\_\_发起支付。 |
| RISK\_REJECT | F | 请求因风险控制被拒绝。 | 提示用户请求因风险控制失败被拒绝。 |
| USER\_AMOUNT\_EXCEED\_LIMIT | F | 收款金额超过用户支付限额。 | 使用不超过用户支付限额的金额创建新收款，或联系用户或发卡银行。 |
| USER\_BALANCE\_NOT\_ENOUGH | F | 用户余额不足，无法完成收款。 | 联系支付宝技术支持获取详细原因。 |
| USER\_NOT\_EXIST | F | 用户账户在支付方式侧不存在。 | 联系用户或发卡银行。 |
| USER\_STATUS\_ABNORMAL | F | 用户在支付方式端的账户状态异常。 | 联系支付宝技术支持以了解具体原因。 |
| --- | --- | --- | --- |
| UNKNOWN\_EXCEPTION | U | 由于未知原因，API调用失败。 | 重新调用接口以解决问题。如果问题持续，请联系支付宝技术支持。 |

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

![图片3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面有帮助吗？