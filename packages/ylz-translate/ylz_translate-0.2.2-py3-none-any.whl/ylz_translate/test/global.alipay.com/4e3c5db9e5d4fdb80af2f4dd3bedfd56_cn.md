通知纠纷 | 产品API | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fnotify_dispute)  
[返回首页](../../)

产品API  
[支付宝API](/docs/ac/ams/api)  
在线支付  
授权  
安全存储  
支付  
订阅  
纠纷  
[acceptDispute](/docs/ac/ams/accept)  
[supplyDefenseDocument](/docs/ac/ams/supply_evidence)  
[downloadDisputeEvidence](/docs/ac/ams/download)  
[notifyDispute](/docs/ac/ams/notify_dispute)  
退款  
申报  
店内支付  

通知纠纷
==========

2024-04-24 07:15

**notifyDispute** API 用于支付宝向商家发送纠纷信息。

结构
====

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：

*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着必须使用双引号（" "）包围字段值。例如：

*   如果字段的数据类型是整数，值为20，则设置为"20"。
*   如果字段的数据类型是布尔值，值为`true`，则设置为"true"。
### 请求参数  
显示全部  
#### paymentRequestId 字符串  必需  
商家为识别支付请求而分配的唯一ID。  
关于此字段的更多信息：  
*   最大长度：64个字符  
#### disputeId 字符串  必需  
支付宝为识别争议而分配的唯一ID。  
关于此字段的更多信息：  
*   最大长度：64个字符  
#### paymentId 字符串  必需  
支付宝为识别支付而分配的唯一ID。  
关于此字段的更多信息：  
*   最大长度：64个字符  
#### disputeTime 日期时间  
争议创建的日期和时间。  
关于此字段的更多信息：  
*   值遵循[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)标准格式。例如，"2019-11-27T12:01:01+08:00"。  
#### disputeAmount Amount 对象  
存在争议的交易金额。  
当发生争议时，此参数返回。  
显示子参数  
#### disputeNotificationType 字符串  必需  
争议通知类型。有效值包括：  
*   `DISPUTE_CREATED`：表示发生了争议。
*   `DISPUTE_JUDGED`：表示争议已被裁决。
*   `DISPUTE_CANCELLED`：表示用户取消了争议。
*   `DEFENSE_SUPPLIED`：表示您已提交争议的辩护文件。
*   `DEFENSE_DUE_ALERT`：支付宝发出的警告，提示您的辩护在_defenseDueTime_后的24小时内即将过期。  
关于此字段的更多信息：  
*   最大长度：30个字符  
#### disputeReasonMsg 字符串  
争议原因。  
关于此字段的更多信息：  
*   最大长度：256个字符  
#### disputeJudgedTime 日期时间  
争议裁决的日期和时间。  
关于此字段的更多信息：  
*   值遵循[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)标准格式。例如，"2019-11-27T12:01:01+08:00"。
#### 争议判断金额（disputeJudgedAmount）- Amount 对象  
争议的扣款金额。  
此参数在争议被判断时返回。  
显示子参数  

#### 争议判断结果（disputeJudgedResult）- 字符串  
争议判断的结果。有效值包括：  
*   `ACCEPT_BY_CUSTOMER`: 表示争议由客户负责。商户可以在资金解冻后处理交易，如退款给客户。
*   `ACCEPT_BY_MERCHANT`: 表示争议由商户负责。从商户结算账户中扣除，资金将解冻。  
关于此字段的更多信息  
*   最大长度：30 个字符  

#### 防御截止时间（defenseDueTime）- 日期时间  
您无法再为争议辩护的截止时间。  
当 _disputeNotificationType_ 的值为 `DISPUTE_CREATED` 或 `DEFENSE_DUE_ALERT` 时，此参数返回。  

#### 争议原因代码（disputeReasonCode）- 字符串  
表示支付被争议的原因代码。有关原因代码的详细信息，请参阅 [退款原因代码](https://global.alipay.com/docs/ac/dispute/reason_code)。  
当 _disputeNotificationType_ 的值为 `DISPUTE_CREATED` 或 `DISPUTE_JUDGED` 时，此参数返回。  
关于此字段的更多信息  
*   最大长度：64 个字符  

#### 争议来源（disputeSource）- 字符串  
负责处理争议的卡组织。  
当 _disputeNotificationType_ 的值为 `DISPUTE_CREATED` 或 `DISPUTE_JUDGED` 时，此参数返回。  
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
关于发生的争议的通知  
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
"争议金额": {  
"货币": "EUR",  
"值": "1000"  
},  
"争议ID": "202209212501310115730104\*\*\*\*",  
"争议通知类型": "DISPUTE\_CREATED",  
"辩护到期时间": "2023-09-20T23:41:32-07:00",  
"争议时间": "2022-09-20T23:41:32-07:00",  
"争议原因代码": "4853",  
"争议来源": "Mastercard",  
"付款ID": "202209231540108001001888XXXXXX\*\*\*\*",  
"付款请求ID": "requestId\_12345\*\*\*\*"  
}  
请注意，此文本的后半部分似乎被重复的字符“ה”所填充，没有提供额外的信息。在正常情况下，请求体应包含有关争议的详细信息，如金额、ID、通知类型、辩护时间、争议时间、原因代码、来源以及与争议相关的付款ID和请求ID。如果有更多信息，请提供，以便进行翻译。
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
注意：以上内容为示例，实际响应可能包含更多数据。在蚂蚁金服的业务中，"resultCode"为"SUCCESS"表示操作成功，"resultStatus"的"S"通常代表正常状态，"resultMessage"则会给出详细的成功信息。如果需要翻译更详细的文档或有特定的上下文，请提供更多信息。
### 结果/错误代码  
| 代码 | 值 | 消息 |
| --- | --- | --- |
| SUCCESS | S | 成功 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。  
![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)  

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)  

#### 这个页面有帮助吗？