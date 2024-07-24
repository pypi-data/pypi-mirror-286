inquireVaulting | Product APIs | Alipay Docs
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Finquire_vaulting)

[Go to Homepage](../../)

Product APIs

[Alipay APIs](/docs/ac/ams/api)

Online payments

Authorization

Vault

[createVaultingSession](/docs/ac/ams/vaulting_session)

[vaultPaymentMethod](/docs/ac/ams/vault_method)

[notifyVaulting](/docs/ac/ams/notify_vaulting)

[inquireVaulting](/docs/ac/ams/inquire_vaulting)

Payment

Subscription

Dispute

Refund

Declaration

In-store payments

inquireVaulting
===============

2023-12-26 08:34

POST /v1/vaults/inquireVaulting

Use the **inquireVaulting** API to inquire about the vaulting status of a payment method.

Structure
=========

A message consists of a header and body. The following sections are focused on the body structure. For the header structure, see:

*   [Request header](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [Response header](https://global.alipay.com/docs/ac/ams/api_fund#WWH90) 

**Note**: Set the data type of each field (except array) as String. This means that you must use double quotation marks (" ") to enclose the field value. Examples:

*   If the data type of a field is Integer and its value is 20, set it as "20".
*   If the data type of a field is Boolean and its value is `true`, set it as "true".  

### Request parameters

#### vaultingRequestId String  REQUIRED

The unique ID that is assigned by a merchant to identify a card vaulting request.

More information about this field

*   This field is an API idempotency field. For vaulting requests that are initiated with the same value of _vaultingRequestId_ and reach a final status of `S` or `F`, the same result is to be returned for the request.

More information about this field

*   Maximum length: 64 characters

### Response parameters

Show all

#### result Result object REQUIRED

Information about the request calling result.

This field does not indicate the vaulting result. This field only indicates whether this interface is called successfully.

Show child parameters

#### vaultingRequestId String  REQUIRED

The unique ID that is assigned by a merchant to identify a card vaulting request.

More information about this field

*   Maximum length: 64 characters

#### normalUrl URL  

The URL that redirects users to a WAP or WEB page in the default browser or the embedded WebView.

When the value of _result.resultStatus_ is `S` and the value of _vaultingStatus_ is `PROCESSING`, one or more of the following URLs may be returned: _schemeUrl_, _applinkUrl_, and _normalUrl_.

When the value of _paymentMethodType_ is `CARD`, the user is required to complete the 3DS authentication on the page accessed through this URL.

More information about this field

*   Maximum length: 2048 characters

#### schemeUrl URL  

The URL scheme that redirects users to open an App in an Android or iOS system when the target App is installed.

When the value of _result.resultStatus_ is `S` and the value of _vaultingStatus_ is `PROCESSING`, one or more of the following URLs may be returned: _schemeUrl_, _applinkUrl_, and _normalUrl_.

More information about this field

*   Maximum length: 2048 characters

#### applinkUrl URL  

The URL that redirects users to open an app when the target app is installed, or to open a WAP page when the target app is not installed. For Android, the URL is a Native App Link. For iOS, the URL is a Universal Link.

When the value of _result.resultStatus_ is `S` and the value of _vaultingStatus_ is `PROCESSING`, one or more of the following URLs may be returned: _schemeUrl_, _applinkUrl_, and _normalUrl_.

More information about this field

*   Maximum length: 2048 characters

#### paymentMethodDetail PaymentMethodDetail object 

The details about the payment method that needs to be vaulted.

This parameter is returned when the value of _vaultingStatus_ is `SUCCESS`.

Show child parameters

#### vaultingStatus String  

Indicates the payment method's vaulting status. Valid values are:

*   `SUCCESS`: indicates that the vaulting is successful. 
*   `FAIL`: indicates that the vaulting failed.
*   `PROCESSING`: indicates that the vaulting is under process. 

This parameter is returned when the value of _result.resultStatus_ is `S`.

More information about this field

*   Maximum length: 10 characters

API Explorer

Sample CodesRun in Sandbox

### Request

URL

North America

https://open-na-global.alipay.com/ams/api/v1/vaults/inquireVaulting

Request Body

Copy

1

2

3

{

"vaultingRequestId": "123456789206"

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

8

9

10

11

12

13

14

15

16

17

{

"paymentMethodDetail": {

"card": {

"brand": "VISA",

"cardToken": "ALIPAY9CGwsAeMBug

          +G2dSKDV6AIsNKTxAFNkOMoj8Gxvt8h0eDUbd6nO5CwMFIjEFERWxCAo

          /b1OjVTvtl1zspyMGcg==",

"maskedCardNo": "\*\*\*\*\*\*\*\*\*\*\*\*8764"

},

"paymentMethodType": "CARD"

},

"vaultingRequestId": "123487889889",

"vaultingStatus": "SUCCESS",

"result": {

"resultCode": "SUCCESS",

"resultMessage": "success.",

"resultStatus": "S"

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Result process logic

For different request results, different actions must be taken. The possible responses for _result.resultStatus_ are:

*   `S`: indicates the API call succeeded. You can get the vaulting result from _vaultingStatus_ in the API response.
*   `F`: indicates the API call failed. For more information on why the call failed, see _result.resultCode_.
*   `U`: indicates the API call failed due to an unknown reason. Retry using the same request ID. 

### Result/Error codes

| Code | Value | Message | Further action |
| --- | --- | --- | --- |
| SUCCESS | S | Success |  |
| VAULTING\_NOT\_EXIST | F | The vaulting request ID does not exist. | Check whether the value of _vaultingRequestId_ is correct. If it is correct, contact Alipay Technical Support for specific reasons.
 |
| UNKNOWN\_EXCEPTION | U | An API call has failed, which is caused by unknown reasons. | Call the interface again to resolve the issue. If not resolved, contact Alipay Technical Support.

 |

![Image 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)

#### Is this page helpful?