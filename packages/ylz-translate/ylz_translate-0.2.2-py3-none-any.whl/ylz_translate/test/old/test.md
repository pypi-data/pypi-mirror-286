APM payments | Checkout Payment | Alipay Docs
































[![Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)[Go to Homepage](../../)Checkout Payment[Overview](/docs/ac/cashierpay/overview)Accept paymentsSDK integrationAPI-only integration[APM paymentsAPM](/docs/ac/cashierpay/apm_api)Card paymentsCardAfter paymentsPayment methodsOther resourcesAdvanced features[Pre-front solutionAPI](/docs/ac/cashierpay/prefront)[Buy now pay laterAPI](/docs/ac/cashierpay/bnpl)[Card vaultingAPI](/docs/ac/cashierpay/cv)[Card vaultingSDK](/docs/ac/cashierpay/cvsdk)[Card payment featuresAPISDK](/docs/ac/cashierpay/mf?pageVersion=7)APM payments
============

2024-05-11 10:13Checkout payment can help your website or application start to accept payments online. This article introduces the integration solution to support accepting payment from the desktop browser, mobile browser or app. After integration, you can access various payment methods like digital wallets, bank cards, and bank transfers.

User experience
===============

WebWAPAppWeb user experience
-------------------

For payments initiated on a desktop website, you need to redirect the buyer to the redirection URL or open the URL in a new tab.








![APM payments](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png)






WAP user experience
-------------------

In the wap scenario, different payment methods may return some or all of the following three URLs in the response of the **pay** API:




| **Link type** | **User experience** | |
| --- | --- | --- |
| applinkUrl | The payment method app is installed.       APM payments     The payment method app is not installed.       APM payments | If the buyer installs the corresponding payment method app, the app will be automatically pulled up, and the h5 page will be displayed if the app of the channel is not installed. The page capabilities of specific h5 will be provided differently depending on different payment methods. |
| schemeUrl | The payment method app is installed.       APM payments     The payment method app is not installed.       image.png  败,无法推进支付唤起支付方式APP失付方式选择页手机浏览器NTMETHODS | If the buyer installs the payment method app, it will automatically redirect to the app. If it is not installed, the app cannot be launched and will stay on the current page. |
| normalUrl | APM payments | Display the h5 page of this payment method. |


App user experience
-------------------

In the app scenario, different payment methods may return some or all of the following three URLs in the response of the **pay** API:




| **Link type** | **User experience** | |
| --- | --- | --- |
| applinkUrl | The payment method app is installed.       APM payments     The payment method app is not installed.       APM payments | If the buyer installs the corresponding payment method app, the app will be automatically pulled up, and the h5 page will be displayed if the app of the channel is not installed. The page capabilities of specific h5 will be provided differently depending on different channels. |
| schemeUrl | The payment method app is installed.       APM payments     The payment method app is not installed.       image.png  败,无法推进支付唤起支付方式APP失付方式选择页手机浏览器NTMETHODS | If the buyer installs the payment method app, it will automatically redirect to the app. If it is not installed, the app cannot be launched and will stay on the current page. |
| normalUrl | APM payments | Display the h5 page of this payment method. |


Payment flow
============

For each payment method, the payment flow composed of the following steps:

![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")

1. **The buyer enters the checkout page.**
2. **Create the**[**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier)**request**  
After the buyer selects a payment method and submits the order, call the [**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier) API to obtain the payment link to complete the payment.
3. **Handle the payment continuation URL**  
The payment continuation URL is to be returned to the client. You need to redirect the buyer to the payment continuation URL. The payment continuation URL proceeds the payment process with different operations based on the characteristics of payment methods, such as collecting information, redirecting users, invoking the app, displaying QR codes, and performing verifications.
4. **Get the payment result**  
Obtain the payment result using one of the following two methods:
+ Asynchronous notification: Specify the *paymentNotifyUrl* in the [**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier) API to set the address for receiving asynchronous notifications. When the payment is successful or expires, Antom uses [**notifyPayment**](https://global.alipay.com/docs/ac/cashierpay/overview) to send asynchronous notifications to you.
+ Synchronous inquiry: Call the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API to check the payment status.

Integration steps
=================

Start your integration by taking the following steps:

1. (Optional) Add a list of payment methods
2. Invoke the pay API and get the payment continuation URL
3. Obtain the payment results

Step 1: (Optional) Add a list of payment methods Client-side
------------------------------------------------------------

Add the logo and name of the payment methods to be integrated to the payment method list on the payment page for buyers to select. You can obtain the logo and name in one of the following two ways:

* Contact Antom Technical Support to obtain. The logo for Alipay+ payment methods needs to comply with the Alipay+ brand specifications, and can be self-generated according to the size and style you need. Refer to [Brand asset](https://global.alipay.com/docs/ac/ref/brandasset) for more information.
* Call the **consult** API to obtain the payment methods and logo URL supported by the current transactions based on the currency, transaction initiation terminal type, buyer region, and contracted payment methods.

The following figures show the page effect after adding a payment method:

WebWAPApp### Web page effect








![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")






### WAP page effect








![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")



PAYMENTMETHOD

PLAYER450455

PENGLISH

9.99USD

9.99USB

PAYNOW

CONFIRMORDER

3+50

FPX

COM

:0.1USD

PAY

KAKAOAY

FPX

999

TOTAL:

TOKENS

大小


### APP page effect








![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")






Step 2: Invoke the pay API and get the payment continuation URL Server-sideClient-side
--------------------------------------------------------------------------------------

When the buyer selects a payment method provided by Antom to make a payment, you need to collect key information such as the payment request ID, order amount, payment method, transaction environment information, order description, URL of the payment redirection page, and URL for receiving the payment result notification. Then, call the **pay** API to obtain the payment continuation URL, and redirect the buyer to the checkout page specified by the payment continuation URL for payment.

### Initiate a payment request Server-side

Antom provides server-side API libraries for multiple languages. The following code uses Java as an example. You need to install Java 6 or higher.

#### Install an API library

You can find the latest version on [GitHub](https://github.com/alipay/global-open-sdk-java).

copy
```
<dependency>
  <groupId>com.alipay.global.sdk</groupId>
  <artifactId>global-open-sdk-java</artifactId>
  <version>2.0.21</version>
</dependency>
```
#### Initialize the request instance

copy
```
String merchantPrivateKey = "YOUR PRIVATE KEY";
String alipayPublicKey = "ALIPAY PUBLIC KEY"
AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG,
                merchantPrivateKey, alipayPublicKey);
```
#### Create a payment request

The following parameters are included in the payment request.



| **Parameter name** | **Is required** | **Description** |
| --- | --- | --- |
| productCode | Yes | In this scenario, the field is fixed to `CASHIER_PAYMENT`. |
| paymentRequestId | Yes | A unique ID generated by the merchant. |
| paymentAmount | Yes | Payment amount, which is set to the smallest unit of the payment currency. |
| paymentMethod | Yes | Payment method enumeration value. |
| paymentRedirectUrl | Yes | The payment result page of the merchant side, which needs to be displayed according to the results of the server. |
| paymentNotifyUrl | No | The payment result notification address, which can be specified via the API or set a fixed value in the portal. |
| settlementStrategy | No | The settlement currency of the payment. If you have signed multiple settlement currencies, you need to specify it in the API. |
| order | Yes | Order information, including order amount, order ID, and order description. |
| env | Yes | The environment in which the buyer initiates a transaction. |

For more information about the whole parameters, refer to [**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

The following sample code is used for initiating a payment:

copy
```
AlipayPayRequest alipayPayRequest = new AlipayPayRequest();
alipayPayRequest.setClientId(CLIENT_ID);
alipayPayRequest.setPath("/ams/api/v1/payments/pay");
alipayPayRequest.setProductCode(ProductCodeType.CASHIER_PAYMENT);

// replace to your paymentRequestId
alipayPayRequest.setPaymentRequestId("paymentRequestId01");

// set amount
Amount amount = new Amount();
amount.setCurrency("HKD");
amount.setValue("100");
alipayPayRequest.setPaymentAmount(amount);

// set paymentMethod
PaymentMethod paymentMethod = new PaymentMethod();
paymentMethod.setPaymentMethodType("ALIPAY_HK");
alipayPayRequest.setPaymentMethod(paymentMethod);

// set order Info
Order order = new Order();
order.setReferenceOrderId("referenceOrderId01");
order.setOrderDescription("antom test order");
order.setOrderAmount(amount);
alipayPayRequest.setOrder(order);

//set env Info
Env env = new Env();
env.setTerminalType(TerminalType.WAP);
env.setClientIp("114.121.121.01");
env.setOsType(OsType.ANDROID);
alipayPayRequest.setEnv(env);

// replace to your notify url
alipayPayRequest.setPaymentNotifyUrl("http://www.yourNotifyUrl.com");

// replace to your redirect url
alipayPayRequest.setPaymentRedirectUrl("http://www.yourRedirectUrl.com");

//do the Payment
AlipayPayResponse alipayPayResponse = null;
try {
    alipayPayResponse = defaultAlipayClient.execute(alipayPayRequest);
} catch (AlipayApiException e) {
    String errorMsg = e.getMessage();
    // handle error condition
}
```
The following code shows a sample of the request message:

WebWAPApp##### Web sample code


copy
```
{
    "paymentNotifyUrl": "http://www.yourNotifyUrl.com",
    "paymentRequestId": "paymentRequestId01",
    "env": {
        "terminalType": "WEB",
        "clientIp": "114.121.121.01"
    },
    "paymentAmount": {
        "currency": "HKD",
        "value": "100"
    },
    "productCode": "CASHIER_PAYMENT",
    "paymentRedirectUrl": "http://www.yourRedirectUrl.com",
    "paymentMethod": {
        "paymentMethodType": "ALIPAY_HK"
    },
    "order": {
        "orderAmount": {
            "currency": "HKD",
            "value": "100"
        },
        "referenceOrderId": "referenceOrderId01",
        "orderDescription": "antom test order"
    }
}
```

##### WAP sample code


copy
```
{
    "paymentNotifyUrl": "http://www.yourNotifyUrl.com",
    "paymentRequestId": "paymentRequestId01",
    "env": {
        "terminalType": "WAP",
        "clientIp": "114.121.121.01",
        "osType": "ANDROID"
    },
    "paymentAmount": {
        "currency": "HKD",
        "value": "100"
    },
    "productCode": "CASHIER_PAYMENT",
    "paymentRedirectUrl": "http://www.yourRedirectUrl.com",
    "paymentMethod": {
        "paymentMethodType": "ALIPAY_HK"
    },
    "order": {
        "orderAmount": {
            "currency": "HKD",
            "value": "100"
        },
        "referenceOrderId": "referenceOrderId01",
        "orderDescription": "antom test order"
    }
}
```

##### App sample code


copy
```
{
    "paymentNotifyUrl": "http://www.yourNotifyUrl.com",
    "paymentRequestId": "paymentRequestId01",
    "env": {
        "terminalType": "APP",
        "clientIp": "114.121.121.01",
        "osType": "ANDROID"
    },
    "paymentAmount": {
        "currency": "HKD",
        "value": "100"
    },
    "productCode": "CASHIER_PAYMENT",
    "paymentRedirectUrl": "http://www.yourRedirectUrl.com",
    "paymentMethod": {
        "paymentMethodType": "ALIPAY_HK"
    },
    "order": {
        "orderAmount": {
            "currency": "HKD",
            "value": "100"
        },
        "referenceOrderId": "referenceOrderId01",
        "orderDescription": "antom test order"
    }
}
```

##### FAQs

###### How to set the value of terminalType?

* If the buyer initiates a transaction from PC, the *terminalType* needs to be specified as `WEB`.
* If the buyer initiates a transaction from the mobile browser, the *terminalType* needs to be specified as `WAP`. Add the *osType* parameter and fill in the corresponding system parameters `ANDROID` or `IOS` according to the buyer's mobile phone.
* If the buyer initiates a transaction from app, the *terminalType* needs to be specified as `APP`.

###### Can Chinese characters be used in the request?

Do not use Chinese characters in the request field to avoid incompatible payment methods, such as QRIS and Mastercard.

###### How to set the payment result notification address？

Antom will send the payment result through the [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online), which you can specify in the **pay** API via the *paymentNotifyUrl* parameter. If the address of each payment is the same, you can also configure it in the Antom Dashboard. If you have configured the address and set the parameter in the API, Antom will use the address set in the API.

### Receive a payment response Server-side

The following code is the sample response:

WebWAPApp##### Web sample code


copy
```
{
    "normalUrl": "https://open-sea.alipayplus.com/api/open/v1/ac/cashier/self/codevalue/checkout.htm?codeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040090bbmmzTC4BzSex92tUglv31de",
    "orderCodeForm": {
        "codeDetails": [
            {
                "codeValue": "https://global.alipay.com/281002040090bbmmzTC4BzSex92tUglv31de",
                "displayType": "TEXT"
            },
            {
                "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040090bbmmzTC4BzSex92tUglv31de&picSize=L",
                "displayType": "BIGIMAGE"
            },
            {
                "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040090bbmmzTC4BzSex92tUglv31de&picSize=M",
                "displayType": "MIDDLEIMAGE"
            },
            {
                "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040090bbmmzTC4BzSex92tUglv31de&picSize=S",
                "displayType": "SMALLIMAGE"
            }
        ],
        "expireTime": "2024-01-15T01:34:45-08:00"
    },
    "paymentActionForm": "{\"method\":\"GET\",\"paymentActionFormType\":\"RedirectActionForm\",\"redirectUrl\":\"https://open-sea.alipayplus.com/api/open/v1/ac/cashier/self/codevalue/checkout.htm?codeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040090bbmmzTC4BzSex92tUglv31de\"}",
    "paymentAmount": {
        "currency": "HKD",
        "value": "100"
    },
    "paymentCreateTime": "2024-01-15T01:20:46-08:00",
    "paymentId": "20240115194010800100188640298283440",
    "paymentRequestId": "PAY_20240115172044263",
    "redirectActionForm": {
        "method": "GET",
        "redirectUrl": "https://open-sea.alipayplus.com/api/open/v1/ac/cashier/self/codevalue/checkout.htm?codeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040090bbmmzTC4BzSex92tUglv31de"
    },
    "result": {
        "resultCode": "PAYMENT_IN_PROCESS",
        "resultMessage": "payment in process",
        "resultStatus": "U"
    }
}
```

##### WAP sample code


copy
```
{
    "appIdentifier": "hk.alipay.wallet",
    "applinkUrl": "https://render.alipay.hk/p/w/hk-ulink/?path=/mobile&scheme=alipayhk%3A%2F%2Fplatformapi%2FstartApp%3FappId%3D85200168%26fromSite%3Dapp%26CashierAction%3DtradePay%26orderCode%3Dhttps%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR%26paymentRedirectUrl%3Dhttps%3A%2F%2Fkademo.intlalipay.cn%2Fmelitigo%2FTest_114.html%26terminalType%3DWAP",
    "normalUrl": "https://render.alipay.hk/p/h5/hk-cashier-merchant/www/index.html/#/otp?scene=uefa&redirectUrl=https%3A%2F%2Frender.alipay.hk%2Fp%2Fh5%2Fhk-cashier-merchant%2Fwww%2Findex.html%23%2Fpreorder%3ForderCode%3Dhttps%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR",
    "orderCodeForm": {
        "codeDetails": [
            {
                "codeValue": "https://global.alipay.com/281002040092tDM89hJ66zUrMS9hbIRv3kWR",
                "displayType": "TEXT"
            },
            {
                "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR&picSize=L",
                "displayType": "BIGIMAGE"
            },
            {
                "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR&picSize=M",
                "displayType": "MIDDLEIMAGE"
            },
            {
                "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR&picSize=S",
                "displayType": "SMALLIMAGE"
            }
        ],
        "expireTime": "2024-02-28T19:53:58-08:00"
    },
    "paymentActionForm": "{\"method\":\"GET\",\"paymentActionFormType\":\"RedirectActionForm\",\"redirectUrl\":\"https://render.alipay.com/p/w/ac-fe-adaptor/?ACCodeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR&paymentMethodType=ALIPAY_HK&ACPaymentRedirectUrl=https%3A%2F%2Fkademo.intlalipay.cn%2Fmelitigo%2FTest_114.html&ACAppType=WAP\"}",
    "paymentAmount": {
        "currency": "HKD",
        "value": "100"
    },
    "paymentCreateTime": "2024-02-28T19:40:00-08:00",
    "paymentId": "20240229194010800100188940208068249",
    "paymentRequestId": "PAY_20240229113956783",
    "redirectActionForm": {
        "method": "GET",
        "redirectUrl": "https://render.alipay.com/p/w/ac-fe-adaptor/?ACCodeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040092tDM89hJ66zUrMS9hbIRv3kWR&paymentMethodType=ALIPAY_HK&ACPaymentRedirectUrl=https%3A%2F%2Fkademo.intlalipay.cn%2Fmelitigo%2FTest_114.html&ACAppType=WAP"
    },
    "result": {
        "resultCode": "PAYMENT_IN_PROCESS",
        "resultMessage": "payment in process",
        "resultStatus": "U"
    }
}
```

##### App sample code


copy
```
{
  "appIdentifier": "hk.alipay.wallet",
  "applinkUrl": "https://render.alipay.hk/p/w/hk-ulink/?path=/mobile&scheme=alipayhk%3A%2F%2Fplatformapi%2FstartApp%3FappId%3D85200168%26fromSite%3Dapp%26CashierAction%3DtradePay%26orderCode%3Dhttps%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB%26paymentRedirectUrl%3Dhttps%3A%2F%2Fkademo.intlalipay.cn%2Forder%2Fdetail%3Fid%3DALIPAY_HK_1709199158552F696Z%26wallet%3DALIPAY_HK%26terminalType%3DWAP",
  "normalUrl": "https://render.alipay.hk/p/h5/hk-cashier-merchant/www/index.html/#/otp?scene=uefa&redirectUrl=https%3A%2F%2Frender.alipay.hk%2Fp%2Fh5%2Fhk-cashier-merchant%2Fwww%2Findex.html%23%2Fpreorder%3ForderCode%3Dhttps%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB",
  "orderCodeForm": {
    "codeDetails": [
      {
        "codeValue": "https://global.alipay.com/281002040090cQa97QFkz1kHL8zTDW47PyqB",
        "displayType": "TEXT"
      },
      {
        "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB&picSize=L",
        "displayType": "BIGIMAGE"
      },
      {
        "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB&picSize=M",
        "displayType": "MIDDLEIMAGE"
      },
      {
        "codeValue": "https://global.alipay.com/merchant/order/showQrImage.htm?code=https%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB&picSize=S",
        "displayType": "SMALLIMAGE"
      }
    ],
    "expireTime": "*************************"
  },
  "paymentActionForm": "{\"method\":\"GET\",\"paymentActionFormType\":\"RedirectActionForm\",\"redirectUrl\":\"https://render.alipay.com/p/w/ac-fe-adaptor/?ACCodeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB&paymentMethodType=ALIPAY_HK&ACPaymentRedirectUrl=https%3A%2F%2Fkademo.intlalipay.cn%2Forder%2Fdetail%3Fid%3DALIPAY_HK_1709199158552F696Z%26wallet%3DALIPAY_HK&ACAppType=WAP\"}",
  "paymentAmount": {
    "currency": "HKD",
    "value": "100"
  },
  "paymentCreateTime": "2024-02-29T01:32:41-08:00",
  "paymentId": "20240229194010800100188010209093907",
  "paymentRequestId": "ALIPAY_HK_1709199158552F696Z",
  "redirectActionForm": {
    "method": "GET",
    "redirectUrl": "https://render.alipay.com/p/w/ac-fe-adaptor/?ACCodeValue=https%3A%2F%2Fglobal.alipay.com%2F281002040090cQa97QFkz1kHL8zTDW47PyqB&paymentMethodType=ALIPAY_HK&ACPaymentRedirectUrl=https%3A%2F%2Fkademo.intlalipay.cn%2Forder%2Fdetail%3Fid%3DALIPAY_HK_1709199158552F696Z%26wallet%3DALIPAY_HK&ACAppType=WAP"
  },
  "result": {
    "resultCode": "PAYMENT_IN_PROCESS",
    "resultMessage": "payment in process",
    "resultStatus": "U"
  }
}
```

##### FAQs

###### What is the normalUrl?

For web transactions, Antom returns *normalUrl*, which the server-side needs to pass to the client-side for redirection. When you initiate payment for the same order again, you need to obtain a new *normalUrl* for redirection.

###### What is the paymentId?

If you store the corresponding order number for subsequent refunds and reconciliations, you can specify the *paymentId*.

### Redirect to the Checkout page of the payment method Client-side

WebWAPApp##### Link type of web

The merchant server passes the *normalUrl* to the client, and the client page handles the redirection process to *normalUrl*.

##### Link type of WAP

The server-side passes the *normalUrl* to the client-side, which is redirected from the client-side page.

##### Link type of app

For app transactions, Antom will return one or more payment links of *normalUrl*, *applinkUrl*, and *schemeUrl* according to the capabilities of the payment method after initiating a payment request.




| **Link type** | **Features** | **Methods** |
| --- | --- | --- |
| applinkUrl | If the buyer installs the payment method app, directly pull up the app checkout page. If the buyer does not have the payment method app installed, pull up the mobile browser. | Redirect to the merchant app to open this link. Refer to [Best practices](https://global.alipay.com/docs/ac/autodebit_en/best_practice) for more details. |
| normalUrl | Pull up the mobile browser, and some payment methods will redirect to the app checkout page, and some payment methods will directly make H5 payments. |
| schemeUrl | If the buyer installs the payment method app, directly pull up the app checkout page. If the buyer does not have the payment method app installed, return the error. |


The following figure shows the page effect after completing this step:








![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")



RMO.33WILLBEDEDUCTEDFROMYOURBOOST

0%COMBEDCOTTONFORAPRER

DCZ5SU65IANWKBO2CXMUIAL6

CHECKOUT

RM0.33

AYMENTMETHODS

DCZ5SU65JANWKRG2CXWUJAL6

TEST.ACQ.O1

CLASSICBLACKCOTTONT-SHIRT

XCWMDJKFZ2J7AB4T

CONFRMPDYMENT

CONFRMPAYMENT

白BALANCE:RM542

WALLETACCOUNT

CREDITCARD&DEBITCA

XCWMDJKFZ2J7AB4T

HAUTHENTICATE

O221OO5OVCHBMFXL3N

RM0.33

BALANCE:RM542

FORGOTPIN?

OTALTOPAY:

RDERCONFIRMATION

EXTRA-SOFTFEEL

RM0.33

TESTACO\_O1

RDERREVIEW

RM0.33

TESTACO\_O1

SHIPPING

DBYALIPAY-

20221O05OVCHBMFXL3MGXT

RM0.33

UBTOTAL:

RM0.33

15:01

15:01

O

15:01

PAY

L令

RM0.00

L令

ALIPAY

BOOST

$二

DCZ5SU65IANWKRA2CXWUIA

FOR

TOTAL:

O

一

X


RMO.33WILLBEDEDUCTEDFROMYOURBOOST

0%COMBEDCOTTONFORAPRER

DCZ5SU65IANWKBO2CXMUIAL6

CHECKOUT

RM0.33

AYMENTMETHODS

DCZ5SU65JANWKRG2CXWUJAL6

TEST.ACQ.O1

CLASSICBLACKCOTTONT-SHIRT

XCWMDJKFZ2J7AB4T

CONFRMPDYMENT

CONFRMPAYMENT

白BALANCE:RM542

WALLETACCOUNT

CREDITCARD&DEBITCA

XCWMDJKFZ2J7AB4T

HAUTHENTICATE

O221OO5OVCHBMFXL3N

RM0.33

BALANCE:RM542

FORGOTPIN?

OTALTOPAY:

RDERCONFIRMATION

EXTRA-SOFTFEEL

RM0.33

TESTACO\_O1

RDERREVIEW

RM0.33

TESTACO\_O1

SHIPPING

DBYALIPAY-

20221O05OVCHBMFXL3MGXT

RM0.33

UBTOTAL:

RM0.33

15:01

15:01

O

15:01

PAY

L令

RM0.00

L令

ALIPAY

BOOST

$二

DCZ5SU65IANWKRA2CXWUIA

FOR

TOTAL:

O

一

X

#### FAQs

##### How to handle different payment experiences？

You do not need to deal with the different experiences corresponding to different payment methods. It only needs to redirect to the *normalUrl* through the front-end page. Different payment experiences are promoted by *normalUrl* to complete the rendering and payment process.

### Display the payment results page Client-side

You need to provide an HTTPS address and specify it through the *paymentRedirectUrl* field of the **pay** API, which is used to display the payment results on the merchant side.

![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")

#### FAQs

##### What does the payment results page show?

In the case of successful payment or failed payment, it can redirect to the result page from the payment method side.

##### Does redirecting to the results page mean the payment was successful?

The result page cannot be used as the basis for judging whether the payment is successful: 

* After the buyer makes a successful payment, the buyer may not be redirected to the result page due to network or other reasons.
* If the buyer has not completed the payment, it still has an entrance that can be redirected to the result page.
* Antom does not support specifying information that represents the payment result in the *paymentRedirectUrl* field.

Step 3: Obtain the payment resultsClient-side
---------------------------------------------

When the buyer completes the payment or the payment times out, you can get the corresponding payment result from the Antom asynchronous notification or by inquiring the payment result actively.

### **Receive the asynchronous notification**

When a payment is completed or fails, Antom sends an asynchronous notification ([**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online)) to the address that you specified in the **pay** API via the *paymentNotifyUrl* parameter. If the address of each payment is the same, you can also configure the address in Antom Dashboard.

The following is the notification request sample code:

copy
```
{
  "notifyType": "PAYMENT_RESULT",
  "result": {
    "resultCode": "SUCCESS",
    "resultStatus": "S",
    "resultMessage": "success"
  },
  "paymentRequestId": "paymentRequestId01",
  "paymentId": "2020010123456789XXXX",
  "paymentAmount": {
    "value": "100",
    "currency": "HKD"
  },
  "paymentCreateTime": "2020-01-01T12:01:00+08:30",
  "paymentTime": "2020-01-01T12:01:01+08:30"
}
```
The following is the code that verifies and returns the notification:

copy
```
@RequestMapping(path = "/payResult", method = RequestMethod.POST)
public ResponseEntity<AlipayResponse> paymentNotifyProcessor(HttpServletRequest request,
                                                             @RequestBody String body) {

    // retrieve the required parameters from the request header.
    String requestTime = request.getHeader("request-time");
    String clientId = request.getHeader("client-id");
    String rawSignature = request.getHeader("signature");
    String signature = "";

    // get valid part from raw signature
    if(rawSignature==null||rawSignature.isEmpty()){
        throw new RuntimeException("empty notify signature");
    }else {
        String[] parts = rawSignature.split("signature=");
        if (parts.length > 1) {
            signature = parts[1];
        }
    }

    // verify payment result notify's signature
    boolean verifyResult = SignatureTool.verify(request.getMethod(), request.getRequestURI(),
            clientId, requestTime, body, signature,
            ALIPAY_PUBLIC_KEY);
    if (!verifyResult) {
        throw new RuntimeException("Invalid notify signature");
    }

    // update the record status with notify result

    // respond the server that we accept the notify
    Result result = new Result("SUCCESS", "success", ResultStatusType.S);
    AlipayResponse response = new AlipayResponse();
    response.setResult(result);
    return ResponseEntity.ok().body(response);
}
```
The following is the notification response sample code:

copy
```
{
  "result": {
    "resultCode": "SUCCESS",
    "resultStatus": "S",
    "resultMessage": "Success"
  }
}
```
#### FAQs

##### When will the notification be sent?

After the payment is completed, Antom will send the asynchronous notification to you in 3~5s. If the payment is not completed, you need to wait for Antom to close the order before sending the asynchronous notification. The time to close the order is different for different payment methods, generally the default is 14 minutes.

##### Will the asynchronous notification be re-sent?

If you receive an asynchronous notification from Antom, you are required to return the response in the [Sample code](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) format. If you do not respond to the asynchronous notification as required, or the asynchronous notification is not delivered due to network reasons, the notification will be automatically resent within 24 hours. The notification can be resent up to 8 times or until a correct response is received to terminate delivery. The sending intervals are as follows: 0 minutes, 2 minutes, 10 minutes, 10 minutes, 1 hour, 2 hours, 6 hours, and 15 hours.

##### Do I need to countersign the response?

If you receive an asynchronous notification from Antom, you are required to return the response in the [Sample code](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) format, but you do not need to countersign the response.

##### How do I understand the meaning of the following key fields?

* *result*: Indicates the payment result of the order.
* *paymentRequestId*: Indicates the payment request number you generated for consult, cancel, and reconciliation.
* *paymentId*: Indicates the payment order number generated by Antom, used for refund and reconciliation.
* *paymentAmout*: Indicates the payment amount.

### Inquire about the payment result

Initiating a query request will involve the following parameters.



| **Parameter name** | **is required?** | **Description** |
| --- | --- | --- |
| paymentRequestId | No | The payment request number generated by the merchant |

The following is the sample code:

copy
```
  AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG,
          merchantPrivateKey, alipayPublicKey);

  AlipayPayQueryRequest alipayPayQueryRequest = new AlipayPayQueryRequest();
  alipayPayQueryRequest.setClientId(CLIENT_ID);
  alipayPayQueryRequest.setPath("/ams/sandbox/api/v1/payments/inquiryPayment");
  alipayPayQueryRequest.setPaymentRequestId("paymentRequestId01");

  AlipayPayQueryResponse alipayPayQueryResponse;
  try {
      alipayPayQueryResponse = defaultAlipayClient.execute(alipayPayQueryRequest);
  } catch (AlipayApiException e) {
      String errorMsg = e.getMessage();
      // handle error condition
  }
```
**Obtain the response code**

copy
```
{
  "result": {
    "resultCode": "SUCCESS",
    "resultStatus": "S",
    "resultMessage": "Success"
  },
  "paymentStatus": "SUCCESS",
  "paymentRequestId": "paymentRequestId01",
  "paymentId": "2019060811401080010018882020035XXXX",
  "paymentAmount": {
    "value": "100",
    "currency": "HKD"
  },
  "paymentCreateTime": "2019-06-01T12:01:01+08:30",
  "paymentTime": "2019-06-01T12:01:01+08:30",
  "transactions": null
}
```
#### FAQs

##### How do I understand the meaning of the following key fields?

* *result*: the result of the API call. It only indicates the result of the **inquiryPayment** API call. The order result should be determined based on the *paymentStatus*. `SUCCESS` and `FAIL` indicate final results, while `PROCESSING` indicates that the transaction is still in progress.
* *paymentAmount*: amount verification. If there is a need for amount verification, this field can be used.

##### How frequently should I initiate the query?

It is recommended to initiate a round-robin query at an interval of 2 seconds until either the final payment result is retrieved or an asynchronous payment notification is received.

Best practice
=============

Follow these best practices to improve integration efficiency.

Customize the payment timeout
-----------------------------

In the checkout payment scenario, the default timeout on the Antom side is 14 mins, and after the payment timeout, the buyer can't continue to pay. To define the timeout time, you can specify through the *paymentExpireTime* parameter of the **pay** API. After exceeding the specified time, the buyer can not scan the code or log in to the checkout page.

The following sample code shows how to specify the *paymentExpireTime* parameter in the **pay** API:

WebWAPApp### Web sample code


copy
```
{
  "env": {
    "terminalType": "WEB"
  },
  "order": {
    "orderAmount": {
      "currency": "CNY",
      "value": "1314"
    },
    "orderDescription": "Cappuccino #grande (Mika's coffee shop)",
    "referenceOrderId": "ORDER_0517884936248XXXX"
  },
  "paymentAmount": {
    "currency": "CNY",
    "value": "1314"
  },
  "paymentMethod": {
    "paymentMethodType": "ALIPAY_CN"
  },
  "paymentExpiryTime":"2024-01-20T08:51:06+08:00",
  "paymentNotifyUrl": "https://www.gaga.com/notify",
  "paymentRedirectUrl": "imeituan://",
  "paymentRequestId": "iJ9lsVgTx8pX7qJpvW6rfqEE2Kdv9M3lgL8e1999ydfz52uMSqwvT3qXYw8IFBYt",
  "productCode": "CASHIER_PAYMENT",
  "settlementStrategy": {
    "settlementCurrency": "USD"
  }
}
```

### WAP sample code


copy
```
{
  "env": {
    "osType": "ANDROID",
    "terminalType": "WAP"
  },
  "order": {
    "orderAmount": {
      "currency": "CNY",
      "value": "1314"
    },
    "orderDescription": "Cappuccino #grande (Mika's coffee shop)",
    "referenceOrderId": "ORDER_0517884936248XXXX"
  },
  "paymentAmount": {
    "currency": "CNY",
    "value": "1314"
  },
  "paymentMethod": {
    "paymentMethodType": "ALIPAY_CN"
  },
  "paymentExpiryTime":"2024-01-20T08:51:06+08:00",
  "paymentNotifyUrl": "https://www.gaga.com/notify",
  "paymentRedirectUrl": "imeituan://",
  "paymentRequestId": "iJ9lsVgTx8pX7qJpvW6rfqEE2Kdv9M3lgL8e1999ydfz52uMSqwvT3qXYw8IFBYt",
  "productCode": "CASHIER_PAYMENT",
  "settlementStrategy": {
    "settlementCurrency": "USD"
  }
}
```

### App sample code


copy
```
{
  "env": {
    "osType": "ANDROID",
    "terminalType": "APP"
  },
  "order": {
    "orderAmount": {
      "currency": "CNY",
      "value": "1314"
    },
    "orderDescription": "Cappuccino #grande (Mika's coffee shop)",
    "referenceOrderId": "ORDER_0517884936248XXXX"
  },
  "paymentAmount": {
    "currency": "CNY",
    "value": "1314"
  },
  "paymentMethod": {
    "paymentMethodType": "ALIPAY_CN"
  },
  "paymentExpiryTime":"2024-01-20T08:51:06+08:00",
  "paymentNotifyUrl": "https://www.gaga.com/notify",
  "paymentRedirectUrl": "imeituan://",
  "paymentRequestId": "iJ9lsVgTx8pX7qJpvW6rfqEE2Kdv9M3lgL8e1999ydfz52uMSqwvT3qXYw8IFBYt",
  "productCode": "CASHIER_PAYMENT",
  "settlementStrategy": {
    "settlementCurrency": "USD"
  }
}
```

If you specify *paymentExpireTime*, the valid time that the buyer can pay becomes the time in *paymentExpireTime*.

If the buyer pays after this time, there are two types of experience:

* The buyer is unable to complete the payment
* The buyer receives a refund immediately after making the payment

Obtain the payment continuation URL
-----------------------------------

Antom side is directly connected to many payment methods. There is a part of the payment method order interface time-consuming situation, which may lead to your failure to get the response. The buyer can not redirect to the payment continuation URL, affecting the success rate of payment and user experience.

It is recommended to set the interface timeout to 10s to ensure the success rate of getting the response. For the case of calling pay timeout, it is recommended to launch the original request to retry and get the payment continuation URL again.

Optimize the payment experience Only for Web
--------------------------------------------

Some payment methods support buyers to pay by scanning the code or password on PC, and you can target such payment methods without redirection. When the buyer selects this payment method, the code value in the API response will be rendered directly on the merchant's page for displaying the QR code or password, which reduces the page redirect and improves the experience.

The QR code returned by Antom will not be refreshed automatically. When displaying the QR code, add *expireTime* in the API response to display the timeout time. When displaying the passphrase, the copy function of the passphrase is realized, which makes it easy for buyers to paste the payment into the payment method app.

Redirect to the merchant result page
------------------------------------

1. Not all payment methods pull up the app can redirect to your specified address, some payment methods are not supported, such as Kakaopay (KakaoTalk).
2. If the buyer has installed more than one browser. Then when redirecting to the https result page address after payment completion, it will only redirect to the default browser, but the scheme address is not affected.

Suggestions on processing logic for merchant results pages
----------------------------------------------------------

1. **Client redirection abnormality**

If the buyer pays successfully, the buyer may not be able to redirect to the *paymentRedirectUrl* that you specified due to network reasons or the limitations of the payment method itself, and the following two points should be noted in this case:

+ You cannot use the client redirection as the basis for determining the success of the payment.
+ If the *paymentRedirectUrl* of the payment method page fails to redirect to the merchant page, the buyer may manually click the original merchant page. Therefore, in order to avoid the original merchant page manually cutting back to the payment page, leading the buyer to initiate payment of the order again, it is recommended to add a pop-up window for querying the transaction results after redirecting on the original merchant's order page, when the buyer clicks on the pop-up window to display the result of the order, avoiding the payment of the order again.
2. **Trigger order result query after redirection**

If the merchant side is pulled up after triggering a call to the **inquiryPayment** API, then the following different results are suggested:

+ **Successful payment**: the page will display the content related to the shipment after successful payment;
+ **Payment Failure**: the page displays the payment failure, and it is recommended to guide the re-payment;
+ **Payment processing**: the page displays the landing effect, waits for 3-5s, and at the same time, queries the server-side payment results, if it still does not return successful or failed final results, it is recommended to display the "order processing" or "order management portal to view the final results"; it is not recommended to display the "network processing". If there is still no result, we suggest displaying "order processing" or going to "order management portal for final result".

Payment failed retry
--------------------

For the same order on the merchant side, if the first payment is not completed and the buyer is supported to initiate the payment again, then it is recommended that you follow the integration steps below:

1. In the payment request, set the *referenceOrderId* to the order ID and the *paymentRequestId* to the payment order ID.
2. When the same order initiates payment again, the order status will be prioritized, and if the payment is successful, the buyer will be shown the "completed payment", and if the payment is not successful, the **pay** API will be called again to get a new *normalUrl* to redirect. Note that since it is the same order, the *referenceOrderId* can be kept unchanged, while the corresponding new payment order needs to update the *paymentRequestId*.
3. The merchant side needs to check that there is only one successful payment order for a merchant order, if there is more than one successful payment order, then it needs to call the **cancel** API to refund the buyer.
4. For payment methods that do not support refunds, it is recommended to cancel the first payment order before initiating a new payment.

Obtain payment results
----------------------

In order to guarantee the stable acquisition of payment results and avoid the situation where the buyer's payment is completed but you do not get the payment result. It is recommended that you check the payment results at the following stages:

1. When the merchant payment result page is displayed.
2. Before shipping to the buyer.
3. When you receive the Antom reconciliation file.

Open payment method URL Only for App
------------------------------------



| **Payment method features** | **Link type** | **Solution** | **Advantages and disadvantages** |
| --- | --- | --- | --- |
| Only the app checkout is supported | applinkUrl | Redirect to payment method app checkout:iOS calls the *openUrl* method, and Android calls the *startActivity* method. | Advantages:1. Complete the payment in the payment methods app. 2. No need to deal with the exception that the buyer does not have the payment method app installed. |
| normalUrl | Redirect to payment method app checkout:iOS calls the *openUrl* method, and Android calls the *startActivity* method. | Advantages:1. Complete the payment in the payment methods app. 2. No need to deal with the exception that the buyer does not have the payment method app installed.  Disadvantage:1. During the payment process, the browser will be pulled up and then redirected to the payment method app. |
| schemeUrl | Redirect to payment method app checkout:iOS calls the *openUrl* method, and Android calls the *startActivity* method. | Advantage:1. Complete the payment in the payment methods app.  Disadvantage:1. Handle the exception that the buyer does not install the payment method app. |
| Only the H5 checkout is supported | normalUrl | Open the checkout URL in webview. | Advantage:1. The ordering, payment, and delivery processes are all completed within the merchant's app. |
| Support both app and H5 checkout | applinkUrl | iOS calls the *openUrl* method, and Android calls the *startActivity* method. | Advantages:1. Complete the payment in the payment methods app. 2. No need to deal with the exception that the buyer does not have the payment method app installed.  Disadvantage:1. If the buyer does not install the payment method app, it will be downgraded to the H5 checkout, and the payment process will be completed in the system browser. |
| normalUrl | Open the checkout URL in webview. | Advantage:1. The ordering, payment, and delivery processes are all completed within the merchant's app.  Disadvantage:1. Unable to use app checkout, poor payment experience. |
| schemeUrl | iOS calls the *openUrl* method, and Android calls the *startActivity* method. | Advantage:1. Complete the payment in the payment methods app.  Disadvantages:1. Handle the exception that the buyer does not install the payment method app. 2. The H5 checkout cannot be used, and the transaction cannot be restored if the app is not installed. |

### FAQs

#### What to do when encountering a disambiguation box in Android?

Refer to [Google documentation](https://developer.android.com/training/package-visibility/use-cases?hl=zh-cn#avoid-a-disambiguation-dialog) for more information.

#### How to use WebView to load the order page?

To provide an excellent user experience, you can use the WebView to load the order page in the client. After clicking the order, you can directly redirect to the mobile application that supports the payment method to complete the payment, you can refer to the JavaScript code binding to the mobile client code to realize this interactive experience.

* Android: <https://developer.android.com/develop/ui/views/layout/webapps/webview?hl=zh-cn#BindingJavaScript>
* iOS: <https://developer.apple.com/documentation/javascriptcore/jsexport?language=objc>
![](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership) 


#### On this page

[User experience](#Ksw2W "User experience")[Payment flow](#N7q25 "Payment flow")[Integration steps](#nbBeY "Integration steps")[Step 1: (Optional) Add a list of payment methods](#VTOFD "Step 1: (Optional) Add a list of payment methods")[Step 2: Invoke the pay API and get the payment continuation URL](#dUZwg "Step 2: Invoke the pay API and get the payment continuation URL")[Initiate a payment request](#vPvsX "Initiate a payment request")[Install an API library](#6hGTH "Install an API library")[Initialize the request instance](#ft0LA "Initialize the request instance")[Create a payment request](#BGvIj "Create a payment request")[Receive a payment response](#QhTNS "Receive a payment response")[FAQs](#v5Jyj "FAQs")[Redirect to the Checkout page of the payment method](#62lB0 "Redirect to the Checkout page of the payment method")[FAQs](#cXZYo "FAQs")[Display the payment results page](#x1EYF "Display the payment results page")[FAQs](#WblBX "FAQs")[Step 3: Obtain the payment results](#7FBHl "Step 3: Obtain the payment results")[Receive the asynchronous notification](#PMBUH "Receive the asynchronous notification")[FAQs](#nmLpr "FAQs")[Inquire about the payment result](#O1jRy "Inquire about the payment result")[FAQs](#tkpZO "FAQs")[Best practice](#6620B "Best practice")[Customize the payment timeout](#f5gU1 "Customize the payment timeout")[Obtain the payment continuation URL](#CRUkl "Obtain the payment continuation URL")[Optimize the payment experience](#luUxS "Optimize the payment experience")[Redirect to the merchant result page](#qDjwR "Redirect to the merchant result page")[Suggestions on processing logic for merchant results pages](#GdEle "Suggestions on processing logic for merchant results pages")[Payment failed retry](#hAeaV "Payment failed retry")[Obtain payment results](#o55cG "Obtain payment results")[Open payment method URL](#jyh8F "Open payment method URL")[FAQs](#QamNx "FAQs")[What to do when encountering a disambiguation box in Android?](#XTN3K "What to do when encountering a disambiguation box in Android?")[How to use WebView to load the order page?](#2IeMu "How to use WebView to load the order page?")







