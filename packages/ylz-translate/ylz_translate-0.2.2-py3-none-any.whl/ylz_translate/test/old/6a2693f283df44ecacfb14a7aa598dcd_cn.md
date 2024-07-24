[![支付宝——中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![支付宝——中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)  
[返回首页](../../)  
结账支付  
[概览](/docs/ac/cashierpay/overview)  
接受支付  
SDK 集成  
[APM 支付（Web/WAP）](/docs/ac/cashierpay/apm_ww)  
[APM 支付（Android）](/docs/ac/cashierpay/apm_android)  
[APM 支付（iOS）](/docs/ac/cashierpay/apm_ios)  
[卡片支付（Web/WAP）](/docs/ac/cashierpay/wwcard)  
[卡片支付（Android）](/docs/ac/cashierpay/adcard)  
[卡片支付（iOS）](/docs/ac/cashierpay/ioscard)  
API 集成  
支付后  
支付方式  
其他资源  
高级功能  
[预前台解决方案API](/docs/ac/cashierpay/prefront)  
[先买后付API](/docs/ac/cashierpay/bnpl)  
[卡存储API](/docs/ac/cashierpay/cv)  
[卡存储SDK](/docs/ac/cashierpay/cvsdk)  
[卡支付功能API/SDK](/docs/ac/cashierpay/mf?pageVersion=7)  
APM 支付（Web/WAP）
======================  
2024-05-11 10:13  
Antom SDK 是一个预构建的 UI 组件，简化了集成 Antom 支付服务的过程。该组件提供了一种简单快捷的方式，以集成 Antom 支持的所有支付方式，包括信用卡、数字钱包、银行转账、在线银行等。  
SDK 组件可以自动适应买家的设备和位置，根据支付方式的特性执行信息收集、重定向、应用切换、显示二维码等任务。您可以在您的网站或应用上轻松提供全面的支付解决方案，节省构建每个支付接口和流程所需的时间和资源。  
用户体验
===============  
以下图表显示了在购物网站或移动网页应用上支付的用户流程：  
Web  
WAP  
Web 用户体验
-------------------  
![image (16).png](https://global.alipay.com/16)  
WAP 用户体验
-------------------  
![image.png](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "image.png")  
支付流程
============  
对于每种支付方式，支付流程由以下步骤组成：  
![333.webp](https://ac.alipay.com/storage/2020/5/11/793a3d8d-5270-405b-9362-e6a670b9c842.png "333.webp")  
1. **买家到达结账页面。**
2. **创建** [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) **请求**
   买家选择支付方式并提交订单后，您可以调用 [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) 接口获取支付会话。
3. **调用客户端 SDK**
   在客户端，通过支付会话调用 SDK。SDK 将根据支付方式的特性处理信息收集、重定向、应用调用、二维码显示、验证等流程。
4. **获取支付结果**
   使用以下两种方法之一获取支付结果：  
   * 异步通知：在 [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) 接口中设置 _paymentNotifyUrl_ 以指定接收异步通知的地址。支付成功或过期时，Antom 将使用 [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) 向您发送异步通知。
   * 同步查询：调用 [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) 接口检查支付状态。  
集成步骤
=================  
按照以下步骤开始集成：  
1. 创建支付会话
2. 创建并调用 SDK
3. 获取支付结果  
步骤 1：创建支付会话 服务器端
--------------------------------------------  
当买家选择由 Antom 提供的支付方式时，您需要收集支付请求 ID、订单金额、支付方式、订单描述、支付重定向 URL 和支付结果通知 URL 等关键信息，调用 **createPaymentSession** API 创建支付会话，并将支付会话返回给客户端。  
Antom 提供了多种语言的服务器端 API 库。以下代码以 Java 为例，您需要安装 Java 6 或更高版本。
### 安装API库
您可以在[GitHub](https://github.com/alipay/global-open-sdk-java)上找到最新版本。  
复制以下依赖项到您的项目中：

```xml
<dependency>
    <groupId>com.alipay.global.sdk</groupId>
    <artifactId>global-open-sdk-java</artifactId>
    <version>2.0.21</version>
</dependency>
```

确保将此代码段添加到您的Maven `pom.xml` 文件中，以便于引入蚂蚁金服的全局开放SDK。
### 初始化请求实例  
创建一个单例资源来向Antom发起请求。  
复制  
```java
import com.alipay.global.api.AlipayClient;
import com.alipay.global.api.DefaultAlipayClient;  

String merchantPrivateKey = "你的私钥";
String alipayPublicKey = "支付宝公钥";
AlipayClient defaultAlipayClient = new DefaultAlipayClient(EndPointConstants.SG,
    merchantPrivateKey, alipayPublicKey);
```

这段代码是Java语言，用于初始化一个`AlipayClient`实例，这是与蚂蚁金服接口交互的基础。`YOUR PRIVATE KEY`和`ALIPAY PUBLIC KEY`需要替换为你自己的商户私钥和支付宝公钥。`EndPointConstants.SG`代表请求的Endpoint，这里可能是新加坡的服务器地址。
### 创建支付会话  
创建支付会话包括以下参数：  
| 参数名 | 是否必填 | 描述 |
| --- | --- | --- |
| _productCode_ | ✅ | 固定值为 `CASHIER_PAYMENT`。 |
| _paymentRequestId_ | ✅ | 商户生成的唯一交易标识，每次发起支付时需生成新的ID。 |
| _paymentAmount_ | ✅ | 支付金额，应设置为订单货币单位的最小单位，例如，CNY表示分，KRW表示韩元。 |
| _paymentMethod_ | ✅ | 支付方式枚举。 |
| _paymentRedirectUrl_ | ✅ | 商户的支付结果页面，根据服务器端结果，而非固定的成功页面。 |
| _order_ | ✅ | 订单信息，包括订单金额，订单ID和商户侧的订单描述。 |
| _paymentNotifyUrl_ |  | 支付结果通知地址，可以通过接口传递，也可以通过门户设置为固定值。 |
| _settlementStrategy_ |  | 支付结算货币，如果业务已签约多个结算货币，需要在接口中指定。 |

上述参数是创建支付会话的基本参数，完整的参数列表和某些支付方式的额外要求请参考[**createPaymentSession (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/session_cashier)。

#### 调用createPaymentSession API的示例代码  
以下示例代码展示了如何调用**createPaymentSession** API：

```java
AlipayPaymentSessionRequest alipayPaymentSessionRequest = new AlipayPaymentSessionRequest();
alipayPaymentSessionRequest.setClientId(CLIENT_ID);
alipayPaymentSessionRequest.setPath("/ams/sandbox/api/v1/payments/createPaymentSession");
alipayPaymentSessionRequest.setProductCode(ProductCodeType.CASHIER_PAYMENT);  
// 替换为你的paymentRequestId
alipayPaymentSessionRequest.setPaymentRequestId("paymentRequestId01");
// 设置金额
Amount amount = new Amount();
amount.setCurrency("MYR");
amount.setValue("4200");
alipayPaymentSessionRequest.setPaymentAmount(amount);  
// 设置支付方式
PaymentMethod paymentMethod = new PaymentMethod();
paymentMethod.setPaymentMethodType("ONLINEBANKING_FPX");
alipayPaymentSessionRequest.setPaymentMethod(paymentMethod);  
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
// 替换为你的重定向url
alipayPaymentSessionRequest.setPaymentRedirectUrl("https://www.yourMerchantWeb.com");
alipayPaymentSessionRequest.setPaymentNotifyUrl("https://www.yourNotifyUrl");  
AlipayPaymentSessionResponse alipayPaymentSessionResponse = null;
try {
    alipayPaymentSessionResponse = defaultAlipayClient.execute(alipayPaymentSessionRequest);
} catch (AlipayApiException e) {
    String errorMsg = e.getMessage();
    // 处理错误情况
}  
```

以下是一个请求消息的示例：

```json
{
  "paymentNotifyUrl": "https://www.yourNotifyUrl",
  "paymentRequestId": "paymentRequestId01",
  "paymentAmount": {
    "currency": "MYR",
    "value": "4200"
  },
  "productCode": "CASHIER_PAYMENT",
  "paymentRedirectUrl": "https://www.yourMerchantWeb.com",
  "paymentMethod": {
    "paymentMethodType": "ONLINEBANKING_FPX"
  },
  "order": {
    "orderAmount": {
      "currency": "MYR",
      "value": "4200"
    },
    "referenceOrderId": "referenceOrderId01",
    "orderDescription": "antom sdk test order",
    "buyer": {
      "referenceBuyerId": "yourBuyerId"
    }
  }
}
```

以下是一个响应的示例，其中包含以下参数：
*   _paymentSessionData_：需返回前端的支付会话数据。
*   _paymentSessionExpiryTime_：支付会话的过期时间。

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
### 常见问题
#### 请求中可以使用中文字符吗？
请勿在请求的字段中使用中文字符，包括 _paymentRequestId_、_referenceOrderId_、_orderDescription_ 和 _goods_，以避免与 QRIS 和 Mastercard 等不兼容的支付方式。

#### 如何设置支付结果通知地址？
Antom 会通过 [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) 推送支付结果。您可以在 **createPaymentSession** API 中通过 _paymentNotifyUrl_ 参数指定此地址。如果每个支付的通知地址相同，您也可以在 Antom 控制台中进行配置。如果您已经设置了地址并同时在 API 中设置了参数，Antom 将使用 API 中设置的地址。

### 步骤2：创建并调用 SDK 客户端
----------------------------
Antom SDK 是处理支付流程的组件。通过创建支付会话，您可以启动 SDK 来收集信息、在应用间切换以及根据 **createPaymentSession** API 中指定的支付方式显示二维码。

当买家在页面上选择支付方式后，您需要创建 SDK 并使用支付会话来启动它。
### 安装
在开始集成之前，请确保已经完成了以下环境准备：

1. 兼容性处理：为Internet Explorer和其他旧版浏览器提供相应的polyfills。我们推荐使用[Babel-preset-env](https://babeljs.io/docs/en/babel-preset-env)处理项目中的浏览器兼容性问题。
2. 建议使用以下版本的浏览器：

   - 移动浏览器：
     - iOS 11及以上版本
     - Android 5.0及以上版本
   - 电脑浏览器，推荐使用以下版本：

|       |       |       |       |       |       |
| ----- | ----- | ----- | ----- | ----- | ----- |
| ![图片](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1680143117412-8322ebf3-b84b-48d1-a696-5cc5703d1006.png "图片")<br>**Edge**<br><br>最后2个版本 | ![图片](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1680143117377-62f319d6-72e5-4555-aacd-f0efc434ef9e.png "图片")<br>**Firefox**<br><br>最后2个版本 | ![图片](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1680143118111-1392b868-4947-4d0f-941c-53d54c655c8d.png "图片")<br>**Chrome**<br><br>最后2个版本 | ![图片](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1680143118162-1fc223a0-8a35-488f-91aa-5833f5d7726a.png "图片")<br>**Safari**<br><br>最后2个版本 | ![图片](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1680143118154-fc609c28-81bf-4442-985b-fdf4d1c3554d.png "图片")<br>**Opera**<br><br>最后2个版本 | ![图片](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1680143118867-73ee0c65-fbf2-4ff3-b18e-8fa092801c30.png "图片")<br>**Electron**<br><br>最后2个版本 |

可以通过CDN或npm来集成SDK资源包。

```html
复制
<script src="https://sdk.marmot-cloud.com/package/ams-checkout/1.13.0/dist/umd/ams-checkout.min.js"></script>
复制
```

```shell
npm install @alipay/ams-checkout
```
### 初始化 SDK  
使用 `AMSCashierPayment` 创建 SDK 实例，并指定基础配置。配置对象包含以下参数：

| 参数名         | 是否必填 | 描述                                       |
| -------------- | -------- | ------------------------------------------ |
| _environment_  | ✅       | 用于传入环境信息。有效值为：<br><br>*   `sandbox`: 沙盒环境<br>*   `prod`: 生产环境     |
| _locale_        |          | 用于传入语言信息。有效值如下，根据支付方法所在地区选择传递的值。如果传递其他值，默认使用本地语言：<br><br>*   `en_US`: 英语<br>*   `pt_BR`: 葡萄牙语<br>*   `ko_KR`: 韩语<br>*   `es_ES`: 西班牙语<br>*   `ms_MY`: 马来语<br>*   `in_ID`: 印尼语<br>*   `tl_PH`: 他加禄语<br>*   `th_TH`: 泰语<br>*   `vi_VN`: 越南语<br>*   `fr_FR`: 法语<br>*   `nl_NL`: 荷兰语<br>*   `it_IT`: 意大利语<br>*   `de_DE`: 德语<br>*   `zh_CN`: 简体中文<br>*   `zh_HK`: 繁体中文 |
| _analytics_     |          | 用于配置和分析数据。包含以下值：<br><br>*   _enabled_: 可选布尔值。默认为 `true`，允许 SDK 上传和分析操作数据以提供更好的服务。如果不允许上传和分析数据，将其设为 `false`。 |
| _onLog_         |          | 一个回调方法，用于生成 SDK 执行期间的日志和 API 异常的错误信息。 |
| _onEventCallback_ |          | 当 SDK 运行时发生支付事件（如支付结果或表单提交错误）时返回特定事件代码的回调函数。更多详情请参考参考资料。 |

以下示例代码显示如何获取浏览器语言：

```javascript
let language = navigator.language || navigator.userLanguage;
language = language.replace("-", "_"); // 用 "_" 替换 "-"
```

以下示例代码显示如何实例化 SDK：

```javascript
const checkoutApp = new window.AMSCashierPayment({
  environment: "sandbox",
  locale: "en_US",
  onLog: ({code, message}) => {},
  onEventCallback: ({code, message}) => {},
});

// 从服务器请求 paymentSessionData
```

请确保在实际使用中替换 `paymentSessionData` 为实际从服务器获取的数据。
### 调用SDK  
通过实例对象的`createComponent`函数创建支付组件：

| 参数名 | 是否必填 | 描述 |
| --- | --- | --- |
| _sessionData_ | ✅ | 使用_sessionData_参数创建配置对象：将通过**createpaymentSession（结账支付）**API得到的_paymentSessionData_参数中的完整数据传递给_sessionData_参数。 |
| _appearance_ |  | 自定义外观主题配置，包含以下子参数：<br><br>*   _showLoading_: 可选。布尔类型。默认值为`true`，显示默认加载动画。如果不使用默认加载动画，需将此值设为`false`。更多细节请参照其他高级功能。 |

以下示例代码展示了如何调用`createComponent`：

```javascript
// 复制
async function create(sessionData) {
  await checkoutApp.createComponent({
    sessionData: sessionData,
    appearance: {
      showLoading: true, // 默认为true，启用默认加载样式
    }
  });
}
```

在以下情况下，调用`unmount`方法释放SDK组件资源：

*   当买家切换视图离开结账页面时，释放**createPaymentSession**中创建的组件资源。
*   当买家发起多次支付时，释放前一次**createPaymentSession**创建的组件资源。
*   当买家完成支付并设置_notRedirectAfterComplete_为`true`，在获取特定支付结果代码后释放组件资源。

```javascript
// 释放SDK组件资源
checkoutApp.unmount();
```

#### 常见问题

##### 收到`SDK_CREATEPAYMENT_PARAMETER_ERROR`时该怎么办？

若收到此事件代码，请检查传递的_sessionData_是否正确且完整。

##### 收到`SDK_PAYMENT_ERROR`或渲染视图错误时该怎么办？

收到此事件代码时，请检查网络请求。初始化接口可能存在异常，确保创建支付会话请求的环境与SDK实例化时的环境参数一致。检查支付会话创建参数是否传递正确。如果接口异常仍然存在，可联系我们进行故障排查。
### 显示支付结果  
您可以使用支付组件来处理需要重定向（异步支付）和不需要重定向（同步支付）的支付方式。  
#### 重定向支付  
某些支付方式的支付过程需要离开原始网页，跳转到机构页面完成支付，例如在线银行支付方式。在这种情况下，买家完成支付后会被重定向到您在**createPaymentSession** API 中提供的_paymentRedirectUrl_。您可以在该URL中主动查询支付结果，并向买家展示。  
#### 非重定向支付  
对于无重定向的支付，支付结果将通过`onEventCallback`函数给出。这里的支付结果仅用于前端显示，最终的订单状态以服务器端为准。  
您需要通过`onEventCallback`结果数据自定义每个支付结果的处理流程。  
以下是`onEventCallback`返回的支付结果可能的事件代码。  
| | | |
| --- | --- | --- |
| **事件代码** | **消息** | **解决方案** |
| SDK_PAYMENT_SUCCESSFUL | 支付成功。 | 建议将买家重定向到支付结果页面。 |
| SDK_PAYMENT_PROCESSING | 支付处理中。 | 建议检查`onEventCallback`结果数据中的_paymentResultCode_详情。根据提供的信息引导买家重试支付。 |
| SDK_PAYMENT_FAIL | 支付失败。 | 建议检查`onEventCallback`结果数据中的_paymentResultCode_详情。根据提供的信息引导买家重试支付。 |
| SDK_PAYMENT_CANCEL | 买家在未提交订单的情况下退出支付页面。 | 如果在有效期内，可以重新调用SDK并使用_paymentSessionData_；如果已过期，需要重新请求_paymentSessionData_。 |
| SDK_PAYMENT_ERROR | 支付状态异常。 | 建议检查`onEventCallback`结果数据中的_paymentResultCode_详情。根据提供的信息引导买家重试支付。 |

以下示例代码展示了如何处理`onEventCallback`：

```javascript
function onEventCallback({ code, result }) {
  switch (code) {
    case 'SDK_PAYMENT_SUCCESSFUL':
      // 支付成功。将买家重定向到支付结果页面。
      break;
    case 'SDK_PAYMENT_PROCESSING':
      console.log('检查支付结果数据', result);
      // 支付处理中。根据提供的信息引导买家重试支付。
      break;
    case 'SDK_PAYMENT_FAIL':
      console.log('检查支付结果数据', result);
      // 支付失败。根据提供的信息引导买家重试支付。
      break;
    case 'SDK_PAYMENT_CANCEL':
      // 引导买家重试支付。
      break;
    case 'SDK_PAYMENT_ERROR':
      console.log('检查支付结果数据', result);
      // 支付状态异常。根据提供的信息引导买家重试支付。
      break;
    default:
      break;
  }
}
```

### 步骤3：服务器端获取支付结果  
---------------------------
在买家完成支付或支付超时后，蚂蚁金服会通过服务器交互将相应的支付结果发送给您，您可以采用以下方法之一获取支付结果：  
*   接收异步通知
*   查询结果
### **接收异步通知**  
当支付状态最终成功或失败时，蚂蚁金服会通过 [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API 将异步通知发送到在 **createPaymentSession** API 中指定的 _paymentNotifyUrl_。收到蚂蚁金服的通知后，需要按照 [要求](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) 指定的格式返回响应。

蚂蚁金服允许您在 **createPaymentSession** API 的 _paymentNotifyUrl_ 参数中指定 URL。如果每个支付的 URL 相同，您也可以在蚂蚁金服控制台中配置。

以下是一个示例的通知请求：
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
    "currency": "MYR"
  },
  "paymentCreateTime": "2020-01-01T12:01:00+08:30",
  "paymentTime": "2020-01-01T12:01:01+08:30"
}
```
以下示例代码展示了如何验证通知的签名并作出响应：
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
  // 告诉服务器我们接受了通知
  Result result = new Result("SUCCESS", "success", ResultStatusType.S);
  AlipayResponse response = new AlipayResponse();
  response.setResult(result);
  return ResponseEntity.ok().body(response);
}
```
#### 常见问题
##### 何时发送通知？
这取决于支付是否完成：
*   如果支付成功完成，蚂蚁金服通常会在3到5秒内发送异步通知。对于如OTC等某些支付方式，通知可能需要更长的时间。
*   如果支付未完成，蚂蚁金服需要先关闭订单，然后才发送异步通知。不同支付方式关闭订单所需的时间可能不同，通常默认为14分钟。

##### 通知会被重新发送吗？
如果您收到蚂蚁金服的异步通知，需要按照 [示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) 的格式返回响应。如果您未按要求响应异步通知，或者由于网络原因通知未送达，通知将在24小时内自动重试，最多重试8次或直到收到正确响应为止。重试间隔为：0分钟，2分钟，10分钟，10分钟，1小时，2小时，6小时和15小时。

##### 是否需要在响应中添加数字签名？
如果您收到蚂蚁金服的异步通知，需要按照 [示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification) 的格式返回响应，但不需要在响应中添加数字签名。

##### 如何理解以下关键字段的含义？
*   _result_：订单的支付结果。
*   _paymentRequestId_：商家生成的用于查询、取消和对账的支付请求ID。
*   _paymentId_：蚂蚁金服生成的用于退款和对账的支付订单ID。
*   _paymentAmount_：如果有金额对账需求，可以使用这个字段。
### **查询结果**
您可以调用**inquiryPayment** API 来查询订单的结果。  
| 参数名 | 是否必填 | 描述 |
| --- | --- | --- |
| _paymentRequestId_ |  | 商家生成的支付请求ID。 |

参数不完整，完整参数请参考[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API 文档，以及某些支付方式的额外要求。
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
    "value": "500",
    "currency": "USD"
  },
  "paymentCreateTime": "2019-06-01T12:01:01+08:30",
  "paymentTime": "2019-06-01T12:01:01+08:30",
  "transactions": null
}
```
#### 常见问题
##### 如何理解以下关键字段的含义？
*   _result_：API调用的结果。仅表示**inquiryPayment** API调用的结果。订单结果应根据_paymentStatus_确定。`SUCCESS`和`FAIL`表示最终结果，`PROCESSING`表示交易仍在进行中。
*   _paymentAmount_：金额验证。如果有金额验证需求，可使用此字段。

##### 应该多频繁发起查询？
建议每2秒轮询一次，直到获取到最终支付结果或收到异步支付通知。

### 示例代码
#### 前端完整示例代码
```javascript
// 步骤1：初始化SDK并处理回调事件
const onEventCallback = function({ code, result }) {
  switch (code) {
    case 'SDK_PAYMENT_SUCCESSFUL':
      // 支付成功。将买家重定向到支付结果页面。
      break;
    case 'SDK_PAYMENT_PROCESSING':
      console.log('检查支付结果数据', result);
      // 支付正在处理。根据提供的信息引导买家重试支付。
      break;
    case 'SDK_PAYMENT_FAIL':
      console.log('检查支付结果数据', result);
      // 支付失败。根据提供的信息引导买家重试支付。
      break;
    case 'SDK_PAYMENT_CANCEL':
      // 引导买家重试支付。
      break;
    case 'SDK_PAYMENT_ERROR':
      console.log('检查支付结果数据', result);
      // 支付状态异常。根据提供的信息引导买家重试支付。
      break;
    default:
      break;
  }
}
const checkoutApp = new window.AMSCashierPayment({
  environment: "sandbox",
  locale: "en_US",
  onLog: ({code, message}) => {},
  onEventCallback: onEventCallback,
});

// 处理支付按钮事件。
document
  .querySelector("#your form id")
  .addEventListener("submit", handleSubmit);

async function handleSubmit() {
  // 步骤2：服务器调用createPaymentSession API获取paymentSessionData。
  async function getPaymentSessionData() {
    const url = "填入服务器地址";
    const config = {
      // 填入请求配置。
    };
    const response = await fetch(url, config);
    // 从响应中获取paymentSessionData参数的值。
    const { paymentSessionData } = await response.json();
    return paymentSessionData;
  }
  const paymentSessionData = await getPaymentSessionData();  

  // 步骤3：创建渲染组件。
  await checkoutApp.createComponent({
    sessionData: paymentSessionData,
    appearance:{
      showLoading: true, // 默认设为true，启用默认加载样式。
    },
  });
}
```
#### 事件代码
您可能遇到两种类型的事件代码：
*   状态码：在组件运行时生命周期中由`onEventCallback`返回。
*   错误码：在组件初始化阶段由`onEventCallback`或`onError`返回。

| 类型 | 代码 | 描述 | 进一步操作 |
| --- | --- | --- | --- |
| 状态码 | SDK\_START\_OF\_LOADING | 支付组件创建时启动加载动画。 | 无需进一步操作。 |
| SDK\_END\_OF\_LOADING | 支付组件创建时加载动画结束。 | 无需进一步操作。 |
| 错误码 | SDK\_INTERNAL\_ERROR | SDK内部错误。 | 联系Antom技术支持解决问题。 |
| SDK\_CREATEPAYMENT\_PARAMETER\_ERROR | 传递给`AMSCashierPayment`方法的参数不正确。 | 确保参数正确传递并发送新请求。 |
| SDK\_INIT\_PARAMETER\_ERROR | 传递给`createComponent`方法的参数不正确。 | 确保参数正确传递并发送新请求。 |
| SDK\_CREATECOMPONENT\_ERROR | 调用`createComponent`方法时发生异常。 | 联系Antom技术支持解决问题。 |
| SDK\_CALL\_URL\_ERROR | 支付方法客户端撤销失败。 | 联系Antom技术支持解决问题。 |

![](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

## 本页内容
[用户体验](#BkD7T "用户体验")  
[支付流程](#rRtMT "支付流程")  
[集成步骤](#kZlC9 "集成步骤")  
[步骤1：创建支付会话](#zhBSk "步骤1：创建支付会话")  
[安装API库](#d3kyo "安装API库")  
[初始化请求实例](#WLui0 "初始化请求实例")  
[创建支付会话](#Cwfah "创建支付会话")  
[调用createPaymentSession API的示例代码](#3L7zQ "调用createPaymentSession API的示例代码")  
[常见问题](#UGjGp "常见问题")  
[请求中可以使用中文字符吗？](#asEuc "请求中可以使用中文字符吗？")  
[如何设置支付结果通知地址？](#KQLhk "如何设置支付结果通知地址？")  
[步骤2：创建并调用SDK](#oDHQJ "步骤2：创建并调用SDK")  
[安装](#JmurT "安装")  
[初始化SDK](#KQO5X "初始化SDK")  
[调用SDK](#iVDpG "调用SDK")  
[常见问题](#ARgvG "常见问题")  
[显示支付结果](#Go6NO "显示支付结果")  
[重定向支付](#6ubRS "重定向支付")  
[非重定向支付](#NEgUb "非重定向支付")  
[步骤3：获取支付结果](#SnQk7 "步骤3：获取支付结果")  
[接收异步通知](#WDV7j "接收异步通知")  
[常见问题](#V1F5v "常见问题")  
[查询结果](#wlAb8 "查询结果")  
[常见问题](#tkpZO "常见问题")  
[示例代码](#xjYO0 "示例代码")  
[事件代码](#ZedB5 "事件代码")