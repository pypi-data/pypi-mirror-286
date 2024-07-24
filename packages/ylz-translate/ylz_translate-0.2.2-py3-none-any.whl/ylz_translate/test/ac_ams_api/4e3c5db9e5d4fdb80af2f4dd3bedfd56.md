notifyDispute | Product APIs | Alipay Docs
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fnotify_dispute)

[Go to Homepage](../../)

Product APIs

[Alipay APIs](/docs/ac/ams/api)

Online payments

Authorization

Vault

Payment

Subscription

Dispute

[acceptDispute](/docs/ac/ams/accept)

[supplyDefenseDocument](/docs/ac/ams/supply_evidence)

[downloadDisputeEvidence](/docs/ac/ams/download)

[notifyDispute](/docs/ac/ams/notify_dispute)

Refund

Declaration

In-store payments

notifyDispute
=============

2024-04-24 07:15

The **notifyDispute** API is used by Alipay to send the dispute information to the merchant.

Structure
=========

A message consists of a header and body. The following sections are focused on the body structure. For the header structure, see：

*   [Request header](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [Response header](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**Note**: Set the data type of each field (except array) as String. This means that you must use double quotation marks (" ") to enclose the field value. Examples:

*   If the data type of a field is Integer and its value is 20, set it as "20". 
*   If the data type of a field is Boolean and its value is `true`, set it as "true".  

### Request parameters

Show all

#### paymentRequestId String  REQUIRED

The unique ID that is assigned by a merchant to identify a payment request.

More information about this field

*   Maximum length: 64 characters

#### disputeId String  REQUIRED

The unique ID that is assigned by Alipay to identify a dispute.

More information about this field

*   Maximum length: 64 characters

#### paymentId String  REQUIRED

The unique ID that is assigned by Alipay to identify a payment.

More information about this field

*   Maximum length: 64 characters

#### disputeTime Datetime  

The date and time when the dispute is created.

More information about this field

*   The value follows the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) standard format. For example, "2019-11-27T12:01:01+08:00".

#### disputeAmount Amount object 

The amount of the transaction which has a dispute.

This parameter is returned when a dispute occurs.

Show child parameters

#### disputeNotificationType String  REQUIRED

The type of dispute notification. Valid values are:

*   `DISPUTE_CREATED`: indicates that a dispute occurs.
*   `DISPUTE_JUDGED`: indicates that the dispute is judged.  
*   `DISPUTE_CANCELLED`: indicates that the dispute is cancelled by the user.  
*   `DEFENSE_SUPPLIED`: indicates that your defense documents for the dispute are submitted.
*   `DEFENSE_DUE_ALERT`: a warning sent by Alipay that notifies your defense is to be overdue within 24 hours of _defenseDueTime_.

More information about this field

*   Maximum length: 30 characters

#### disputeReasonMsg String  

The dispute reason.

More information about this field

*   Maximum length: 256 characters

#### disputeJudgedTime Datetime  

The date and time when the dispute is judged.

More information about this field

*   The value follows the [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html) standard format. For example, "2019-11-27T12:01:01+08:00".

#### disputeJudgedAmount Amount object 

The deduction amount of the dispute.

This parameter is returned when a dispute is judged.

Show child parameters

#### disputeJudgedResult String  

The result of the dispute judgement. Valid values are:

*   `ACCEPT_BY_CUSTOMER`: Indicates that the dispute is the customer's responsibility. The merchant can process the transaction, such as refunding the customer, after the captured funds are unfrozen.  
*   `ACCEPT_BY_MERCHANT`: Indicates that the dispute is the merchant's responsibility. Deduct from the merchant settlement account, and the captured funds will be unfrozen.  

More information about this field

*   Maximum length: 30 characters

#### defenseDueTime Datetime  

The due time after which you cannot defend the dispute.

This parameter is returned when the value of _disputeNotificationType_ is `DISPUTE_CREATED` or `DEFENSE_DUE_ALERT`.

#### disputeReasonCode String  

The reason code indicating why a payment is disputed. For details about the reason codes, see [Chargeback reason codes](https://global.alipay.com/docs/ac/dispute/reason_code).

This parameter is returned when the value of _disputeNotificationType_ is `DISPUTE_CREATED` or `DISPUTE_JUDGED`.

More information about this field

*   Maximum length: 64 characters

#### disputeSource String  

The card scheme that is responsible for processing the dispute.

This parameter is returned when the value of _disputeNotificationType_ is `DISPUTE_CREATED` or `DISPUTE_JUDGED`.

More information about this field

*   Maximum length: 64 characters

### Response parameters

Show all

#### result Result object REQUIRED

A fixed value, which is sent to Alipay to acknowledge that the notification is received.

Show child parameters

API Explorer

### Request

Case

Notification about an occurred dispute

Request Body

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

11

12

13

14

{

"disputeAmount": {

"currency": "EUR",

"value": "1000"

},

"disputeId": "202209212501310115730104\*\*\*\*",

"disputeNotificationType": "DISPUTE\_CREATED",

"defenseDueTime": "2023-09-20T23:41:32-07:00",

"disputeTime": "2022-09-20T23:41:32-07:00",

"disputeReasonCode": "4853",

"disputeSource": "Mastercard",

"paymentId": "202209231540108001001888XXXXXX\*\*\*\*",

"paymentRequestId": "requestId\_12345\*\*\*\*"

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

### Response

Response Body

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

"resultMessage": "Success"

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

### Result/Error codes

| Code | Value | Message |
| --- | --- | --- |
| SUCCESS | S | Success |

To view the latest updates to the documentation, visit [Release notes](https://global.alipay.com/docs/releasenotes).

![Image 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)

#### Is this page helpful?