蚂蚁金服支付（Web/WAP）| 结账支付 | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fcashierpay%2Fapm_ww)  
[返回首页](../../)

结账支付
[概览](/docs/ac/cashierpay/overview)  
接收支付  
SDK 集成  
[APM 支付（Web/WAP）](/docs/ac/cashierpay/apm_ww)  
[APM 支付（Android）](/docs/ac/cashierpay/apm_android)  
[APM 支付（iOS）](/docs/ac/cashierpay/apm_ios)  
[卡支付（Web/WAP）](/docs/ac/cashierpay/wwcard)  
[卡支付（Android）](/docs/ac/cashierpay/adcard)  
[卡支付（iOS）](/docs/ac/cashierpay/ioscard)  
仅API集成  
支付后  
支付方式  
其他资源  
高级功能  
[预前端解决方案API](/docs/ac/cashierpay/prefront)  
[先买后付API](/docs/ac/cashierpay/bnpl)  
[卡存储API](/docs/ac/cashierpay/cv)  
[卡存储SDK](/docs/ac/cashierpay/cvsdk)  
[卡支付功能API/SDK](/docs/ac/cashierpay/mf)  
APM 支付（Web/WAP）
======================

2024-05-11 10:13

Antom SDK 是一个预构建的UI组件，简化了集成Antom支付服务的过程。这个组件提供了一种简单快捷的方式来集成Antom支持的所有支付方式，包括信用卡、数字钱包、银行转账、在线银行等。
SDK组件能够自动适应买家的设备和位置，根据支付方式的特性执行信息收集、重定向、应用切换、显示二维码等任务。这样，您就可以在您的网站或应用上轻松提供全面的支付解决方案，节省构建每个支付界面和流程所需的时间和资源。

用户体验
==========

以下是用户在购物网站或移动网页应用上支付的流程：

Web
---

![图片3: image (16).png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1713406093717-c0e605ea-4e7c-4c63-92fb-13d7ce4718a1.png)

WAP
---

![图片4: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1713348410211-687f02e0-6035-4cc1-856a-02ef02fbf8b2.png)

支付流程
==========

对于每种支付方式，支付流程包括以下步骤：

![图片5: 333.webp](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1713522435189-a40f3909-9585-45cc-a17e-11ed25fe8416.webp)

1.  **买家到达结账页面。**
2.  **创建** [**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier) **请求**
   买家选择支付方式并提交订单后，您可以通过调用[**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier)接口获取支付会话。
3.  **调用客户端SDK**
   在客户端，通过支付会话调用SDK。SDK将根据支付方式的特性处理信息收集、重定向、应用调用、二维码显示、验证等流程。
4.  **获取支付结果**
   通过以下两种方法之一获取支付结果：
异步通知：在[**createPaymentSession**](https://global.alipay.com/docs/ac/ams/session_cashier)接口中指定_paymentNotifyUrl_，设置接收异步通知的地址。当支付成功或超时时，Antom会使用[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online)向您发送异步通知。

同步查询：调用[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online)接口来查询支付状态。

集成步骤
==========

1.  创建支付会话
2.  创建并调用SDK
3.  获取支付结果

步骤1：创建支付会话（服务器端）
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

这段代码是用于Maven项目的依赖配置，将允许您在Java项目中集成蚂蚁金服的全球开放SDK。
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

这里的代码片段是在Java中初始化一个用于与Antom（可能是蚂蚁金服的某个服务）交互的请求客户端。`DefaultAlipayClient`是客户端的实现类，它需要商户的私钥(`merchantPrivateKey`)和支付宝的公钥(`alipayPublicKey`)作为参数。`EndPointConstants.SG`可能代表服务的端点地址。
### 创建支付会话  
创建支付会话包括以下参数：  
| **参数名** | **是否必填** | **描述** |
| --- | --- | --- |
| *productCode* | ✅ | 值固定为 `CASHIER_PAYMENT`。 |
| *paymentRequestId* | ✅ | 商家生成的唯一ID，每次发起支付时需新生成一个ID。 |
| *paymentAmount* | ✅ | 支付金额，应根据订单货币的最小单位设置，例如CNY表示分，KRW表示元。 |
| *paymentMethod* | ✅ | 支付方式枚举 |
| *paymentRedirectUrl* | ✅ | 商家的支付结果页面，根据服务器端结果，不是固定的成功页面。 |
| *order* | ✅ | 订单信息，包括订单金额、订单ID和商家侧的订单描述。 |
| *paymentNotifyUrl* |  | 支付结果通知地址，可通过接口传入或通过门户设置为固定值。 |
| *settlementStrategy* |  | 支付的结算货币，如果业务已签约多个结算货币，需要在接口中指定。 |  
以上参数是创建支付会话的基本参数，完整的参数和某些支付方式的额外要求请参考[**createPaymentSession（结账支付）**](https://global.alipay.com/docs/ac/ams/session_cashier)**。**  
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
```

请注意，这里的代码示例是基于Java的，并且`CLIENT_ID`需要替换为实际的客户端ID。实际使用时，还需要设置其他参数，如`paymentMethod`、`order`、`paymentRedirectUrl`等，具体取决于您的业务需求。
金额对象 = new 金额对象();
金额对象.set货币("MYR");
金额对象.setValue("4200");
支付宝支付会话请求.set支付金额(金额对象);  
// 设置支付方式
支付方式 = new 支付方式();
支付方式.set支付方式类型("ONLINEBANKING_FPX");
支付宝支付会话请求.set支付方式(支付方式);  
// 设置订单信息
订单 = new 订单();
订单.set参考订单号("referenceOrderId01");
订单.set订单描述("antom sdk 测试订单");
订单.set订单金额(金额对象);
买家 = new 买家();
买家.set参考买家号("yourBuyerId");
订单.set买家(买家);
订单.set订单金额(金额对象);
支付宝支付会话请求.set订单(订单);  
// 替换为你的重定向URL
支付宝支付会话请求.set支付重定向URL("https://www.yourMerchantWeb.com");
支付宝支付会话请求.set支付通知URL("https://www.yourNotifyUrl");  
支付宝支付会话响应 = null;
try {
支付宝支付会话响应 = 默认支付宝客户端.execute(支付宝支付会话请求);
} catch (支付宝Api异常 e) {
字符串 错误信息 = e.getMessage();
// 处理错误情况
}  

以下代码展示了请求消息的示例:  
复制  
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
"orderDescription": "antom sdk 测试订单",
"buyer": {
"referenceBuyerId": "yourBuyerId"
}
}
}  

以下代码展示了响应的示例，其中包含以下参数:  
*   _paymentSessionData_: 需要返回给前端的支付会话数据
*   _paymentSessionExpiryTime_: 支付会话的过期时间。  
复制  
{
"paymentSessionData": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Kvvmsdk+akdLvoShW5avHX8e8J15P8uNVEf/PcCMyXg==&&SG&&111",
"paymentSessionExpiryTime": "2023年4月6日03:28:49 UTC",
"paymentSessionId": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Ikyj9FPVUOpv+DjiIZqMe",
"result": {
"resultCode": "成功",
"resultMessage": "操作成功。",
"resultStatus": "S"
}
}

这段Markdown格式的文档翻译成中文如下：

"支付会话数据": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Kvvmsdk+akdLvoShW5avHX8e8J15P8uNVEf/PcCMyXg==&&SG&&111",
"支付会话过期时间": "2023年4月6日03:28:49协调世界时",
"支付会话ID": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Ikyj9FPVUOpv+DjiIZqMe",
"结果": {
"结果代码": "成功",
"结果信息": "操作成功。",
"结果状态": "S"
}
}
### 常见问题解答  
#### 请求中可以使用中文字符吗？  
请勿在请求中的字段，包括`paymentRequestId`、`referenceOrderId`、`orderDescription`和`goods`使用中文字符，以避免与QRIS和Mastercard等不兼容的支付方式。  
#### 如何设置支付结果通知地址？  
Antom会通过[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online)接口发送支付结果。您可以在`createPaymentSession` API中通过`paymentNotifyUrl`参数指定此地址。如果每个支付的通知地址相同，您也可以在Antom控制台上进行配置。如果您同时在控制台配置了地址并在API中设置了参数，Antom将使用API中设置的地址。  
步骤2：创建并调用SDK客户端
---------------------------------------------  
Antom SDK是一个用于处理支付流程的组件。通过创建支付会话，您可以初始化SDK以收集信息、在应用间切换以及根据`createPaymentSession` API中指定的支付方式显示二维码。  
在买家在页面上选择支付方式后，您需要创建SDK并使用支付会话进行初始化。
### 安装

在开始集成前，请确保您已完成以下环境准备：

1. **兼容性处理**：为Internet Explorer和其他旧版浏览器提供相应的polyfills。我们建议您在构建项目时使用[Babel-preset-env](https://babeljs.io/docs/en/babel-preset-env)来解决浏览器兼容性问题。

2. **推荐的浏览器版本**：
   - **移动浏览器**：
     - iOS：11及以上版本
     - Android：5.0及以上版本
   - **桌面浏览器**，推荐以下版本：
     | ![Edge](http://godban.github.io/browsers-support-badges/)**Edge** 最后2个版本 | ![Firefox](http://godban.github.io/browsers-support-badges/)**Firefox** 最后2个版本 | ![Chrome](http://godban.github.io/browsers-support-badges/)**Chrome** 最后2个版本 | ![Safari](http://godban.github.io/browsers-support-badges/)**Safari** 最后2个版本 | ![Opera](http://godban.github.io/browsers-support-badges/)**Opera** 最后2个版本 | ![Electron](http://godban.github.io/browsers-support-badges/)**Electron** 最后2个版本 |
     | --- | --- | --- | --- | --- | --- |

您可以通过CDN或npm来集成SDK资源包。

```html
<!-- 通过CDN引入 -->
<script src="https://sdk.marmot-cloud.com/package/ams-checkout/1.13.0/dist/umd/ams-checkout.min.js"></script>
```

```bash
# 通过npm安装
npm install @alipay/ams-checkout
```
### 初始化 SDK  
使用 `AMSCashierPayment` 创建 SDK 实例，并指定基础配置。配置对象包含以下参数：

| **参数名称** | **是否必需** | **描述** |
| --- | --- | --- |
| *environment* | ✅ | 用于传递环境信息。有效值为：* `sandbox`：沙盒环境 * `prod`：生产环境 |
| *locale* |  | 用于传递语言信息。有效值如下，根据支付方法所在地区选择传递的值。如果传递其他值，默认使用本地语言：* `en_US`：英语 * `pt_BR`：葡萄牙语 * `ko_KR`：韩语 * `es_ES`：西班牙语 * `ms_MY`：马来语 * `in_ID`：印度尼西亚语 * `tl_PH`：他加禄语 * `th_TH`：泰语 * `vi_VN`：越南语 * `fr_FR`：法语 * `nl_NL`：荷兰语 * `it_IT`：意大利语 * `de_DE`：德语 * `zh_CN`：简体中文 * `zh_HK`：繁体中文 |
| *analytics* |  | 用于配置和分析数据。包含以下值：* *enabled*：可选布尔值，默认为 `true`，表示允许 SDK 上传和分析操作数据以提供更好的服务。如果不允许上传和分析数据，将其设置为 `false`。 |
| *onLog* |  | 一个回调方法，用于生成 SDK 执行期间的日志和 API 异常的错误信息。 |
| *onEventCallback* |  | 当 SDK 运行时发生支付事件（如支付结果或表单提交错误）时返回特定事件代码的回调函数。有关详细信息，请参阅参考资料。 |

以下示例代码展示了如何获取浏览器语言：

```javascript
let language = navigator.language || navigator.userLanguage;
language = language.replace("-", "_"); // 将 "-" 替换为 "_" 
```

以下示例代码展示了如何实例化 SDK：

```javascript
const checkoutApp = new window.AMSCashierPayment({
  // 配置参数
  environment: 'sandbox', // 例如：'sandbox' 或 'prod'
  locale: 'en_US', // 例如：'en_US' 或其他语言代码
  analytics: {
    enabled: true // 可选，是否开启数据分析，默认为 true
  },
  onLog: function(log) {
    // 处理日志回调
  },
  onEventCallback: function(eventCode, eventData) {
    // 处理事件回调
  }
});
```

请注意，实际代码中需要根据您的具体需求和环境设置参数。
环境： "沙箱",
区域设置： "en_US",
日志回调： ({code, message}) => {},
事件回调： ({code, message}) => {},
});

// 向服务器请求获取支付会话数据
### 调用SDK  
使用实例对象中的`createComponent`函数创建支付组件：  
| **参数名** | **必填** | **描述** |
| --- | --- | --- |
| *sessionData* | ✅ | 使用*sessionData*参数创建配置对象：将通过**createpaymentSession（结账支付）**API获取的*paymentSessionData*参数中的完整数据传递给*sessionData*参数。 |
| *appearance* |  | 自定义外观主题配置，包含以下子参数：* *showLoading*：可选。布尔类型。默认值为`true`，显示默认加载动画。如果不使用默认加载动画，需将此值设为`false`。更多详情参见其他高级功能。 |  

以下示例代码展示了如何调用`createComponent`：  
```javascript
async function create(sessionData) {
  await checkoutApp.createComponent({
    sessionData: sessionData,
    appearance: {
      showLoading: true, // 默认为true，启用默认加载样式
    }
  });
}
```
在以下情况下调用`unmount`方法释放SDK组件资源：  
*   当买家切换视图离开结账页面时，释放**createPaymentSession**中创建的组件资源。
*   当买家发起多次支付时，释放之前**createPaymentSession**中创建的组件资源。
*   当买家完成支付并设置_notRedirectAfterComplete_为true时，在获取特定支付结果代码后释放组件资源。  

```javascript
// 释放SDK组件资源
checkoutApp.unmount();
```
#### 常见问题  
##### 收到`SDK_CREATEPAYMENT_PARAMETER_ERROR`时应如何处理？  
收到此事件代码时，请检查传递的sessionData是否正确且完整。  
##### 收到`SDK_PAYMENT_ERROR`或渲染视图错误时应如何处理？
当收到此事件代码时，请检查网络请求。可能在初始化接口中存在异常，您需要确保创建支付会话请求的环境与所实例化SDK的环境参数一致。请确认支付会话创建参数是否正确传递。如果接口异常仍然存在，您可以联系我们的技术支持以进行故障排除。
### 显示支付结果  
您可以使用支付组件处理需要重定向（异步支付）和不需要重定向（同步支付）的支付方式。  

#### 重定向支付  
某些支付方式的支付流程需要离开原始网页，跳转到机构页面完成支付，例如在线银行支付。在这种情况下，买家完成支付后会被重定向到您在 **createPaymentSession** API 中提供的 _paymentRedirectUrl_。您可以在该URL中主动查询支付结果并展示给买家。  

#### 非重定向支付  
对于无需重定向的支付，支付结果将通过 `onEventCallback` 函数返回。这里的支付结果仅用于前端显示，最终订单状态以服务器端为准。  
您需要通过 `onEventCallback` 结果数据自定义每个支付结果的处理流程。  

以下是 `onEventCallback` 返回的支付结果可能的事件代码：  

| **事件代码** | **消息** | **解决方案** |
| --- | --- | --- |
| SDK_PAYMENT_SUCCESSFUL | 支付成功。 | 建议将买家重定向到支付结果页面。 |
| SDK_PAYMENT_PROCESSING | 支付处理中。 | 建议查看 `onEventCallback` 结果数据中的 *paymentResultCode* 以获取详细信息。根据提供的信息引导买家重试支付。 |
| SDK_PAYMENT_FAIL | 支付失败。 | 建议查看 `onEventCallback` 结果数据中的 *paymentResultCode* 以获取详细信息。根据提供的信息引导买家重试支付。 |
| SDK_PAYMENT_CANCEL | 买家未提交订单就退出了支付页面。 | 如果 *paymentSessionData* 在有效期内，可以重新调用 SDK；如果已过期，需要重新请求 *paymentSessionData*。 |
| SDK\_支付\_错误 | 支付状态异常 | 建议您检查`onEventCallback`结果数据中的`paymentResultCode`值以获取详细信息。根据提供的信息引导买家重试支付。 |
| --- | --- | --- | --- |
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
步骤3：获取支付结果（服务器端）
--------------------------------

买家完成支付或支付超时后，Antom会通过服务器交互将相应的支付结果发送给您，您可以通过以下任一方式获取支付结果：

1. **接收异步通知**：Antom会发送异步通知到您的服务器，您需要在服务器端设置接收并处理这些通知。
2. **查询结果**：您也可以主动发起查询请求，从Antom的服务器获取支付状态。

确保您的服务器能够正确处理这些请求，以便及时更新订单状态并提供相应的用户体验。
### **接收异步通知**  
当支付成功或失败时，蚂蚁金服会通过[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API，将异步通知发送到在**createPaymentSession** API中指定的_支付通知URL_。收到蚂蚁金服的通知后，您需要按照[要求](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)返回响应。  
蚂蚁金服允许您在**createPaymentSession** API的_paymentNotifyUrl_参数中指定URL。如果每个支付的URL相同，您也可以在蚂蚁金服控制台中进行配置。  

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
"currency": "MYR"
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
```
请注意，您需要完成签名验证的剩余部分，并根据验证结果处理支付状态。通常，这包括检查签名的有效性，确认支付详情，更新您的系统状态，然后返回适当的响应给蚂蚁金服。
```java
boolean verifyResult = SignatureTool.verify(request.getMethod(), request.getRequestURI(),
        clientId, requestTime, body, signature,
        ALIPAY_PUBLIC_KEY);
if (!verifyResult) {
    throw new RuntimeException("无效的回调签名");
}  
// 根据通知结果更新记录状态
// 回复服务器我们已接收通知
Result result = new Result("SUCCESS", "success", ResultStatusType.S);
AlipayResponse response = new AlipayResponse();
response.setResult(result);
return ResponseEntity.ok().body(response);
```

#### 常见问题解答 (FAQs)

##### 何时会发送通知？
这取决于支付是否完成：
*   如果支付成功完成，蚂蚁金服通常会在3到5秒内发送异步通知。对于像柜台支付（OTC）这样的支付方式，通知可能会稍有延迟。
*   如果支付未完成，蚂蚁金服需要先关闭订单，然后才会发送异步通知。不同支付方式关闭订单的时间会有所不同，通常默认为14分钟。

##### 异步通知会重新发送吗？
当你收到蚂蚁金服的异步通知时，你需要按照[示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)的格式返回响应。如果你未按要求响应异步通知，或者由于网络原因通知未送达，系统会在24小时内自动重试发送。通知最多重试8次，或者直到收到正确的响应以终止发送。重试发送的间隔为：0分钟，2分钟，10分钟，10分钟，1小时，2小时，6小时和15小时。

##### 需要在响应中添加数字签名吗？
不需要在响应中添加数字签名。通常，你只需要验证接收到的通知的签名，确保其来自蚂蚁金服，并在验证成功后返回正确的响应。
如果您收到蚂蚁金服的异步通知，您需要按照[示例代码](https://global.alipay.com/docs/ac/cashier_payment_cn/notification)的格式返回响应，但不需要在响应中添加数字签名。

#### 如何理解以下关键字段的含义？

*   _result_：订单的支付结果。
*   _paymentRequestId_：商家生成的用于查询、取消和对账的支付请求ID。
*   _paymentId_：蚂蚁金服生成的用于退款和对账的支付订单ID。
*   _paymentAmount_：如果有金额对账需求，您可以使用这个字段。
### **查询支付结果**  
您可以调用 **inquiryPayment** API 来查询订单的支付结果。  
| **参数名称** | **是否必需** | **描述** |
| --- | --- | --- |
| *paymentRequestId* |  | 商户生成的支付请求ID。 |  
请注意，以上参数不完整，完整的参数集及特定支付方式的额外要求，请参考 [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API 文档。  
以下示例代码展示了如何调用 **inquiryPayment** API:  
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
以下是一个请求消息的示例:  
```json
{
  "paymentRequestId": "paymentRequestId01"
}
```  
以下是一个响应消息的示例:  
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
*   _result_: API调用的结果。它仅表示**inquiryPayment** API调用的结果。订单状态应根据_paymentStatus_来确定。`SUCCESS`和`FAIL`表示最终结果，而`PROCESSING`表示交易仍在进行中。
*   _paymentAmount_: 金额验证。如果需要验证金额，可以使用此字段。
#### 我应该多久查询一次？
建议以2秒的间隔进行轮询查询，直到获取到最终的支付结果或接收到异步支付通知为止。

示例代码
==========

前端完整示例代码：
```javascript
// 步骤1：实例化SDK并处理回调事件
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
  .querySelector("#你的表单ID")
  .addEventListener("submit", handleSubmit);  

async function handleSubmit() {
  // 步骤2：服务器调用createPaymentSession API获取paymentSessionData。
  // ...
}
```

请注意，这里的`#你的表单ID`需要替换为实际的表单ID。
异步函数获取支付会话数据
================

```javascript
async function getPaymentSessionData() {
  const url = "填写服务器地址";
  const config = {
    // 填写请求配置。
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
  appearance: {
    showLoading: true, // 默认设为true，启用默认加载样式。
  },
});
}
```

事件代码
========

您可能会遇到两种类型的事件代码：

* 状态代码：在组件运行时生命周期中由`onEventCallback`返回。
* 错误代码：在组件初始化阶段由`onEventCallback`或`onError`返回。

| 类型 | 代码 | 描述 | 进一步操作 |
| --- | --- | --- | --- |
| 状态代码 | SDK\_START\_OF\_LOADING | 支付组件创建时加载动画开始播放。 | 无需进一步操作。 |
| SDK\_END\_OF\_LOADING | 支付组件创建时加载动画结束。 | 无需进一步操作。 |
| 错误代码 | SDK\_INTERNAL\_ERROR | SDK内部错误发生。 | 联系Antom技术支持解决问题。 |
| SDK\_CREATEPAYMENT\_PARAMETER\_ERROR | 传递给`AMSCashierPayment`方法的参数不正确。 | 确保参数传递正确并发送新请求。 |
| SDK\_INIT\_PARAMETER\_ERROR | 传递给`createComponent`方法的参数不正确。 | 确保参数传递正确并发送新请求。 |
| SDK\_CREATECOMPONENT\_ERROR | 调用`createComponent`方法时发生异常。 | 联系Antom技术支持解决问题。 |
| SDK\_CALL\_URL\_ERROR | 支付方式客户端撤销失败 | 联系蚂蚁金服技术支持解决此问题。 |
| --- | --- | --- |
| 查看文档最新更新，请访问 [版本更新日志](https://global.alipay.com/docs/releasenotes)。 |
| ![图片12](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片13](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png) |
| ©2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership) |
#### 此页面是否有帮助？
#### 本页内容
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
[实例化SDK](#KQO5X "实例化SDK")  
[调用SDK](#iVDpG "调用SDK")  
[常见问题](#ARgvG "常见问题")  
[显示支付结果](#Go6NO "显示支付结果")  
[重定向支付](#6ubRS "重定向支付")  
[非重定向支付](#NEgUb "非重定向支付")  
[步骤3：获取支付结果](#SnQk7 "步骤3：获取支付结果")  
[接收异步通知](#WDV7j "接收异步通知")  
[常见问题](#V1F5v "常见问题") |
[查询结果](#wlAb8 "查询结果")  
[常见问题解答](#tkpZO "常见问题解答")  
[示例代码](#xjYO0 "示例代码")  
[事件代码](#ZedB5 "事件代码")