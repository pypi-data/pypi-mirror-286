Android | Checkout Payment | Alipay Docs
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fcashierpay%2Fcard_android)

[Go to Homepage](../../)

Checkout Payment

[Overview](/docs/ac/cashierpay/overview)

Accept payments

After payments

Payment methods

Other resources

Advanced features

[Pre-front solutionAPI](/docs/ac/cashierpay/prefront)

[Buy now pay laterAPI](/docs/ac/cashierpay/bnpl)

[Card vaultingAPI](/docs/ac/cashierpay/cv)

[Card vaultingSDK](/docs/ac/cashierpay/cvsdk)

[Card payment featuresAPISDK](/docs/ac/cashierpay/mf)

Android
=======

In this topic, you'll learn how to integrate the card payment SDK into an Android client so that you can render cashier pages in a mobile application.

Prerequisites

Before integrating the card payment SDK, familiarize yourself with the [_Integration guide_](https://global.alipay.com/docs/integration) and [_Overview_](https://global.alipay.com/docs/ac/ams/api_fund). This will enable you to understand the steps for integrating server APIs and notes for calling the APIs. Also, ensure that you have completed the following tasks:

*   Obtain a client ID in Antom Dashboard.
*   Properly configure keys in Antom Dashboard .
*   Install the latest version of Android Studio.
*   Target at least Android 4.4 (API level 19) or higher.
*   Use Gradle 4.1 or earlier.
*   Configure a physical machine or simulator to run your application.

Key integration steps

Integrate the card payment SDK by following these steps:

1

Integrate the SDK package

Client side

To integrate the SDK package, please refer to [Integrate the SDK Package](https://global.alipay.com/docs/ac/antom_sdk/android_en).

2

Create an SDK instance by using the `AMSCashierPayment` method:

Client side

Follow these steps to create an SDK instance:

1.  Create a _configuration_ object: A required object. The object must contain all of the following configuration parameters:
    *   _setLocale_: An optional string, which is used by the merchant client to identify the language of the buyer's browser. Specify this parameter to ensure that the SDK displays pages in the correct language. The valid values are as follows. If any other values are passed, English will be used as the default language.
        *   `locale("es", "ES")`: Spanish
            
        *   `locale("ko", "KR")`: Korean
            
        *   `locale("pt", "BR")`: Portuguese
            
        *   `locale("en", "US")`: English
            
    *   _setOption_: Optional. It is used to specify whether to use the default loading pattern and the sandbox environment. Valid values are:
        *   `"sandbox", "true"`: Sandbox environment
        *   `"sandbox", "false"`: Production environment
        *   `"showLoading", "true"`: Use the default loading pattern.
        *   `"showLoading", "false"`: Do not use the default loading pattern.
2.  Create an instance of the **OnCheckoutListener** API, which is used for event handling in the subsequent process. The API includes the following method:
    *   `onEventCallback`: Required. A callback function that monitors payment events on the checkout page, returning _eventCode_ and _eventResult_.
3.  Set the instance of the **OnCheckoutListener** API in that of the _configuration_ object to execute event callbacks.
4.  Instantiate the `AMSCashierPayment` method.

Create an SDK instance:

Java

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

// Create the

    AMSCashierPaymentConfigurat

    ion type.

AMSCashierPaymentConfiguration

    configuration \= new

    AMSCashierPaymentConfigurat

    ion();

configuration.setLocale(new

    Locale("en", "US"));

// Specify showLoading as true

    (default value) to use the

    default loading pattern.

    Specify it as false to

    customize the loading

    animation based on

    onEventCallback.

configuration.setOption

    ("showLoading", "true");

// Set the sandbox environment.

    If you leave it empty, the

    production environment is

    used by default.

configuration.setOption

    ("sandbox", "true");

// Set the callback to monitor

    payment events on the

    checkout page.

configuration

    .setOnCheckoutListener(new

    OnCheckoutListener() {

@Override

public void onEventCallback

        (String eventCode,

        AMSEventResult

        eventResult) {

public void onEventCallback

        (String eventCode,

        AMSEventResult

        eventResult) {

Log.e(TAG,

            "onEventCallback

            eventCode=" +

            eventCode + "

            eventResult=" +

            eventResult

            .toString());

}

});

// Instantiate

    AMSCashierPayment

AMSCashierPayment checkout \=

    new AMSCashierPayment

    .Builder(activity,

    configuration).build();

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

3

Send a **createPaymentSession (Checkout Payment)** request to the Alipay server.

Client side

After the buyer selects a card payment method for payment, your client starts monitoring the payment button click event. When your client detects that the payment button is clicked, your server needs to send a **[createpaymentSession (Checkout Payment)](http://global.alipay.com/docs/ac/ams/session_cashier)** request to the Alipay server. After you receive the response from the API call, use the value of the _paymentSessionData_ parameter to complete Step 4.

**Note**: In your **createPaymentSession (Checkout Payment)** request, specify _paymentRedirectUrl_ as the URL Scheme that you provide to redirect buyers to the payment result page upon payment completion.

The following sample for calling the createPaymentSession API includes mandatory parameters and several optional parameters.

JSON

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

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

{

"order": {

"buyer": {

"buyerName": {

"firstName": "\*\*\*\*\*",

"fullName": "D\*\*\*u",

"lastName": "Liu",

"middleName": "Skr"

},

"buyerRegistrationTime":

          "2022-01-01T09:30:00

          +08:00",

"referenceBuyerId": "tony

          .c"

},

"goods": \[{

"goodsBrand": "AMSDM",

"goodsCategory": "card

          /ssr/adc",

"goodsName": "Goods No.1"

          ,

"goodsQuantity": "1",

"goodsSkuName": "SKU1",

"goodsUnitAmount": {

"currency": "USD",

"value": "10000"

},

"goodsUrl": "HangZhou

          LeiFenTa",

"referenceGoodsId":

          "amsdm\_good\_tony\_c\_20

          230227\_095825\_922"

}\],

"orderAmount": {

"currency": "BRL",

"value": "2129"

},

"orderDescription":

        "AMSDM\_GIFT",

"referenceOrderId":

        "amsdmorder\_tony\_c\_2023

        0227\_095825\_921"

},

"paymentAmount": {

"currency": "BRL",

"value": "2129"

},

"paymentFactor": {

"isAuthorization": true

},

"paymentMethod": {

"paymentMethodType": "CARD"

        ,

"paymentMethodMetaData":{

"paymentMethodRegion"

            :"BR"

}

},

"paymentNotifyUrl": "https

      ://www.google.com.sg",

"paymentRedirectUrl": "https

      ://www.baidu.com",

"paymentRequestId":

      "amsdmpayk\_tony\_c\_2023022

      7\_095825\_920\_532",

"productCode":

      "CASHIER\_PAYMENT",

"settlementStrategy": {

"settlementCurrency": "USD"

},

"enableInstallmentCollection"

      :"true"

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

The response sample of the API call is shown as follows:

JSON

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

{

"paymentSessionData":

      "UNvjVWnWPXJA4BgW

      +vfjsQj7PbOraafHY19X

      +6EqMz6Kvvmsdk

      +akdLvoShW5avHX8e8J15P8uN

      VEf/PcCMyXg==&&SG&&111",

"paymentSessionExpiryTime":

      "2023-04-06T03:28:49Z",

"paymentSessionId":

      "UNvjVWnWPXJA4BgW

      +vfjsQj7PbOraafHY19X

      +6EqMz6Ikyj9FPVUOpv

      +DjiIZqMe",

"result": {

"resultCode": "SUCCESS",

"resultMessage": "success."

        ,

"resultStatus": "S"

}

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

4

Create a component for collecting payment factors by using the `createComponent` method in the instantiated object

Client side

Call the `createComponent()` method and pass in the following parameters:

*   _activity_: A required object belonging to the _Activity_ type. It is used to include the information about context parameters on the current page.
*   _sessionData_: A required string. Pass the complete data in the _paymentSessionData_ parameter obtained in the response through the **createpaymentSession (Cashier Payment)** API to the _sessionData_ parameter.

Call the `onDestroy()` method to free SDK component resources in the following situations:

*   When the user exits the checkout page, free the component resources created in the **createPaymentSession**.
*   When the user initiates multiple payments, free the component resources created in the previous **createPaymentSession**.

Create a configuration object:

Java

1

2

3

checkout.createComponent

    (activity,sessionData);

//Free SDK component resources

checkout.onDestroy();

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Reference

Event codes

The SDK provides the following status codes:

*   `SDK_START_OF_LOADING`: The loading animation starts to play during the payment component creation.
    
*   `SDK_END_OF_LOADING`: The loading animation ends during the payment component creation.
    

The SDK provides the following error codes:

*   `SDK_INTERNAL_ERROR`: The internal error of the SDK occurs. Contact Alipay Technical Support to resolve the issue.
    
*   `SDK_CREATEPAYMENT_PARAMETER_ERROR`: The parameters passed into the `createComponent` method are incorrect. Ensure the parameters are passed correctly and send a new request.
    
*   `SDK_CALL_URL_ERROR`: Represents one of the following cases:
    
    *   The redirection to the merchant page failed to be executed.
    *   The parameter _paymentRedirectUrl_ in your **createpaymentSession (Cashier Payment)** request is not passed or passed incorrectly.
*   `SDK_INTEGRATION_ERROR`: Dependencies are not found. Ensure that the dependencies are added correctly and retry the integration process.
    

Code sample in key steps

The following code sample shows the key steps during integration. The sample does not include the code used for calling the **createpaymentSession (Cashier Payment)** API.

Java

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

// The development tool is

    automatically imported.

import com.alipay.ams.component

    .sdk.callback

    .OnCheckoutListener;

import com.alipay.ams.component

    .sdk.payment

    .AMSCashierPayment;

import com.alipay.ams.component

    .sdk.payment

    .AMSCashierPaymentConfigura

    tion;

// Step 1: Create the

    AMSCashierPaymentConfigurat

    ion type.

AMSCashierPaymentConfiguration

    configuration \= new

    AMSCashierPaymentConfigurat

    ion();

configuration.setLocale(new

    Locale("en", "US"));

// Set the sandbox environment.

    If you leave it empty, the

    production environment is

    used by default.

configuration.setOption

    ("sandbox", "true");

// Set the callback to monitor

    payment events on the

    checkout page.

configuration

    .setOnCheckoutListener(new

    OnCheckoutListener() {

@Override

public void onEventCallback

        (String eventCode,

        String message) {

Log.e(TAG,

            "onEventCallback

            eventCode=" +

            eventCode + "

            eventResult=" +

            eventResult

            .toString());

}

});

// Instantiate

    AMSCashierPayment.

AMSCashierPayment checkout \=

    new AMSCashierPayment

    .Builder(activity,

    configuration).build();

// Submit the payment

public void handleSubmit(View

    view) {

// Step 2: Call the

        createPaymentSession

        API to obtain

        paymentSessionData.

String paymentSessionData \=

        requestSessionData();

// Step 3: Create and

        render the card

        component

// Best practice

checkout.createComponent

        (activity,

        paymentSessionData);

}

הההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#### Is this page helpful?

To view the latest updates to the documentation, visit [Release notes](https://global.alipay.com/docs/releasenotes).

![Image 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)