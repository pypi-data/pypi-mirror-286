Card payments (Android) | Checkout Payment | Alipay Docs
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fcashierpay%2Fadcard)

[Go to Homepage](../../)

Checkout Payment

[Overview](/docs/ac/cashierpay/overview)

Accept payments

SDK integration

[APM payments (Web/WAP)APM](/docs/ac/cashierpay/apm_ww)

[APM payments (Android)APM](/docs/ac/cashierpay/apm_android)

[APM payments (iOS)APM](/docs/ac/cashierpay/apm_ios)

[Card payments (Web/WAP)Card](/docs/ac/cashierpay/wwcard)

[Card payments (Android)Card](/docs/ac/cashierpay/adcard)

[Card payments (iOS)Card](/docs/ac/cashierpay/ioscard)

API-only integration

After payments

Payment methods

Other resources

Advanced features

[Pre-front solutionAPI](/docs/ac/cashierpay/prefront)

[Buy now pay laterAPI](/docs/ac/cashierpay/bnpl)

[Card vaultingAPI](/docs/ac/cashierpay/cv)

[Card vaultingSDK](/docs/ac/cashierpay/cvsdk)

[Card payment featuresAPISDK](/docs/ac/cashierpay/mf?pageVersion=7)

Card payments (Android)
=======================

2024-05-11 10:13

Antom SDK is a pre-built UI component designed to collect card information and manage 3D authentication processes for you. Integration of this component does not require you have a PCI qualification, making it ideal for those who prefer to entrust Antom to collect card information.

User experience
===============

The following figures show the user journey of paying on an app:

![Image 3: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1711338358204-54fb815f-6754-404f-a95a-6407e14573ce.png)

Payment flow
============

For each payment method, the payment flow is composed of the following steps:

![Image 4: 111卡.webp](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1713521451605-d3ce7ff5-694a-441c-8724-2b82d2a8f2df.webp)

1.  **The use****r lands on the checkout page.**

1.  **Create the** [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) **request**  
    After the buyer selects a payment method and submits the order, you can obtain the payment session by calling the [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) interface.
2.  **Invoke the client SDK**  
    On the client side, invoke the SDK through the payment session. The SDK will handle information collection, redirection, app invocation, QR code display, verification, and other processes based on the payment method's characteristics.
3.  **Get the payment result**  
    Obtain the payment result by using one of the following two methods:

1.  Asynchronous Notification: Specify the _paymentNotifyUrl_ in the [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) interface to set the address for receiving asynchronous notifications. When the payment is successful or expires, Antom will use [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) to send asynchronous notifications to you.
2.  Synchronous Inquiry: Call the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) interface to check the payment status.

5.  **Get the capture result**  
    For card payments, you need to obtain the capture result by using one of the following two methods:

1.  Asynchronous Notification: Specify the _paymentNotifyUrl_ in the [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) interface to set the address for receiving asynchronous notifications. When the payment request is successful or expires, Antom will use [**notifyCapture**](https://global.alipay.com/docs/ac/ams/notify_capture) to send asynchronous notifications to you.
2.  Synchronous Inquiry: Call the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) interface to check the payment request status.

Integration steps
=================

Start your integration by taking the following steps:

1.  Create a payment session
2.  Create and invoke the SDK
3.  Obtain payment result
4.  Obtain capture result

Step 1: Create a payment session Server-side
--------------------------------------------

When a buyer selects a payment method provided by Antom, you need to collect key information such as the payment request ID, order amount, payment method, order description, payment redirect URL, and payment result notification URL, call the **createPaymentSession** API to create a payment session, and return the payment session to the client.

Antom provides server-side API libraries for multiple languages. The following codes use Java as an example. You need to install Java 6 or higher.

### Install an API library

You can find the latest version on [GitHub](https://github.com/alipay/global-open-sdk-java).

copy

    <dependency>
    <groupId>com.alipay.global.sdk</groupId>
    <artifactId>global-open-sdk-java</artifactId>
    <version>2.0.21</version>
    </dependency>

### Initialize request instance

Create a singleton resource to make a request to Antom.

copy

    import com.alipay.global.api.AlipayClient;
    import com.alipay.global.api.DefaultAlipayClient;
    
    String merchantPrivateKey = "YOUR PRIVATE KEY";
    String alipayPublicKey = "ALIPAY PUBLIC KEY"
    AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG,
                                                               merchantPrivateKey, alipayPublicKey);

### Create a payment session

Creating a payment session involves the following parameters:

<table style="width:748px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="211" span="1"><col width="97" span="1"><col width="440" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0388ea856bbe02afe63d190348731e7f" id="u6f40ff96" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Parameter name</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="72343843194873f8d541ae3e10240daa" id="u763f47eb" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Required</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="5d543d063dd4279418160659598feaf4" id="u49778224" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Description</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="e3b409cda7c24ce13c2060c1e332959e" id="u8c2bae99" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>productCode</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="2499e7854cc2964a3514d63af8ba9fc2" id="u71fa19c6" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span><span></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="88630b787799717b20db46df79292347" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">Represents the payment product that is being used, which is stipulated in the contract. For Checkout Payment, the value is fixed as </span><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">CASHIER_PAYMENT</span></code><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="5c728e08228bb7061801f12beaafa87b" id="ucc713e74" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>paymentRequestId</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="92c12d56a2963dd259abc63e05aaebe8" id="u12408bfe" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="c03bf09685e08170fe274ae8d816e9d8" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">The unique ID assigned by </span>the merchant<span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px"> to identify a payment request.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="eea143db1f8edad5a6d7f4efe205ec56" id="uba71bbed" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>paymentAmount</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="b71e8ef182ac57595d95540e7e6a818b" id="u4ebd7ac0" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="fc31a3ba44b9e977f29db200eb3283c8" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">The payment amount that you request to receive in the order currency.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="247d2c7cf69b32f683c62e3cd629078b" id="ue6f8f924" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>paymentMethod</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="63d9480b35c2224aae20473e5c712d55" id="u564356d5" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="e6b7aafe76891befc03f82527ad8653b" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">The payment method that is used to collect the payment by </span>the merchant<span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px"> or acquirer.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="a10d2dbda37097575c15c88793dc1473" id="u01ca8003" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>paymentRedirectUrl</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="e66bf72f74fe3d704ed6874e43a1f543" id="u2b394d26" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="9894a3a9f8b77b71e8c7f7491aab89b6" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">The merchant page URL that the </span>buyer<span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px"> is redirected to after the payment is completed.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="e5620cb62ce78f1133fe518a16198527" id="u8ebfb495" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>order</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="7c23ed868404541dcf103bbe69abc52f" id="u2196daaf" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="af50633d32a767b21a0c5f2f9193737b" id="udf73b1b1" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">The order information, such as buyer, merchant, goods, amount, shipping information, and purchase environment.</span></p></td></tr><tr style="height:33px"><td colspan="1" style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="43e1ab4026d038a37b45ed3c9522a77b" id="u99012931" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span style="color:rgba(0, 0, 0, 0.78)">paymentNotifyUrl</span></em></p></td><td colspan="1" style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="b940a35f4dc05d4f5ec3085cc829d9cd" id="uca918755" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(0, 0, 0, 0.78)"></span></p></td><td colspan="1" style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="eb79ce3d25678384b8bb1580b27f36d4" id="ua3100e6b" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>Payment result notification address, which can be passed in through the interface or set as a fixed value through the portal.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="852a19bfe7209b7a21c85eb4a2ff409a" id="u4fd83c72" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>settlementStrategy</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="65df0474942087d87e3507f5781f1f8c" id="uaa5db6c4" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">The settlement strategy for the payment request.</span></p></td></tr></tbody></table>

The above parameters are the basic parameters for creating a payment session, for full parameters and additional requirements for certain payment methods refer to [**createPaymentSession (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/session_cashier)**.**

#### Sample codes of calling the createPaymentSession API

The following sample code shows how to call the **createPaymentSession** API:

copy

    AlipayPaymentSessionRequest alipayPaymentSessionRequest = new AlipayPaymentSessionRequest();
    alipayPaymentSessionRequest.setClientId(CLIENT_ID);
    alipayPaymentSessionRequest.setPath("/ams/sandbox/api/v1/payments/createPaymentSession");
    alipayPaymentSessionRequest.setProductCode(ProductCodeType.CASHIER_PAYMENT);
    
    
    // replace to your paymentRequestId
    alipayPaymentSessionRequest.setPaymentRequestId("paymentRequestId01");
    
    Amount amount = new Amount();
    amount.setCurrency("SGD");
    amount.setValue("4200");
    
    alipayPaymentSessionRequest.setPaymentAmount(amount);
    
    //set settlement currency
    SettlementStrategy settlementStrategy = new SettlementStrategy();
    settlementStrategy.setSettlementCurrency("SGD");
    alipayPaymentSessionRequest.setSettlementStrategy(settlementStrategy);
    
    // set paymentMethod
    PaymentMethod paymentMethod = new PaymentMethod();
    paymentMethod.setPaymentMethodType("CARD");
    alipayPaymentSessionRequest.setPaymentMethod(paymentMethod);
    
    // set paymentFactor
    PaymentFactor paymentFactor = new PaymentFactor();
    paymentFactor.setAuthorization(true);
    alipayPaymentSessionRequest.setPaymentFactor(paymentFactor);
    
    // set order Info
    Order order = new Order();
    order.setReferenceOrderId("referenceOrderId01");
    order.setOrderDescription("antom sdk test order");
    order.setOrderAmount(amount);
    Buyer buyer = new Buyer();
    buyer.setReferenceBuyerId("yourBuyerId");
    order.setBuyer(buyer);
    order.setOrderAmount(amount);
    alipayPaymentSessionRequest.setOrder(order);
    
    // replace to your notify url
    alipayPaymentSessionRequest.setPaymentNotifyUrl("https://www.yourNotifyUrl");
    
    // replace to your redirect url
    alipayPaymentSessionRequest.setPaymentRedirectUrl("https://www.yourMerchantWeb.com");
    AlipayPaymentSessionResponse alipayPaymentSessionResponse = null;
    
    try {
        alipayPaymentSessionResponse = defaultAlipayClient.execute(alipayPaymentSessionRequest);
    } catch (AlipayApiException e) {
        String errorMsg = e.getMessage();
        // handle error condition
    }
    

The following code shows a sample of the request message:

copy

    {
      "order": {
        "buyer": {
          "referenceBuyerId": "yourBuyerId"
        },
        "orderAmount": {
          "currency": "SGD",
          "value": "4200"
        },
        "orderDescription": "antom sdk test order",
        "referenceOrderId": "referenceOrderId01"
      },
      "paymentAmount": {
        "currency": "SGD",
        "value": "4200"
      },
      "paymentFactor": {
        "isAuthorization": true
      },
      "paymentMethod": {
        "paymentMethodType": "CARD"
      },
      "paymentNotifyUrl": "https://www.yourNotifyUrl",
      "paymentRedirectUrl": "https://www.yourMerchantWeb.com",
      "paymentRequestId": "paymentRequestId01",
      "productCode": "CASHIER_PAYMENT",
      "settlementStrategy": {
        "settlementCurrency": "SGD"
      }
    }

The following code shows a sample of the response, which contains the following parameters:

*   _paymentSessionData_: the payment session to be returned to the frontend
*   _paymentSessionExpiryTime_: the expiration time of the payment session.

copy

    {
      "paymentSessionData": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Kvvmsdk+akdLvoShW5avHX8e8J15P8uNVEf/PcCMyXg==&&SG&&111",
      "paymentSessionExpiryTime": "2023-04-06T03:28:49Z",
      "paymentSessionId": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Ikyj9FPVUOpv+DjiIZqMe",
      "result": {
        "resultCode": "SUCCESS",
        "resultMessage": "success.",
        "resultStatus": "S"
      }
    }

### FAQs

#### Can Chinese characters be used in the request?

Do not use Chinese characters for the fields in the request including _paymentRequestId_, _referenceOrderId_, _orderDescription_, and _goods_ to avoid incompatible payment methods, such as QRIS and Mastercard.

#### How to set the payment result notification address?

Antom will send the payment result through the [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online), which you can specify in the **createPaymentSession** API via the _paymentNotifyUrl_ parameter. If the address of each payment is the same, you can also configure it in the Antom Dashboard. If you have configured the address and set the parameter in the API, Antom will use the address set in the API.

Step 2: Create and invoke the SDK Client-side
---------------------------------------------

The Antom SDK is a component used for handling payment processes. You initiate the SDK by creating a payment session to collect information, switch between apps, and display QR codes based on the payment method specified in **createPaymentSession** API.

After the buyer selects a payment method on the page, you need to create the SDK and initiate it with a payment session.

### Install

Version Requirements: target at least Android 4.4 (API level 19) or higher.

To integrate the SDK package, refer to [Integrate the SDK Package](https://global.alipay.com/docs/ac/antom_sdk/android_en).

### Instantiate the SDK

Create the SDK instance by using the `AMSCashierPayment` and specify basic configurations. Creating a configuration object includes the following methods:

<table style="width:748px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="211" span="1"><col width="97" span="1"><col width="440" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="a8a9bb16099ffd5e3b97b0e19d1c9eed" id="udb8b3360" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Method name</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="35fcf90ed719ef00afb7e15ac781dabb" id="u3a641a1d" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Required</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="619c73c7fdd247bac8518b9fe652b23b" id="ub99badcd" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Description</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="a1612fab6b50f5a943c7d55b2b9a1664" id="uaf3b013a" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">setLocale</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0c62e320935eb59b98e7e7fe8612bd82" id="uc37f05b1" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:#20304C"></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="797fa0222c646cb02f18c0f668e1e90e" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>It is used to pass in language information. Valid values are listed as follows. You can choose the value to pass based on the region of the payment method. If other values are passed, the local language is used by default:</span></p><ul data-lake-id="ccd9fa63a74ad005ad3572aeb0e05095" lake-indent="0" style="list-style-type:disc;padding-left:23px;margin:0px;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word"><li data-lake-id="3dd43c5426d8808fe5904ab133b224a7" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>en_US</span></code><span>: English</span></li><li data-lake-id="d3f1951d6c32de4a4c49f32f32d1c2f8" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>pt_BR</span></code><span>: Portuguese</span></li><li data-lake-id="59b89117bb83bdba03b6825fbff5f4c0" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>ko_KR</span></code><span>: Korean</span></li><li data-lake-id="17c08fbc59ebe147d86fbde8b055c461" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>es_ES</span></code><span>: Spanish</span></li><li data-lake-id="5d1ac34bf5431328ce76b975cf7138fe" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>ms_MY</span></code><span>: Malay</span></li><li data-lake-id="f41b1b796ea32f7da2eacd0e664d05fd" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>in_ID</span></code><span>: Indonesian</span></li><li data-lake-id="4e6d870a9a92fed057ff6f75ed3eba91" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>tl_PH</span></code><span>: Tagalog</span></li><li data-lake-id="9f346c232d12bc06fa42d6153b0d1c2f" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>th_TH</span></code><span>: Thai</span></li><li data-lake-id="67567795a62d6d8978b6709051962e33" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>vi_VN</span></code><span>: Vietnamese</span></li><li data-lake-id="5d3ebbe266405bda289eb04a9adcb86b" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>fr_FR</span></code><span>: French</span></li><li data-lake-id="eb0cca524c43e0a9ce293eede29d701f" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>nl_NL</span></code><span>: Dutch</span></li><li data-lake-id="d9a583444205ee3b53f23deea6628c14" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>it_IT</span></code><span>: Italian</span></li><li data-lake-id="5d7b1755b13a8740b5f9893f855ec922" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>de_DE</span></code><span>: German</span></li><li data-lake-id="be3cc4cee2c3501142891fa2a3a02883" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>zh_CN</span></code><span>: Simplified Chinese</span></li><li data-lake-id="c0e86a30803ded4feeb20cea850b18a7" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>zh_HK</span></code><span>: Traditional Chinese</span></li></ul></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="860f8ac99d51a039634b7be90e7c8ff2" id="ue49570c0" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:#20304C"></span><em><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">setOption</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="d573c2dbad2c7ce78cf47932c4537e4f" id="u2788e75b" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:#20304C"></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="fb4e2f1304df850eb4502952a2b1609c" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">It is used to specify whether to use the default loading pattern and the sandbox environment. Valid values are:</span></p><ul data-lake-id="6ca630139183a80e1664696d0648d3ef" lake-indent="0" style="list-style-type:disc;padding-left:23px;margin:0px;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word"><li data-lake-id="e3e93ab61e0b2d791a489491c9c468af" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>"sandbox", "true"</span></code><span>: Sandbox environment</span></li><li data-lake-id="011bde1dc62890ee6b53e6024d43d07b" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>"sandbox", "false"</span></code><span>: Production environment</span></li><li data-lake-id="3ee482038c62f904f6597d0dc4fd3b35" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>"showLoading", "true"</span></code><span>: Use the default loading pattern.</span></li><li data-lake-id="57c454a3b07896a3d7f855d84121ad57" style="text-align:left"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>"showLoading", "false"</span></code><span>: Do not use the default loading pattern.</span></li></ul></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="2367b23e3ef6d61950fcac93304a5b81" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">setOnCheckoutListener</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="569eca1db5288284178c210b59e8b842" id="u13a28ceb" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:#20304C"></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="bdb79b07641fc2598c249fbb8bb4d89f" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>Create an instance of the </span><strong><span>OnCheckoutListener </span></strong><span>API, which is used for event handling in the subsequent process. The API includes the following method:</span></p><ul data-lake-id="0791514e6bb479ba2c10d8304b215f38" lake-indent="0" style="list-style-type:disc;padding-left:23px;margin:0px;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word"><li data-lake-id="b67c5e4f69cc1227fe8bea577c02876d"><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span>onEventCallback</span></code><span>: Required. A callback function that monitors payment events on the checkout page, returning </span><em><span>eventCode</span></em><span> and </span><em><span>eventResult</span></em><span>.</span></li></ul></td></tr></tbody></table>

The following sample code shows how to instantiate the SDK:

copy

    AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration();
    configuration.setLocale(new Locale("en", "US"));
    // Specify showLoading as true (default value) to use the default loading pattern. Specify it as false to customize the loading animation based on onEventCallback.
    configuration.setOption("showLoading", "true");
    // Set the sandbox environment. If you leave it empty, the production environment is used by default.
    configuration.setOption("sandbox", "true");
    // Configure whether the payment button is rendered by the SDK component.
    configuration.setOption("showSubmitButton", "true");
    // Set the callback to monitor payment events on the checkout page.
    configuration.setOnCheckoutListener(new OnCheckoutListener() {
        @Override
        public void onEventCallback(String eventCode, AMSEventResult eventResult) {
            Log.e(TAG, "onEventCallback eventCode=" + eventCode + " eventResult=" + eventResult.toString());
        }
    });
    // Instantiate AMSCashierPayment.
    AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();

### Invoke the SDK

Call the `createComponent` method:

<table style="width:748px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="211" span="1"><col width="97" span="1"><col width="440" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="dccc242f53ac968be5c31b6b09a95f67" id="u0212e586" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Parameter name</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="1a5acad53d77b9b800d7758b138aa54d" id="u31c41301" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Required</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="b3b9abda1d23ec1f3e06a12bcab6e6aa" id="u85a3aa96" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Description</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="10be8f3e706ab7ddeb961451419da775" id="ue98caa71" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span class="lake-fontsize-11" style="color:rgba(4, 15, 36, 0.85);font-size:14px" data-mce-style="font-size: 11px">sessionData</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="ee85478c5c03ee10d296da5626c4adc0" id="ucda7a3a1" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>✅</span><span style="color:#20304C"></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="ce51e5a99304cec4f5de9ad206b907c4" id="uc5eff8a5" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>Create a configuration object by using the </span><em><span>sessionData</span></em><span> parameter: Pass the complete data in the </span><em><span>paymentSessionData</span></em><span> parameter obtained in the response through the </span><strong><span>createpaymentSession (Checkout Payment) </span></strong><span>API to the </span><em><span>sessionData </span></em><span>parameter.</span></p></td></tr></tbody></table>

Call the `onDestroy` method to free SDK component resources in the following situations:

*   When the buyer exits the checkout page, free the component resources created in the **createPaymentSession**.
*   When the buyer initiates multiple payments, free the component resources created in the previous **createPaymentSession**.

The following sample code shows how to invoke the SDK:

copy

    checkout.createComponent(activity, sessionData);
    
    //Free SDK component resources
    checkout.onDestroy();

### Display payment results

The payment result will be returned through the `onEventCallback` function. The payment result here is only for front-end display, and the final order status is subject to the server side. You need to customize the processing flow you want for each payment result through the data in the result of `onEventCallback.`

The following are the possible event codes of the payment result returned by `onEventCallback`.

<table style="width:873px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="264" span="1"><col width="230" span="1"><col width="379" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="c925a1ba37b2c8a6ba702afae26f2314" id="u7c0579bc" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span>Event code</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="66c01cb4baac6bad96f5a2931e784c5c" id="uffdbb30d" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span>Message</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="74835a6ba7aa4daf0fc7afe43e344c6e" id="u0b0267d0" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span>Solution</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="a167e351edc1453c6eb20241d8c75b7a" id="ubfa995a2" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>SDK_PAYMENT_SUCCESSFUL</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="052e301b618fdceba59815b4d7653e01" id="u94a81535" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">Payment was successful.</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="c47787784867e10c20e393f8c08208c2" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">Suggest redirecting </span>buyer<span style="color:rgba(4, 15, 36, 0.85)">s to the payment result page.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="6d7051566e89c45b26125a3ad372e453" id="u218c26c2" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>SDK_PAYMENT_PROCESSING</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="b9ce56489ec9978a882ee7103ce2244d" id="ua1c57d91" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">Payment was being processed.</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="94510db5282419945ae90206b45341be" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">We suggest that you check the value of </span><em><span style="color:rgba(4, 15, 36, 0.85)">paymentResultCode</span></em><span style="color:rgba(4, 15, 36, 0.85)"> in the onEventCallback result data for details. Guide </span>buyer<span style="color:rgba(4, 15, 36, 0.85)">s to retry the payment based on the provided information.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="642a3318d17f6bde73059e65f348afa7" id="ud8fe9617" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>SDK_PAYMENT_FAIL</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="84f58d7331510dc25baad55c2b67b0c0" id="ud18bd7b4" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">Payment failed.</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0bc9d6d39612ef2c0fba75c7d314ab79" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">We suggest that you check the value of </span><em><span style="color:rgba(4, 15, 36, 0.85)">paymentResultCode</span></em><span style="color:rgba(4, 15, 36, 0.85)"> in the onEventCallback result data for details. Guide </span>buyer<span style="color:rgba(4, 15, 36, 0.85)">s to retry the payment based on the provided information.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="f53f06a0fff71363a8d0847aeb8d43a1" id="u05ba9588" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>SDK_PAYMENT_CANCEL</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="8df585877cf0505cfc8e1dfbe351ba92" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>The </span>buyer<span> exits the payment page without submitting the order.</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="19dd5594c71d4d2ecd618530542da46a" id="u66fa09a2" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>The SDK can be re-invoked with a </span><em><span>paymentSessionData</span></em><span> within the validity period; if it has expired, the </span><em><span>paymentSessionData</span></em><span> needs to be re-requested.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="11e0eb1e6fb2218015ee47227a8a1542" id="ue2972b66" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>SDK_PAYMENT_ERROR</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="afc2579013d064b2b3e28d72bed80cc8" id="u7f2fac3b" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">The payment status was abnormal.</span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="5dc5c473fc2ea28d12931a703a81b353" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">We suggest that you check the value of </span><em><span style="color:rgba(4, 15, 36, 0.85)">paymentResultCode</span></em><span style="color:rgba(4, 15, 36, 0.85)"> in the onEventCallback result data for details. Guide </span>buyer<span style="color:rgba(4, 15, 36, 0.85)">s to retry the payment based on the provided information.</span></p></td></tr></tbody></table>

The following sample code shows how to process the `onEventCallback`:

copy

    AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration();
    configuration.setLocale(new Locale("en", "US"));
    // Specify showLoading as true (default value) to use the default loading pattern. Specify it as false to customize the loading animation based on onEventCallback.
    configuration.setOption("showLoading", "true");
    // Set the sandbox environment. If you leave it empty, the production environment is used by default.
    configuration.setOption("sandbox", "true");
    // Configure whether the payment button is rendered by the SDK component.
    configuration.setOption("showSubmitButton", "true");
    // Set the callback to monitor payment events on the checkout page.
    configuration.setOnCheckoutListener(new OnCheckoutListener() {
        @Override
        public void onEventCallback(String eventCode, AMSEventResult eventResult) {
            Log.e(TAG, "onEventCallback eventCode=" + eventCode + " eventResult=" + eventResult.toString());
    
            if (!TextUtils.isEmpty(eventCode)) {
                if ("SDK_PAYMENT_SUCCESSFUL".equals(eventCode)) {
                    // Payment was successful. Redirect buyers to the payment result page.
                } else if ("SDK_PAYMENT_PROCESSING".equals(eventCode)) {
                    // Payment was being processed. Guide buyers to retry the payment based on the provided information.
                } else if ("SDK_PAYMENT_FAIL".equals(eventCode)) {
                    // Payment failed. Guide buyers to retry the payment based on the provided information.
                }else if ("SDK_PAYMENT_CANCEL".equals(eventCode)) {
                    // Guide buyers to retry the payment.
                } else if ("SDK_PAYMENT_ERROR".equals(eventCode)) {
                    // The payment status was abnormal. Guide buyers to retry the payment based on the provided information.
                } else if ("SDK_FORM_VERIFICATION_FAILED".equals(eventCode)) {
                    // The SDK displays a form error code on the element collection page if the form submission fails.
                }
            }
        }
    });
    // Instantiate AMSCashierPayment.
    AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();

Step 3: Obtain payment result Server-side
-----------------------------------------

After the buyer completes the payment or the payment times out, Antom sends the corresponding payment results to you through server interactions, you can obtain the payment result by one of the following methods:

*   Receive the asynchronous notification
*   Inquire about the result

### Receive the asynchronous notification

When the payment reaches a final status of success or failure, Antom sends an asynchronous notification to the _paymentNotifyUrl_ specified in the **createPaymentSession** API through the [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API. When you receive the notification from Antom, you are required to return a response as instructed in [Requirements](https://global.alipay.com/docs/ac/cashier_payment_cn/notification).

Antom allows you to specify the URL in the _paymentNotifyUrl_ parameter within the **createPaymentSession** API. If the URL for each payment is the same, you can also configure it in the Antom Dashboard.

The following code shows a sample of the notification request:

copy

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
        "value": "4200",
        "currency": "SGD"
      },
      "paymentCreateTime": "2020-01-01T12:01:00+08:30",
      "paymentTime": "2020-01-01T12:01:01+08:30"
    }

The following sample code shows how to verify the signature of the notification and make a response to the notification:

copy

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

#### FAQs

##### When will the notification be sent?

It depends on whether the payment is completed:

*   If the payment is successfully completed, Antom will usually send you an asynchronous notification within 3 to 5 seconds. For some payment methods like OTC, the notification might take a bit longer.
*   If the payment is not completed, Antom needs to close the order first before sending an asynchronous notification. The time it takes for different payment methods to close the order varies, usually defaulting to 14 minutes.

##### Will the asynchronous notification be re-sent?

If you receive an asynchronous notification from Antom, you are required to return the response in the [Sample code](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) format. If you do not respond to the asynchronous notification as required, or the asynchronous notification is not delivered due to network reasons, the notification will be automatically resent within 24 hours. The notification can be resent up to 8 times or until a correct response is received to terminate delivery. The sending intervals are as follows: 0 minutes, 2 minutes, 10 minutes, 10 minutes, 1 hour, 2 hours, 6 hours, and 15 hours.

##### Do I need to add a digital signature to the response?

If you receive an asynchronous notification from Antom, you are required to return the response in the [Sample code](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) format, but you do not need to add a digital signature to your response.

##### How do I understand the meaning of the following key fields?

*   _result_: the payment result of the order.
*   _paymentRequestId_: the payment request ID generated by the merchant used for querying, canceling, and reconciliation.
*   _paymentId_: the payment order ID generated by Antom used for refund and reconciliation.
*   _paymentAmount_: if there is a need for amount reconciliation, you can consume this field.

### Inquire about the result

You can call the **inquiryPayment** API to initiate a query on the result of an order.

<table style="width:748px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="211" span="1"><col width="97" span="1"><col width="440" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0440e23f15e8fbfc1ebda120418918ca" id="u3f5430ff" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span style="color:#20304C">Parameter name</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="cc1462feac756a0267d0873ab872e7e5" id="u27f6e593" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span style="color:#20304C">Required</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="866c44b27a096d4252a025d8fb31e8ba" id="u1ad3a168" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span style="color:#20304C">Description</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="c9ebd4b3fb6ccb7f244df5d8998700ab" id="ud473e6db" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>paymentRequestId</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0f3ec39b7a5bbe88f24cb81f2d7bcb1e" id="u55289c52" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="18e8f85e7f8ce7c5bf063b797def80e8" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">The payment request ID generated by </span>the merchant<span style="color:rgba(4, 15, 36, 0.85)">.</span></p></td></tr></tbody></table>

The parameter is not a full set of parameters, refer to the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API for full set of parameters and additional requirements for certain payment methods.

The following sample code shows how to call the **inquiryPayment** API:

copy

    
    AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG,
                    merchantPrivateKey, alipayPublicKey);
    
    AlipayPayQueryRequest alipayPayQueryRequest = new AlipayPayQueryRequest();
    alipayPayQueryRequest.setClientId(CLIENT_ID);
    alipayPayQueryRequest.setPath("/ams/sandbox/api/v1/payments/inquiryPayment");
    
    alipayPayQueryRequest.setPaymentRequstId("paymentRequestId01");
    AlipayPayQueryResponse alipayPayQueryResponse;
        try {
            alipayPayQueryResponse = defaultAlipayClient.execute(alipayPayQueryRequest);
        } catch (AlipayApiException e) {
           String errorMsg = e.getMessage();
                // handle error condition
        }

The following code shows a sample of the request message:

copy

    {
      "paymentRequestId": "paymentRequestId01"
    }

The following code shows a sample of the response message:

copy

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
        "value": "4200",
        "currency": "SGD"
      },
      "paymentCreateTime": "2019-06-01T12:01:01+08:30",
      "paymentTime": "2019-06-01T12:01:01+08:30",
      "transactions": null
    }

#### FAQs

##### How do I understand the meaning of the following key fields?

*   _result_: the result of the API call. It only indicates the result of the **inquiryPayment** API call. The order result should be determined based on the _paymentStatus_. `SUCCESS` and `FAIL` indicate final results, while `PROCESSING` indicates that the transaction is still in progress.
*   _paymentAmount_: amount verification. If there is a need for amount verification, this field can be used.

##### How frequently should I initiate the query?

It is recommended to initiate a round-robin query at an interval of 2 seconds until either the final payment result is retrieved or an asynchronous payment notification is received.

Step 4: Obtain capture result Server-side
-----------------------------------------

After the buyer completes the capture or the capture times out, Antom sends the corresponding capture results to you through server interactions, you can obtain the capture result by one of the following methods:

*   Receive the asynchronous notification
*   Inquire about the result

### **Receive the asynchronous notification**

When the capture reaches a final status of success or failure, Antom sends an asynchronous notification to the _paymentNotifyUrl_ specified in the **createPaymentSession** API through the [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API. When you receive the notification from Antom, you are required to return a response as instructed in [Requirements](https://global.alipay.com/docs/ac/cashier_payment_cn/notification).

Antom allows you to specify the URL in the _paymentNotifyUrl_ parameter within the **createPaymentSession** API. If the URL for each payment is the same, you can also configure it in the Antom Dashboard.

The following code shows a sample of successful capture:

copy

      "captureAmount": {
        "currency": "SGD",
        "value": "4200"
      },
      "notifyType": "CAPTURE_RESULT",
      "captureId": "2022XXXXXXX",
      "captureRequestId": "captureRequestId01",
      "captureTime": "2022-11-10T00:34:52-08:00",
      "paymentId": "2022XXXXXXX",
      "result": {
        "resultCode": "SUCCESS",
        "resultMessage": "success.",
        "resultStatus": "S"
      }
    }

The following code shows a sample of failed capture:

copy

      "captureAmount": {
        "currency": "SGD",
        "value": "4200"
      },
      "notifyType": "CAPTURE_RESULT",
      "captureId": "2022XXXXXXX",
      "captureRequestId": "captureRequestId01",
      "captureTime": "2022-11-10T00:34:52-08:00",
      "paymentId": "2022XXXXXXX",
      "result": {
        "resultCode": "PROCESS_FAIL",
        "resultMessage": "fail.",
        "resultStatus": "F"
      }
    }

The following sample code shows how to verify the signature of the notification and make a response to the notification:

copy

    @RequestMapping(path = "/captureResult", method = RequestMethod.POST)
    public ResponseEntity<AlipayResponse> captureNotifyProcessor(HttpServletRequest request,
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

#### FAQs

##### When will the notification be sent?

It depends on whether the payment is completed:

*   If the payment is successfully completed, Antom will usually send you an asynchronous notification within 3 to 5 seconds. For some payment methods like OTC, the notification might take a bit longer.
*   If the payment is not completed, Antom needs to close the order first before sending an asynchronous notification. The time it takes for different payment methods to close the order varies, usually defaulting to 14 minutes.

##### Will the asynchronous notification be re-sent?

If you receive an asynchronous notification from Antom, you are required to return the response in the [Sample code](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) format. If you do not respond to the asynchronous notification as required, or the asynchronous notification is not delivered due to network reasons, the notification will be automatically resent within 24 hours. The notification can be resent up to 8 times or until a correct response is received to terminate delivery. The sending intervals are as follows: 0 minutes, 2 minutes, 10 minutes, 10 minutes, 1 hour, 2 hours, 6 hours, and 15 hours.

##### Do I need to add a digital signature to the response?

If you receive an asynchronous notification from Antom, you are required to return the response in the [Sample code](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) format, but you do not need to add a digital signature to your response.

##### How do I understand the meaning of the following key fields?

*   _result_: represents the capture result of the order.
*   _notifyType_: the value of notifyType is `CAPTURE_RESULT`.
*   _paymentRequestId_: the payment request number you generated, used for querying, canceling, and reconciliation.
*   _paymentId_: the payment order ID generated by Antom used for refund and reconciliation.
*   _acquirerReferenceNo_: merchants integrating with in-card payment services in Singapore and Hong Kong will receive specific acquirer numbers in the notification.

### **Inquire about the result**

You can call the **inquiryPayment** API to initiate a query on the result of an order.

<table style="width:748px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="211" span="1"><col width="97" span="1"><col width="440" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="c79324bc672f4ce82577aee8e2c5038c" id="u2e692fad" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span style="color:#20304C">Parameter name</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="36818fce1dc487ba92bff1d0f839d2ae" id="ucc62ee77" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span style="color:#20304C">Required</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="42fa88dce165d71934a6f5435f4539a6" id="u72f0ceb4" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span style="color:#20304C">Description</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="4a0643c7c223924fb4225ada9271e5cd" id="ue2a28058" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span>paymentRequestId</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="bd786582aeaf1de16fc7c716157f652b" id="uc2fb7399" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span></span></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="d154710e1ef55b9ebff0eb654aae4374" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">The payment request ID generated by </span>the merchant<span style="color:rgba(4, 15, 36, 0.85)">.</span></p></td></tr></tbody></table>

The parameter is not a full set of parameters, refer to the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API for full set of parameters and additional requirements for certain payment methods.

The following sample code shows how to call the **inquiryPayment** API:

copy

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

The following code shows a sample of the request message:

copy

    {
      "paymentRequestId": "paymentRequestId01"
    }

#### Value of capture status

The value of the _transactions_ in the response of the API is the capture status:

<table style="width:633px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col width="275" span="1"><col width="358" span="1"></colgroup><tbody><tr style="height:33px"><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="b1168706a296e038e4ac3e54667af6ef" id="u4d66a268" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Parameter name</span></strong></p></td><td style="background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="fdac5bd4e833f339385c9e59a9381feb" id="u69b5c0d9" style="text-align:center;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" style="color:rgb(32, 48, 76);font-size:14px" data-mce-style="font-size: 11px">Description</span></strong></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="1e28b1ce801c008599a2f8849b88b510" id="u00191700" style="text-align:left;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">transactions.transationType</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="7798d7ce6edcc9b68b684e23c6236fbc" id="u28f25565" style="text-align:left;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">The value is </span><code style="font-family:monospace;font-size:inherit;background-color:rgba(0, 0, 0, 0.06);padding:0px 2px;border:1px solid rgba(0, 0, 0, 0.08);border-radius:2px;line-height:inherit;overflow-wrap:break-word;text-indent:0px"><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">CAPTURE</span></code><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">, meaning </span><span style="color:rgba(4, 15, 36, 0.85)">the capture status.</span></p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="46e7113cd3906a5c0442fe962a0fc2fb" id="uba8aaedc" style="text-align:left;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><em><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">transactions.transactionResult</span></em></p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="8c347dbb44b662f4e44aeb94c24e0fdd" id="u22985684" style="text-align:left;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span style="color:rgba(4, 15, 36, 0.85)">Capture status</span></p></td></tr></tbody></table>

The following code shows a sample of successful capture:

copy

    {
        "transactions": [
            {
                "transactionType": "CAPTURE",
                "transactionStatus": "SUCCESS",
                "transactionRequestId": "test_test_test_XXXX",
                "transactionAmount": {
                    "currency": "SGD",
                    "value": "4200"
                },
                "transactionId": "2022XXXXXXXX",
                "transactionResult": {
                    "resultStatus": "S",
                    "resultCode": "SUCCESS",
                    "resultMessage": "success"
                }
            }
        ]
    }

The following code shows a sample of failed capture:

copy

    {
        "transactions": [
            {
                "transactionType": "CAPTURE",
                "transactionStatus": "FAIL",
                "transactionRequestId": "test_test_test_XXXX",
                "transactionAmount": {
                    "currency": "SGD",
                    "value": "4200"
                },
                "transactionTime": "2022-09-29T07:13:50-07:00",
                "transactionId": "2022XXXXXXXX",
                "transactionResult": {
                    "resultStatus": "F",
                    "resultCode": "PROCESS_FAIL",
                    "resultMessage": "General business failure. No retry."
                }
            }
        ]
    }

The following code shows a sample of processing capture:

copy

    {
        "transactions": [
            {
                "transactionType": "CAPTURE",
                "transactionStatus": "PROCESSING",
                "transactionRequestId": "test_test_test_XXXX",
                "transactionAmount": {
                    "currency": "SGD",
                    "value": "4200"
                },
                "transactionId": "2022XXXXXXXX",
                "transactionResult": {
                    "resultStatus": "U",
                    "resultCode": "PAYMENT_IN_PROCESS",
                    "resultMessage": "payment in process"
                }
            }
        ]
    }

#### FAQs

##### How do I understand the meaning of the following key fields?

*   _result_: the result of the API call. It only indicates the result of the **inquiryPayment** API call. The order result should be determined based on the _paymentStatus_. `SUCCESS` and `FAIL` indicate final results, while `PROCESSING` indicates that the transaction is still in progress.
*   _paymentAmount_: amount verification. If there is a need for amount verification, this field can be used.

##### How frequently should I initiate the query?

It is recommended to initiate a round-robin query at an interval of 2 seconds until either the final payment result is retrieved or an asynchronous payment notification is received.

Sample codes
============

Full sample codes for front-end:

copy

    AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration();
    configuration.setLocale(new Locale("en", "US"));
    // Specify showLoading as true (default value) to use the default loading pattern. Specify it as false to customize the loading animation based on onEventCallback.
    configuration.setOption("showLoading", "false");
    // Set the sandbox environment. If you leave it empty, the production environment is used by default.
    configuration.setOption("sandbox", "true");
    // Configure whether the payment button is rendered by the SDK component.
    configuration.setOnCheckoutListener(new OnCheckoutListener() {
        @Override
        public void onEventCallback(String eventCode, AMSEventResult eventResult) {
            AlipayLog.e(TAG, "onEventCallback eventCode=" + eventCode + " eventResult=" + eventResult.toString());
    
            if (!TextUtils.isEmpty(eventCode)) {
                if ("SDK_PAYMENT_SUCCESSFUL".equals(eventCode)) {
                    // Payment was successful. Redirect buyers to the payment result page.
                } else if ("SDK_PAYMENT_PROCESSING".equals(eventCode)) {
                    // Payment was being processed. Guide buyers to retry the payment based on the provided information.
                } else if ("SDK_PAYMENT_FAIL".equals(eventCode)) {
                    // Payment failed. Guide buyers to retry the payment based on the provided information.
                }else if ("SDK_PAYMENT_CANCEL".equals(eventCode)) {
                    // Guide buyers to retry the payment.
                } else if ("SDK_PAYMENT_ERROR".equals(eventCode)) {
                    // The payment status was abnormal. Guide buyers to retry the payment based on the provided information.
                } else if ("SDK_END_OF_LOADING".equals(eventCode)) {
                    // End your custom loading animation.
                }
            }
        }
    });
    // Instantiate AMSCashierPayment.
    AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();
    
    checkout.createComponent(activity, sessionData);

Event codes  

==============

You might see two types of event codes:

*   Status codes: Returned by `onEventCallback` during the component's runtime lifecycle.
*   Error codes: Returned by `onEventCallback` or `onError` during the component initialization phase.

<table style="width:821px;outline:none;border-collapse:collapse;border:1px solid rgb(217, 217, 217)" class="lake-table"><colgroup><col span="1" width="148"><col span="1" width="204"><col span="1" width="265"><col span="1" width="204"></colgroup><tbody><tr style="height:33px"><td style="text-align:center;vertical-align:top;background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0b005a8154cfba11c1c7c0c28298e8d3" id="u30405c04" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">Type</span></strong></p></td><td style="text-align:center;vertical-align:top;background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="80198adf91a13878efa95070abab7085" id="u06eef118" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span class="lake-fontsize-11" data-mce-style="font-size: 11px" style="font-size:14px">Code</span></strong></p></td><td style="text-align:center;vertical-align:top;background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="c2901d12bb6644f45ae815478b373a42" id="ua01cd051" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span>Description</span></strong></p></td><td style="text-align:center;vertical-align:top;background-color:rgb(212, 238, 252);min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="4d5ffe4d1c17d41042c04488e39360ab" id="u379fc3ca" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><strong><span>Further action</span></strong></p></td></tr><tr style="height:33px"><td rowspan="2" style="text-align:center;vertical-align:middle;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="8e0c1d7f70cc34ebab53d7a5f666aef3" id="u6baf56a0" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>Status codes</span></p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="0eb22034915d7569dc458517ab32969f" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">SDK_START_OF_LOADING</p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="f7e437222c1c0ac9853769938499a111" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">The loading animation starts to play during the payment component creation.</p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="cd7ea3bb031fbbd20de6ee8169f622ca" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>No further action.</span></p></td></tr><tr style="height:33px"><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="970c39128428e57a8471475f1b68042d" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">SDK_END_OF_LOADING</p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="53e7f775e4b4ff25b6452740792b4dfb" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">The loading animation ends during the payment component creation.</p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="980de3e134cf4e8d2af39286979c75ca" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">No further action.</p></td></tr><tr style="height:33px"><td rowspan="4" colspan="1" style="text-align:center;vertical-align:middle;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="993fa670d54f26853983723b5ef17029" id="u9c921db8" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>Error codes</span></p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="05e1c73492cd0cfff9258d3da8b84a36" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">SDK_INTERNAL_ERROR</p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="57173f172e85ba5fa004bab8ae6def9e" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">The internal error of the SDK occurs.</p></td><td style="text-align:left;vertical-align:top;min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="03df1e49fac48e67d6f85ebf8d4c2a97" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">Contact Antom Technical Support to resolve the issue.</p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="7ed2677c9be754c4e0b4fd80945a9e46" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">SDK_CREATEPAYMENT_PARAMETER_ERROR</p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="5b6e469d4bfa87cbf17d863b0ae415f7" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">The parameters passed into the createComponent method are incorrect.</p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="575ac1996d2880456a38d4b21b09d5cf" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">Ensure the parameters are passed correctly and send a new request.</p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="87743b7130a4652faf13fd3db514404b" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">SDK_CALL_URL_ERROR</p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="5a338df99db49a22fcffa0fa168c52e4" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px"><span>Represents one of the following cases:</span></p><ul data-lake-id="2165e8724ce708ab75cc9cab678d7687" lake-indent="0" style="list-style-type:disc;padding-left:23px;margin:0px;font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word"><li data-lake-id="9c27b18d63a244f209dbbdfce9134695"><span>The redirection to the merchant page failed to be executed.</span></li><li data-lake-id="d21b02a90cc210ba4265a7cb277cda67"><span>The parameter</span> <em><span>paymentRedirectUrl</span></em><em> </em><span>in your</span> <strong><span>createpaymentSession (Cashier Payment)</span></strong> <span>request is not passed or passed incorrectly.</span></li></ul></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="b56b4f83e5cba8264bb318d6c22e62d0" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">Contact Antom Technical Support to resolve the issue.</p></td></tr><tr style="height:33px"><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="69f799df3470472eb2caf7b639cb7e8e" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">SDK_INTEGRATION_ERROR</p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="77272cf883487634e703d85befd1e09e" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">Dependencies are not found.</p></td><td style="min-width:90px;font-size:14px;white-space:normal;overflow-wrap:break-word;border:1px solid rgb(217, 217, 217);padding:4px 8px;cursor:default"><p data-lake-id="feb5070aabf1f275c43e4b030b9b087a" style="font-size:14px;color:rgb(38, 38, 38);line-height:1.74;letter-spacing:0.05em;outline-style:none;overflow-wrap:break-word;margin-top:0px;margin-bottom:0px">Ensure that the dependencies are added correctly and retry the integration process.</p></td></tr></tbody></table>

![Image 5](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 6](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)

#### Is this page helpful?

#### On this page

[User experience](#fc442 "User experience")

[Payment flow](#eLZVd "Payment flow")

[Integration steps](#QLFGi "Integration steps")

[Step 1: Create a payment session](#zhBSk "Step 1: Create a payment session")

[Install an API library](#d3kyo "Install an API library")

[Initialize request instance](#WLui0 "Initialize request instance")

[Create a payment session](#fzPO2 "Create a payment session")

[Sample codes of calling the createPaymentSession API](#3L7zQ "Sample codes of calling the createPaymentSession API")

[FAQs](#UGjGp "FAQs")

[Can Chinese characters be used in the request?](#asEuc "Can Chinese characters be used in the request?")

[How to set the payment result notification address?](#KQLhk "How to set the payment result notification address?")

[Step 2: Create and invoke the SDK](#xhgER "Step 2: Create and invoke the SDK")

[Install](#Ddkes "Install")

[Instantiate the SDK](#KQO5X "Instantiate the SDK")

[Invoke the SDK](#OXd8h "Invoke the SDK")

[Display payment results](#s5Wpy "Display payment results")

[Step 3: Obtain payment result](#CH9lr "Step 3: Obtain payment result")

[Receive the asynchronous notification](#MfdWT "Receive the asynchronous notification")

[FAQs](#V1F5v "FAQs")

[Inquire about the result](#UpOeG "Inquire about the result")

[FAQs](#tkpZO "FAQs")

[Step 4: Obtain capture result](#lSBz0 "Step 4: Obtain capture result")

[Receive the asynchronous notification](#nnrAd "Receive the asynchronous notification")

[FAQs](#Bdbew "FAQs")

[Inquire about the result](#NrYhL "Inquire about the result")

[Value of capture status](#q3e0A "Value of capture status")

[FAQs](#Waqa6 "FAQs")

[Sample codes](#BJbEu "Sample codes")

[Event codes](#blzVa "Event codes")