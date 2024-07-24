vaultPaymentMethod | Product APIs | Alipay Docs
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fvault_method)

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

vaultPaymentMethod
==================

2024-03-14 08:39

POST /v1/vaults/vaultPaymentMethod

Use the **vaultPaymentMethod** API to vault a payment method prior to initiating a payment. From the API response, you can obtain _cardToken_ or one or more of _normalUrl, schemeUrl, or applinkUrl_. _cardToken_ is used to initiate payments using the [**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier) API, while the URLs can be used to redirect the user to complete the vaulting.

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

#### vaultingRequestId String  REQUIRED

The unique ID that is assigned by a merchant to identify a card vaulting request.

More information about this field

*   This field is an API idempotency field.For vaulting requests that are initiated with the same value of vaultingRequestId and reach a final status of S or F, the same result is to be returned for the request.
*   Maximum length: 64 characters

#### vaultingNotificationUrl String  REQUIRED

The URL that is used to receive the vaulting result notification.

More information about this field

*   Maximum length: 2048 characters

#### redirectUrl String  REQUIRED

The merchant page URL that the buyer is redirected to after the vaulting process is completed.

More information about this field

*   Maximum length: 2048 characters

#### merchantRegion String  

The country or region where the merchant operates the business. The value of this parameter is a 2-letter country or region code based on the [ISO 3166 Country Codes](https://www.iso.org/obp/ui/#search) standard.

Some possible values are `US`, `SG`, `HK`, `PK`, `JP`, `CN`, `BR`, `AU`, and `MY`.

Specify this parameter when you use the Global Acquirer Gateway (GAGW) product.

More information about this field

*   Maximum length: 2 characters

#### paymentMethodDetail PaymentMethodDetail object REQUIRED

The details about the payment method that needs to be vaulted.

Show child parameters

#### env Env object REQUIRED

Information about the environment where the order is placed, such as the device information.

Show child parameters

### Response parameters

Show all

#### result Result object REQUIRED

The result of the API call.

Show child parameters

#### vaultingRequestId String  REQUIRED

The unique ID that is assigned by a merchant to identify a card vaulting request.

More information about this field

*   Maximum length: 64 characters

#### paymentMethodDetail PaymentMethodDetail object 

The details about the payment method that needs to be vaulted.

This parameter is returned when the value of _result.resultStatus_ is `S`.

Show child parameters

#### normalUrl String  

The URL that redirects the user to a WAP or WEB page in the default browser or the embedded WebView.

When the value of _result.resultCode_ is `VERIFICATION_IN_PROCESS`, one or more of the following URLs may be returned: _schemeUrl_, _appLinkUrl_, and _normalUrl_.

When the value of _paymentMethodType_ is `CARD`, the user is required to complete the 3DS authentication on the page accessed through this URL.

More information about this field

*   Maximum length: 2048 characters

#### schemeUrl String  

The URL scheme that redirects the user to open an app in an Android or iOS system when the target app is installed.

More information about this field

*   Maximum length: 2048 characters

#### applinkUrl String  

The URL that redirects the user to open an app when the target app is installed, or to open a WAP page when the target app is not installed.

More information about this field

*   Maximum length: 2048 characters

API Explorer

Sample CodesRun in Sandbox

### Request

URL

North America

https://open-na-global.alipay.com/ams/api/v1/vaults/vaultPaymentMethod

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

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

{

"vaultingRequestId": "123456789206",

"vaultingNotificationUrl": "www.test.com",

"redirectUrl": "www.test.com",

"paymentMethodDetail": {

"paymentMethodType": "CARD",

"card": {

"cardNo": "4112273146798764",

"brand": "VISA",

"cardholderName": {

"firstName": "xu",

"middleName": "fang",

"lastName": "jie",

"fullName": "xufangjie"

},

"billingAddress": {

"region": "CN",

"address1": "gongzhuan Road",

"city": "hangzhou",

"state": "zhejiang",

"zipCode": "310000"

},

"cvv": "123",

"expiryYear": "26",

"expiryMonth": "08",

"businessRegistrationNo": "96"

}

},

"env": {

"terminalType": "app"

}

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

*   `S`: indicates the API call succeeded. Obtain _cardToken_ from the response in this API. Then use the value of _cardToken_ in the [**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier) API when initiating payments.
*   `F`: indicates the API call failed. For more information on why the call failed, see _result.resultCode_.
*   `U`: When this value is returned, take action depending on whether or not the value of _resultCode_ is `VERIFICATION_IN_PROCESS`:

*   Result code is not `VERIFICATION_IN_PROCESS`: The API call fails. Call this API again with a new _vaultingRequestId value_.
*   Result code is `VERIFICATION_IN_PROCESS`: Check whether one or more of the three URLs (_appLinkUrl_, _normalUrl_, _schemeUrl_) are returned:

*   one or more of the URLs returned: The vaulting is created successfully. Redirect your user to the specific URL provided to complete the vaulting.
*   no URLs returned: The vaulting creation fails. Call this API again with a new _vaultingRequestId_ value. If the issue persists, contact Alipay Technical Support.  

### Result/Error codes

| Code | Value | Message | Further action |
| --- | --- | --- | --- |
| SUCCESS | S | Success | The vaulting session is successfully created. No further action is needed.
 |
| PARAM\_ILLEGAL | F | The required parameters are not passed, or illegal parameters exist. For example, a non-numeric input, an invalid date, or the length and type of the parameter are wrong. | Check and verify whether the required request fields (including the header fields and body fields) of the current API are correctly passed and valid.

 |
| PROCESS\_FAIL | F | A general business failure occurred. | Do not retry. Human intervention is usually needed. It is recommended that you contact Alipay Technical Support to troubleshoot the issue.

 |
| UNKNOWN\_EXCEPTION | U | An API call has failed, which is caused by unknown reasons. | Call the interface again to resolve the issue. If not resolved, contact Alipay Technical Support.

 |
| VERIFICATION\_IN\_PROCESS | U | The verification of the payment method information is under process. | Get any of the URLs (_appLinkUrl, normalUrl, schemeUrl_) and open the URL. If no URL is returned, call this API again with a new request ID. If the issue persists, contact Alipay Technical Support.

 |
| VERIFICATION\_FAIL | F | The verification of the payment method information failed. | Call this API again with a new request ID.

 |

To view the latest updates to the documentation, visit [Release notes](https://global.alipay.com/docs/releasenotes).

![Image 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)

#### Is this page helpful?