信用卡支付（Android）| 结账支付 | 支付宝文档
==================

[![支付宝，中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg) ![支付宝，中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fcashierpay%2Fadcard)  
[返回首页](../../)

结账支付  
[概述](/docs/ac/cashierpay/overview)  
接收支付  
SDK集成  
[APM支付（Web/WAP）](/docs/ac/cashierpay/apm_ww)  
[APM支付（Android）](/docs/ac/cashierpay/apm_android)  
[APM支付（iOS）](/docs/ac/cashierpay/apm_ios)  
[信用卡支付（Web/WAP）](/docs/ac/cashierpay/wwcard)  
[信用卡支付（Android）](/docs/ac/cashierpay/adcard)  
[信用卡支付（iOS）](/docs/ac/cashierpay/ioscard)  
API仅集成  
支付后  
支付方式  
其他资源  
高级功能  
[预前端解决方案API](/docs/ac/cashierpay/prefront)  
[先买后付API](/docs/ac/cashierpay/bnpl)  
[卡存储API](/docs/ac/cashierpay/cv)  
[卡存储SDK](/docs/ac/cashierpay/cvsdk)  
[卡支付功能API/SDK](/docs/ac/cashierpay/mf?pageVersion=7)  
信用卡支付（Android）
=======================

2024-05-11 10:13  
Antom SDK是一个预构建的UI组件，用于收集卡信息并为您处理3D认证流程。集成此组件不需要您具有PCI资格，适合那些希望委托Antom收集卡信息的情况。

用户体验
===============

以下图示显示了在应用程序中支付的用户流程：  
![Image 3: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1711338358204-54fb815f-6754-404f-a95a-6407e14573ce.png)  

支付流程
============

对于每种支付方式，支付流程由以下步骤组成：  
![Image 4: 111卡.webp](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1713521451605-d3ce7ff5-694a-441c-8724-2b82d2a8f2df.webp)  

1. **用户进入结账页面。**  
2. **创建** [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) **请求**
   买家选择支付方式并提交订单后，您可以通过调用[**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier)接口获取支付会话。
3. **调用客户端SDK**
   在客户端，通过支付会话调用SDK。SDK将根据支付方式的特性处理信息收集、重定向、应用调用、二维码显示、验证等流程。
4. **获取支付结果**
   通过以下两种方法之一获取支付结果：  
   1. 异步通知：在[**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier)接口中指定_paymentNotifyUrl_，设置接收异步通知的地址。支付成功或过期时，Antom将使用[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online)向您发送异步通知。
   2. 同步查询：调用[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online)接口检查支付状态。  
5. **获取扣款结果**
   对于信用卡支付，您需要通过以下两种方法之一获取扣款结果：  
   1. 异步通知：在[**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier)接口中指定_paymentNotifyUrl_，设置接收异步通知的地址。当支付请求成功或过期时，Antom将使用[**notifyCapture**](https://global.alipay.com/docs/ac/ams/notify_capture)向您发送异步通知。
   2. 同步查询：调用[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online)接口检查支付请求状态。  

集成步骤
=================  

按照以下步骤开始集成：  
1. 创建支付会话
2. 创建并调用SDK
3. 获取支付结果
4. 获取扣款结果  

步骤1：创建支付会话 服务器端
--------------------------------------------  

当买家选择Antom提供的支付方式时，您需要收集支付请求ID、订单金额、支付方式、订单描述、支付重定向URL和支付结果通知URL等关键信息，调用**createPaymentSession** API创建支付会话，并将支付会话返回给客户端。

Antom提供了多种语言的服务器端API库。以下代码以Java为例，您需要安装Java 6或更高版本。
### 安装API库
您可以在[GitHub](https://github.com/alipay/global-open-sdk-java)上找到最新版本。  
复制以下内容：  
```xml
<dependency>
    <groupId>com.alipay.global.sdk</groupId>
    <artifactId>global-open-sdk-java</artifactId>
    <version>2.0.21</version>
</dependency>
```

这段代码是用于Maven项目的依赖配置，将它添加到您的`pom.xml`文件中，即可引入蚂蚁金服的全球开放SDK Java版，版本号为2.0.21。
### 初始化请求实例  
创建一个单例资源以向Antom发起请求。  
复制  
```java
import com.alipay.global.api.AlipayClient;
import com.alipay.global.api.DefaultAlipayClient;

String merchantPrivateKey = "您的私钥";
String alipayPublicKey = "支付宝公钥";
AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG,
    merchantPrivateKey, alipayPublicKey);
```

这里的代码是在Java环境中初始化一个用于与Antom（可能是蚂蚁金服的某个服务）交互的请求客户端。`DefaultAlipayClient`是客户端的实现类，它需要商户的私钥(`merchantPrivateKey`)和支付宝的公钥(`alipayPublicKey`)作为参数。`EndPointConstants.SG`代表请求的endpoint，可能是指新加坡（SG）的服务器。
### 创建支付会话  
创建支付会话涉及以下参数：  
| 参数名 | 是否必需 | 描述 |
| --- | --- | --- |
| productCode | 是 | 代表所使用的支付产品，根据合同规定。对于结账支付，值固定为 `CASHIER_PAYMENT`。 |
| paymentRequestId | 是 | 商家为识别支付请求分配的唯一ID。 |
| paymentAmount | 是 | 您请求以订单货币接收的支付金额。 |
| paymentMethod | 是 | 商家或收单方用来收集支付的方法。 |
| paymentRedirectUrl | 是 | 买家在支付完成后重定向到的商家页面URL。 |
| order | 是 | 包含买家、商家、商品、金额、配送信息和购买环境的订单信息。 |
| paymentNotifyUrl | 可选 | 支付结果通知地址，可以通过接口传递或通过门户设置为固定值。 |
| settlementStrategy | 可选 | 支付请求的结算策略。 |

上述参数是创建支付会话的基本参数。完整参数和某些支付方法的额外要求，请参考[**createPaymentSession (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/session_cashier)**。**  

#### 调用createPaymentSession API 的示例代码  
以下示例代码展示了如何调用 **createPaymentSession** API：  
```java
AlipayPaymentSessionRequest alipayPaymentSessionRequest = new AlipayPaymentSessionRequest();
alipayPaymentSessionRequest.setClientId(CLIENT_ID);
alipayPaymentSessionRequest.setPath("/ams/sandbox/api/v1/payments/createPaymentSession");
alipayPaymentSessionRequest.setProductCode(ProductCodeType.CASHIER_PAYMENT);  
// 替换为您的 paymentRequestId
alipayPaymentSessionRequest.setPaymentRequestId("paymentRequestId01");  
Amount amount = new Amount();
amount.setCurrency("SGD");
amount.setValue("4200");  
alipayPaymentSessionRequest.setPaymentAmount(amount);  
// 设置结算货币
SettlementStrategy settlementStrategy = new SettlementStrategy();
settlementStrategy.setSettlementCurrency("SGD");
alipayPaymentSessionRequest.setSettlementStrategy(settlementStrategy);  
// 设置支付方式
PaymentMethod paymentMethod = new PaymentMethod();
paymentMethod.setPaymentMethodType("CARD");
alipayPaymentSessionRequest.setPaymentMethod(paymentMethod);  
// 设置支付因子
PaymentFactor paymentFactor = new PaymentFactor();
paymentFactor.setAuthorization(true);
alipayPaymentSessionRequest.setPaymentFactor(paymentFactor);  
// 设置订单信息
Order order = new Order();
order.setReferenceOrderId("referenceOrderId01");
order.setOrderDescription("antom sdk test order");
order.setOrderAmount(amount);
Buyer buyer = new Buyer();
buyer.setReferenceBuyerId("yourBuyerId");
order.setBuyer(buyer);
order.setOrderAmount(amount);
alipayPaymentSessionRequest.setOrder(order);  
// 替换为您的通知URL
alipayPaymentSessionRequest.setPaymentNotifyUrl("https://www.yourNotifyUrl");  
// 替换为您的重定向URL
alipayPaymentSessionRequest.setPaymentRedirectUrl("https://www.yourMerchantWeb.com");
AlipayPaymentSessionResponse alipayPaymentSessionResponse = null;  
try {
    alipayPaymentSessionResponse = defaultAlipayClient.execute(alipayPaymentSessionRequest);
} catch (AlipayApiException e) {
    String errorMsg = e.getMessage();
    // 处理错误情况
}  
```
以下代码展示了请求消息的示例：  
```json
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
```
以下代码展示了响应示例，其中包含以下参数：
*   `paymentSessionData`: 用于返回前端的支付会话数据
*   `paymentSessionExpiryTime`: 支付会话的过期时间  
```json
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
```
### 常见问题解答  
#### 请求中可以使用中文字符吗？  
请勿在请求中的字段，包括`paymentRequestId`、`referenceOrderId`、`orderDescription`和`goods`使用中文字符，以避免与QRIS和Mastercard等不兼容的支付方式。  
#### 如何设置支付结果通知地址？  
Antom会通过[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online)接口发送支付结果。您可以在**createPaymentSession** API中通过`paymentNotifyUrl`参数指定此地址。如果每个支付的通知地址相同，您也可以在Antom控制台上进行配置。如果您同时在控制台配置了地址并在API中设置了参数，Antom将使用API中设置的地址。  
### 步骤2：创建并调用SDK客户端
---------------------------------------------  
Antom SDK是一个用于处理支付流程的组件。通过创建支付会话，您可以收集信息、在应用间切换以及根据**createPaymentSession** API中指定的支付方式显示二维码来初始化SDK。  
当买家在页面上选择支付方式后，您需要创建SDK并使用支付会话来启动它。
### 安装  
版本要求：目标至少为Android 4.4（API级别19）或更高。  
要集成SDK包，请参考[集成SDK包](https://global.alipay.com/docs/ac/antom_sdk/android_en)。
### 初始化SDK  
使用`AMSCashierPayment`创建SDK实例，并指定基础配置。创建配置对象包括以下方法：

| 方法名称 | 是否必需 | 描述 |
| --- | --- | --- |
| `setLocale` | 不必需 | 用于传入语言信息。有效值如下，根据支付方式所在地区选择传入的值。如果传入其他值，默认使用本地语言： |
| `en_US` | 英语 |
| `pt_BR` | 葡萄牙语 |
| `ko_KR` | 韩语 |
| `es_ES` | 西班牙语 |
| `ms_MY` | 马来语 |
| `in_ID` | 印尼语 |
| `tl_PH` | 塔加洛语 |
| `th_TH` | 泰语 |
| `vi_VN` | 越南语 |
| `fr_FR` | 法语 |
| `nl_NL` | 荷兰语 |
| `it_IT` | 意大利语 |
| `de_DE` | 德语 |
| `zh_CN` | 简体中文 |
| `zh_HK` | 繁体中文 |

| `setOption` | 不必需 | 用于指定是否使用默认加载模式和沙箱环境。有效值为： |
| `"sandbox", "true"` | 沙箱环境 |
| `"sandbox", "false"` | 生产环境 |
| `"showLoading", "true"` | 使用默认加载模式 |
| `"showLoading", "false"` | 不使用默认加载模式 |

| `setOnCheckoutListener` | 不必需 | 创建`OnCheckoutListener`接口实例，用于后续流程中的事件处理。接口包含以下方法： |
| `onEventCallback` | 必需 | 监听结账页面的支付事件，返回`eventCode`和`eventResult`。 |

以下示例代码展示了如何实例化SDK：

```java
AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration();
configuration.setLocale(new Locale("en", "US"));
// 默认值为true，使用默认加载模式。设置为false以根据onEventCallback自定义加载动画。
configuration.setOption("showLoading", "true");
// 设置沙箱环境。不设置则默认使用生产环境。
configuration.setOption("sandbox", "true");
// 配置是否由SDK组件渲染支付按钮。
configuration.setOption("showSubmitButton", "true");
// 设置监听结账页面支付事件的回调。
configuration.setOnCheckoutListener(new OnCheckoutListener() {
    @Override
    public void onEventCallback(String eventCode, AMSEventResult eventResult) {
        Log.e(TAG, "onEventCallback eventCode=" + eventCode + " eventResult=" + eventResult.toString());
    }
});
// 初始化AMSCashierPayment。
AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();
```

请注意，`activity`参数应替换为您的Activity实例。
### 调用SDK

调用`createComponent`方法：

| 参数名 | 是否必填 | 描述 |
| --- | --- | --- |
| sessionData | ✅ | 使用`sessionData`参数创建配置对象：将通过`createpaymentSession（结账支付）`API获取的`paymentSessionData`参数中的完整数据传递给`sessionData`参数。 |

在以下情况下调用`onDestroy`方法释放SDK组件资源：

1. 买家退出结账页面时，释放`createPaymentSession`中创建的组件资源。
2. 买家发起多次支付时，释放前一次`createPaymentSession`创建的组件资源。

以下示例代码展示了如何调用SDK：

```java
checkout.createComponent(activity, sessionData);
// 释放SDK组件资源
checkout.onDestroy();
```

请注意，这段文档是针对某个支付或结账流程的SDK使用说明，其中`activity`代表Android中的Activity对象，`sessionData`包含了支付会话的相关信息。在实际应用中，需要根据具体的SDK接口和上下文进行操作。
### 显示支付结果  
支付结果将通过`onEventCallback`函数返回。这里的支付结果仅用于前端展示，最终订单状态以服务器端为准。您需要通过`onEventCallback`返回结果中的数据自定义每个支付结果的处理流程。  
以下是`onEventCallback`返回的支付结果可能的事件代码：  

| 事件代码 | 消息 | 解决方案 |
| --- | --- | --- |
| SDK_PAYMENT_SUCCESSFUL | 支付成功。 | 建议将买家重定向到支付结果页面。 |
| SDK_PAYMENT_PROCESSING | 支付处理中。 | 建议检查`onEventCallback`结果数据中的`paymentResultCode`详细信息。根据提供的信息引导买家重试支付。 |
| SDK_PAYMENT_FAIL | 支付失败。 | 建议检查`onEventCallback`结果数据中的`paymentResultCode`详细信息。根据提供的信息引导买家重试支付。 |
| SDK_PAYMENT_CANCEL | 买家未提交订单退出支付页面。 | 在有效期内，可以使用`paymentSessionData`重新调用SDK；如果已过期，需要重新请求`paymentSessionData`。 |
| SDK_PAYMENT_ERROR | 支付状态异常。 | 建议检查`onEventCallback`结果数据中的`paymentResultCode`详细信息。根据提供的信息引导买家重试支付。 |

以下示例代码展示了如何处理`onEventCallback`：

```java
AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration();
configuration.setLocale(new Locale("en", "US"));
// 设置showLoading为true（默认值）以使用默认加载模式。设置为false以根据onEventCallback自定义加载动画。
configuration.setOption("showLoading", "true");
// 设置沙箱环境。如果不设置，默认使用生产环境。
configuration.setOption("sandbox", "true");
// 配置是否由SDK组件渲染支付按钮。
configuration.setOption("showSubmitButton", "true");
// 设置监听结账页面支付事件的回调。
configuration.setOnCheckoutListener(new OnCheckoutListener() {
    @Override
    public void onEventCallback(String eventCode, AMSEventResult eventResult) {
        Log.e(TAG, "onEventCallback eventCode=" + eventCode + " eventResult=" + eventResult.toString());
        if (!TextUtils.isEmpty(eventCode)) {
            if ("SDK_PAYMENT_SUCCESSFUL".equals(eventCode)) {
                // 支付成功。将买家重定向到支付结果页面。
            } else if ("SDK_PAYMENT_PROCESSING".equals(eventCode)) {
                // 支付处理中。根据提供的信息引导买家重试支付。
            } else if ("SDK_PAYMENT_FAIL".equals(eventCode)) {
                // 支付失败。根据提供的信息引导买家重试支付。
            } else if ("SDK_PAYMENT_CANCEL".equals(eventCode)) {
                // 引导买家重试支付。
            } else if ("SDK_PAYMENT_ERROR".equals(eventCode)) {
                // 支付状态异常。根据提供的信息引导买家重试支付。
            } else if ("SDK_FORM_VERIFICATION_FAILED".equals(eventCode)) {
                // 如果表单提交失败，SDK在元素收集页面显示表单错误代码。
            }
        }
    }
});
// 实例化AMSCashierPayment。
AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();
```

### 步骤3：获取支付结果（服务器端）
-----------------------------------------

买家完成支付或支付超时后，Antom会通过服务器交互将相应的支付结果发送给您，您可以通过以下方法之一获取支付结果：

1. 接收异步通知
2. 查询结果
### 接收异步通知  
当支付成功或失败并达到最终状态时，蚂蚁金服会通过[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API，将异步通知发送到在**createPaymentSession** API中指定的_paymentNotifyUrl_。收到蚂蚁金服的通知后，您需要按照[要求](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)返回响应。

蚂蚁金服允许您在**createPaymentSession** API的_paymentNotifyUrl_ 参数中指定URL。如果每个支付的URL相同，您也可以在蚂蚁金服控制台中进行配置。

以下是一个通知请求的示例：
```json
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
```
以下示例代码展示了如何验证通知的签名并做出响应：
```java
@RequestMapping(path = "/payResult", method = RequestMethod.POST)
public ResponseEntity<AlipayResponse> paymentNotifyProcessor(HttpServletRequest request,
@RequestBody String body) {
// 从请求头中获取所需参数。
String requestTime = request.getHeader("request-time");
String clientId = request.getHeader("client-id");
String rawSignature = request.getHeader("signature");
String signature = "";  
// 从原始签名中获取有效部分
if(rawSignature==null||rawSignature.isEmpty()){
throw new RuntimeException("empty notify signature");
}else {
String[] parts = rawSignature.split("signature=");
if (parts.length > 1) {
signature = parts[1];
}
}  
// 验证支付结果通知的签名
boolean verifyResult = SignatureTool.verify(request.getMethod(), request.getRequestURI(),
clientId, requestTime, body, signature,
ALIPAY_PUBLIC_KEY);
if (!verifyResult) {
throw new RuntimeException("Invalid notify signature");
}  
// 根据通知结果更新记录状态
// 响应服务器，表示接受通知
Result result = new Result("SUCCESS", "success", ResultStatusType.S);
AlipayResponse response = new AlipayResponse();
response.setResult(result);
return ResponseEntity.ok().body(response);
}
```
#### 常见问题解答  
##### 何时会发送通知？  
这取决于支付是否完成：  
*   如果支付成功完成，蚂蚁金服通常会在3到5秒内发送异步通知。对于像柜台支付（OTC）这样的支付方式，通知可能需要更长的时间。
*   如果支付未完成，蚂蚁金服需要先关闭订单，然后才会发送异步通知。不同支付方式关闭订单所需的时间会有所不同，通常默认为14分钟。

##### 通知会被重新发送吗？  
如果您收到蚂蚁金服的异步通知，您需要按照[示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)的格式返回响应。如果您未按要求响应异步通知，或者由于网络原因通知未送达，通知将在24小时内自动重试发送，最多重试8次或直到收到正确响应为止。发送间隔为：0分钟，2分钟，10分钟，10分钟，1小时，2小时，6小时和15小时。

##### 是否需要在响应中添加数字签名？  
如果您收到蚂蚁金服的异步通知，您需要按照[示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)的格式返回响应，但不需要在响应中添加数字签名。

##### 如何理解以下关键字段的含义？  
*   _result_：订单的支付结果。
*   _paymentRequestId_：商家生成的用于查询、取消和对账的支付请求ID。
*   _paymentId_：蚂蚁金服生成的用于退款和对账的支付订单ID。
*   _paymentAmount_：如有金额对账需求，可以使用此字段。
### 查询支付结果  
您可以调用**inquiryPayment** API 来查询订单的支付结果。  
| **参数名称** | **必需** | **描述** |
| --- | --- | --- |
| paymentRequestId | 是 | 商户生成的支付请求ID。 |

请注意，以上并非所有参数，完整参数集及特定支付方式的额外要求请参考[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API 文档。  
以下示例代码展示了如何调用**inquiryPayment** API：  
```java
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
    // 处理错误情况
}
```
以下是一个请求消息的示例：  
```json
{
  "paymentRequestId": "paymentRequestId01"
}
```
以下是一个响应消息的示例：  
```json
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
```
#### 常见问题解答  
##### 如何理解以下关键字段的含义？  
*   _result_：API调用的结果。它仅表示**inquiryPayment** API调用的结果。订单结果应根据_paymentStatus_来确定。`SUCCESS`和`FAIL`表示最终结果，而`PROCESSING`表示交易仍在进行中。
*   _paymentAmount_：金额验证。如果有金额验证需求，可以使用此字段。  
##### 应该多久发起一次查询？  
建议以2秒的间隔进行轮询查询，直到获取到最终的支付结果或收到异步支付通知为止。  
步骤4：获取扣款结果（服务器端）
-----------------------------------------
在买家完成扣款或扣款超时后，蚂蚁金服会通过服务器交互将相应的扣款结果发送给您，您可以通过以下方式之一获取扣款结果：  
*   接收异步通知
*   查询结果
### **接收异步通知**  
当扣款达到成功或失败的最终状态时，Antom会通过[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API，向在**createPaymentSession** API中指定的_paymentNotifyUrl_ 发送异步通知。收到Antom的通知后，您需要按照[要求](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)返回响应。

Antom允许您在**createPaymentSession** API的_paymentNotifyUrl_ 参数中指定URL。如果每个支付的URL相同，您也可以在Antom控制台中进行配置。

以下是一个成功的扣款示例：

```json
{
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
```

以下是一个失败的扣款示例：

```json
{
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
```

以下示例代码展示了如何验证通知的签名并做出响应：

```java
@RequestMapping(path = "/captureResult", method = RequestMethod.POST)
public ResponseEntity<AlipayResponse> captureNotifyProcessor(HttpServletRequest request,
    @RequestBody String body) {
  // 从请求头中获取所需参数。
  String requestTime = request.getHeader("request-time");
  String clientId = request.getHeader("client-id");
  String rawSignature = request.getHeader("signature");
  String signature = "";  

  // 从原始签名中获取有效部分
  if (rawSignature == null || rawSignature.isEmpty()) {
    throw new RuntimeException("empty notify signature");
  } else {
    String[] parts = rawSignature.split("signature=");
    if (parts.length > 1) {
      signature = parts[1];
    }
  }  

  // 验证支付结果通知的签名
  boolean verifyResult = SignatureTool.verify(request.getMethod(), request.getRequestURI(),
      clientId, requestTime, body, signature,
      ALIPAY_PUBLIC_KEY);
  if (!verifyResult) {
    throw new RuntimeException("Invalid notify signature");
  }  

  // 根据通知结果更新记录状态
  // 响应服务器我们已接受通知
  Result result = new Result("SUCCESS", "success", ResultStatusType.S);
  AlipayResponse response = new AlipayResponse();
  response.setResult(result);
  return ResponseEntity.ok().body(response);
}
```

#### 常见问题

##### 何时发送通知？
这取决于支付是否完成：
*   如果支付成功完成，Antom通常会在3到5秒内发送异步通知。对于像柜台支付（OTC）这样的支付方式，通知可能需要更长时间。
*   如果支付未完成，Antom需要先关闭订单，然后才发送异步通知。不同支付方式关闭订单所需的时间会有所不同，通常默认为14分钟。

##### 通知会重新发送吗？
如果您收到Antom的异步通知，您需要按照[示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)的格式返回响应。如果您未按要求响应异步通知，或者由于网络原因通知未送达，通知将在24小时内自动重新发送，最多可重试8次，直到收到正确的响应为止。发送间隔为：0分钟，2分钟，10分钟，10分钟，1小时，2小时，6小时和15小时。

##### 是否需要在响应中添加数字签名？
如果您收到Antom的异步通知，您需要按照[示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)的格式返回响应，但不需要在响应中添加数字签名。

##### 如何理解以下关键字段的含义？
*   _result_：表示订单的扣款结果。
*   _notifyType_：notifyType 的值为 `CAPTURE_RESULT`。
*   _paymentRequestId_：您生成的支付请求号，用于查询、取消和对账。
*   _paymentId_：Antom 生成的支付订单ID，用于退款和对账。
*   _acquirerReferenceNo_：在新加坡和香港集成卡内支付服务的商家将在通知中收到特定的收单方编号。
### **查询支付结果**

您可以调用 **inquiryPayment** API 来查询订单的支付结果。

#### 参数说明

| 参数名称 | 是否必填 | 描述 |
| --- | --- | --- |
| paymentRequestId | 是 | 商户生成的支付请求ID。 |

以上参数不完整，完整参数及某些支付方式的额外要求请参考 [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API 文档。

#### 示例代码

```java
// 初始化AlipayClient
AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG, merchantPrivateKey, alipayPublicKey);

// 创建AlipayPayQueryRequest对象
AlipayPayQueryRequest alipayPayQueryRequest = new AlipayPayQueryRequest();
alipayPayQueryRequest.setClientId(CLIENT_ID);
alipayPayQueryRequest.setPath("/ams/sandbox/api/v1/payments/inquiryPayment");
alipayPayQueryRequest.setPaymentRequestId("paymentRequestId01");

// 执行查询
try {
    AlipayPayQueryResponse alipayPayQueryResponse = defaultAlipayClient.execute(alipayPayQueryRequest);
} catch (AlipayApiException e) {
    String errorMsg = e.getMessage();
    // 处理错误情况
}
```

#### 捕获状态值

API响应中的 `_transactions` 字段表示捕获状态：

| 参数名称 | 描述 |
| --- | --- |
| transactions.transactionType | 值为 `CAPTURE`，表示捕获状态。 |
| transactions.transactionStatus | 捕获状态。 |
| transactions.transactionResult | 捕获结果。 |

#### 示例响应

- 成功捕获：

```json
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
```

- 失败捕获：

```json
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
```

- 处理中捕获：

```json
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
```

#### 常见问题

- **如何理解关键字段的含义？**
  - `result`：API调用的结果，仅表示**inquiryPayment** API的调用结果。订单状态应基于`paymentStatus`来确定。`SUCCESS`和`FAIL`表示最终结果，`PROCESSING`表示交易仍在进行中。
  - `paymentAmount`：金额验证。如有需要，可以使用此字段进行验证。

- **应多频繁发起查询？**
  建议每2秒轮询一次，直到获取最终支付结果或收到异步支付通知。

#### 示例代码
```java
// 示例代码省略
```

#### 事件代码
```java
// 示例代码省略
```

#### 常见问题
- **如何理解以下关键字段的含义？**
  - 类型：状态代码 - 由组件运行时生命周期的`onEventCallback`返回。
  - 类型：错误代码 - 由组件初始化阶段的`onEventCallback`或`onError`返回。

#### 示例代码
```java
// 示例代码省略
```

#### 事件代码
```java
// 示例代码省略
```

**@2024 阿里巴巴集团 [法律信息](https://global.alipay.com/docs/ac/platform/membership)**

#### 这个页面是否有帮助？

#### 本页面内容
- [用户体验](#fc442)
- [支付流程](#eLZVd)
- [集成步骤](#QLFGi)
- [步骤1：创建支付会话](#zhBSk)
- [安装API库](#d3kyo)
- [初始化请求实例](#WLui0)
- [创建支付会话](#fzPO2)
- [调用createPaymentSession API的示例代码](#3L7zQ)
- [常见问题](#UGjGp)
- [请求中可以使用中文吗？](#asEuc)
- [如何设置支付结果通知地址？](#KQLhk)
- [步骤2：创建并调用SDK](#xhgER)
- [安装](#Ddkes)
- [初始化SDK](#KQO5X)
- [调用SDK](#OXd8h)
- [显示支付结果](#s5Wpy)
- [步骤3：获取支付结果](#CH9lr)
- [接收异步通知](#MfdWT)
- [常见问题](#V1F5v)
- [查询结果](#UpOeG)
- [常见问题](#tkpZO)
- [步骤4：获取捕获结果](#lSBz0)
- [接收异步通知](#nnrAd)
- [常见问题](#Bdbew)
- [查询结果](#NrYhL)
- [捕获状态的值](#q3e0A)
- [常见问题](#Waqa6)
- [示例代码](#BJbEu)
- [事件代码](#blzVa)
```