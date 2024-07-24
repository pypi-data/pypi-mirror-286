# Android | 结账支付 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)](/docs/)
[![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fcashierpay%2Fcard_android)  
[返回首页](../../)  

## 结账支付
[概述](/docs/ac/cashierpay/overview)  
接收支付  
支付后操作  
支付方式  
其他资源  
高级功能  
[预前端解决方案API](/docs/ac/cashierpay/prefront)  
[先买后付API](/docs/ac/cashierpay/bnpl)  
[卡存储API](/docs/ac/cashierpay/cv)  
[卡存储SDK](/docs/ac/cashierpay/cvsdk)  
[卡支付功能API SDK](/docs/ac/cashierpay/mf)  

## Android
在本主题中，您将学习如何在Android客户端中集成卡支付SDK，以便在移动应用中渲染收银员页面。

### 先决条件
在集成卡支付SDK之前，请先熟悉[_集成指南_](https://global.alipay.com/docs/integration)和[_概述_](https://global.alipay.com/docs/ac/ams/api_fund)，以了解如何集成服务器API的步骤和调用API的注意事项。同时，请确保已完成以下任务：

1. 在Antom仪表盘中获取客户端ID。
2. 在Antom仪表盘中正确配置密钥。
3. 安装最新版本的Android Studio。
4. 目标至少为Android 4.4（API级别19）或更高。
5. 使用Gradle 4.1或更早版本。
6. 配置物理设备或模拟器以运行您的应用程序。

### 关键集成步骤
按照以下步骤集成卡支付SDK：

1. 集成SDK包  
   客户端
为了集成SDK包，请参考[Integrate the SDK Package](https://global.alipay.com/docs/ac/antom_sdk/android_en)。

2. 使用`AMSCashierPayment`方法创建SDK实例：

客户端操作：

1. 创建一个`configuration`对象：这是必需的。对象必须包含以下所有配置参数：
   * `setLocale`：可选字符串，商户客户端用以识别买家浏览器的语言。设置此参数以确保SDK显示正确的语言。有效值如下。如果传递其他值，将默认使用英语。
   * `locale("es", "ES")`：西班牙语
   * `locale("ko", "KR")`：韩语
   * `locale("pt", "BR")`：葡萄牙语
   * `locale("en", "US")`：英语
   * `setOption`：可选，用于指定是否使用默认加载模式和沙箱环境。有效值为：
   * `"sandbox", "true"`：沙箱环境
   * `"sandbox", "false"`：生产环境
   * `"showLoading", "true"`：使用默认加载模式。
   * `"showLoading", "false"`：不使用默认加载模式。

2. 创建一个**OnCheckoutListener** API的实例，用于后续过程中的事件处理。API包括以下方法：
   * `onEventCallback`：必需。一个监听结账页面支付事件的回调函数，返回`eventCode`和`eventResult`。

3. 将**OnCheckoutListener** API的实例设置到`configuration`对象中，以执行事件回调。

4. 实例化`AMSCashierPayment`方法。

创建SDK实例（Java）：

1. 2. 3. 4. 5. 6. 7. 8. 9. 10. 11. 12. 13. 14. 15. 16. 17. 18. // 创建 AMSCashierPaymentConfiguration 类型的对象。 AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration(); configuration.setLocale(new 

请注意，这里只提供了Java代码片段的开头，完整的代码实现需要继续编写以完成实例化和调用`AMSCashierPayment`方法。
```java
// 设置语言环境为美国英语
Locale locale = new Locale("en", "US");
// 默认情况下，showLoading 为 true，使用默认加载模式
// 设置为 false 可以根据 onEventCallback 自定义加载动画
configuration.setOption("showLoading", "true");
// 设置沙箱环境，留空则默认使用生产环境
configuration.setOption("sandbox", "true");
// 设置监听结账页面支付事件的回调
configuration.setOnCheckoutListener(new OnCheckoutListener() {
    @Override
    public void onEventCallback(String eventCode, AMSEventResult eventResult) {
        Log.e(TAG, "onEventCallback eventCode=" + eventCode + " eventResult=" + eventResult.toString());
    }
});
// 创建 AMSCashierPayment 对象
AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();
```

```
// 向支付宝服务器发送 **创建支付会话（结账支付）** 请求
// 这部分通常涉及网络调用，使用客户端 SDK 提供的方法，具体实现取决于蚂蚁金服的 API 文档
// 例如：
AlipayClient client = new AlipayClient(...); // 初始化客户端
AlipayRequest<CreatePaymentSessionRequest> request = new AlipayRequest<CreatePaymentSessionRequest>(...); // 创建请求对象，填充必要参数
client.execute(request, new AlipayCallback() {
    @Override
    public void onSuccess(CreatePaymentSessionResponse response) {
        // 处理成功响应，如展示支付二维码或启动支付流程
    }

    @Override
    public void onFailure(AlipayError error) {
        // 处理失败情况，如显示错误信息
    }

    @Override
    public void onConnectTimeout() {
        // 网络超时处理
    }

    @Override
    public void onNetworkError() {
        // 网络错误处理
    }
});
```

请注意，以上代码是示例，实际使用时需要根据蚂蚁金服的官方 SDK 文档和具体业务逻辑进行调整。
当买家选择信用卡支付方式后，您的客户端开始监听支付按钮的点击事件。一旦检测到支付按钮被点击，您的服务器需要向支付宝服务器发送一个 **[创建支付会话（Checkout Payment）](http://global.alipay.com/docs/ac/ams/session_cashier)** 请求。在接收到API响应后，使用`paymentSessionData`参数的值来完成第4步。

**注意**：在您的 **创建支付会话（Checkout Payment）** 请求中，将`paymentRedirectUrl`设置为您提供的URL Scheme，以便在支付完成后将买家重定向到支付结果页面。

以下是一个调用`createPaymentSession` API的示例，包括必填参数和一些可选参数。

```json
{
  "order": {
    "buyer": {
      "buyerName": {
        "firstName": "****",
        "fullName": "D**u",
        "lastName": "Liu",
        "middleName": "Skr"
      },
      "buyerRegistrationTime": "2022-01-01T09:30:00+08:00",
      "referenceBuyerId": "tony.c"
    },
    "goods": [
      {
        "goodsBrand": "AMSDM",
        "goodsCategory": "card/ssr/adc",
        "goodsName": "Goods No.1",
        "goodsQuantity": "1",
        "goodsSkuName": "SKU1",
        "goodsUnitAmount": {
          "currency": "USD",
          "value": "10000"
        },
        "goodsUrl": "HangZhou LeiFenTa",
        "referenceGoodsId": "amsdm_good_tony_c_20230227_095825_922"
      }
    ],
    "orderAmount": {
      "currency": "BRL",
      "value": "2129"
    },
    "orderDescription": "AMSDM_GIFT",
    "referenceOrderId": "amsdmorder_tony_c_20230227_095825_921"
  },
  "paymentAmount": {
    "currency": "BRL",
    "value": "2129"
  },
  "paymentFactor": {
    "isAuthorization": true
  },
  "paymentMethod": {
    // 支付方式相关参数
  },
  "paymentSessionData": {
    // 用于创建支付会话的数据
  },
  "returnUrl": "http://example.com/return", // 支付完成后返回的URL
  "notifyUrl": "http://example.com/notify" // 支付状态通知的URL
}
```

请注意，`paymentMethod`部分应包含具体的支付方式信息，`paymentSessionData`和`returnUrl`、`notifyUrl`是示例中的占位符，需要根据实际业务进行填充。
支付方式类型：信用卡  
支付方式元数据：  
支付方式区域：BR  
支付通知URL：https://www.google.com.sg  
支付重定向URL：https://www.baidu.com  
支付请求ID：amsdmpayk_tony_c_20230227_095825_920_532  
产品代码：CASHIER_PAYMENT  
结算策略：  
结算货币：USD  
启用分期付款收集：是  

以下是API调用的响应示例：  
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
"paymentSessionData": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Kvvmsdk+akdLvoShW5avHX8e8J15P8uNVEf/PcCMyXg==&&SG&&111",  
"paymentSessionExpiryTime": "2023-04-06T03:28:49Z",  
"paymentSessionId": "UNvjVWnWPXJA4BgW+vfjsQj7PbOraafHY19X+6EqMz6Ikyj9FPVUOpv+DjiIZqMe",  
"result": {  
"resultCode": "SUCCESS",  
"resultMessage": "成功。",  
"resultStatus": "S"  
}  
}  

请注意，上述信息是示例数据，实际使用时请替换为真实数据。
创建一个用于收集支付因素的组件，使用实例化对象中的`createComponent`方法  
客户端  
调用`createComponent()`方法并传入以下参数：  
*   _activity_：必需的对象，属于_Activity_类型。用于包含当前页面上下文参数的信息。
*   _sessionData_：必需的字符串。将通过**createpaymentSession（收银台支付）**API响应中获取的_paymentSessionData_参数的完整数据传递给_sessionData_参数。  
在以下情况下调用`onDestroy()`方法释放SDK组件资源：  
*   当用户离开结账页面时，释放**createPaymentSession**中创建的组件资源。
*   当用户发起多次支付时，释放之前**createPaymentSession**中创建的组件资源。  
创建配置对象：  
Java  
```java
checkout.createComponent(activity, sessionData);
// 释放SDK组件资源
checkout.onDestroy();
```
参考  
事件代码  
SDK 提供以下状态代码：  
*   `SDK_START_OF_LOADING`：在创建支付组件时开始播放加载动画。
*   `SDK_END_OF_LOADING`：在创建支付组件时加载动画结束。

SDK 提供以下错误代码：  
（此处应有错误代码列表，但原文档中这部分缺失，无法提供准确翻译。请根据实际SDK文档补充。）
* `SDK_INTERNAL_ERROR`: SDK 内部错误发生。请联系支付宝技术支持以解决问题。
* `SDK_CREATEPAYMENT_PARAMETER_ERROR`: 传递给 `createComponent` 方法的参数不正确。确保参数正确传递并重新发送请求。
* `SDK_CALL_URL_ERROR`: 表示以下情况之一：
  * 商户页面重定向执行失败。
  * 在 **createpaymentSession (收银台支付)** 请求中的 `paymentRedirectUrl` 参数未传递或传递错误。
* `SDK_INTEGRATION_ERROR`: 未找到依赖项。确保已正确添加依赖项并重新尝试集成过程。

关键步骤的代码示例

以下代码示例展示了集成过程中的关键步骤，不包括调用 **createpaymentSession (收银台支付)** API 的代码。

Java

```java
// 开发工具自动导入
import com.alipay.ams.component.sdk.callback.OnCheckoutListener;
import com.alipay.ams.component.sdk.payment.AMSCashierPayment;
import com.alipay.ams.component.sdk.payment.AMSCashierPaymentConfiguration;

// 步骤1：创建 AMSCashierPaymentConfiguration 类型的对象
AMSCashierPaymentConfiguration configuration = new AMSCashierPaymentConfiguration();
configuration.setLocale(new Locale("en", "US"));

// 设置沙箱环境。留空则默认使用生产环境。
configuration.setOption("sandbox", "true");

// 设置监听收银台页面支付事件的回调
configuration.setOnCheckoutListener(new OnCheckoutListener() {
    @Override
    public void onEventCallback(String eventCode, String message) {
        Log.e(TAG, "onEventCallback eventCode=" + eventCode + ", message=" + message);
        // 处理回调事件
    }
});

// 其他集成代码...
```

请注意，此代码示例仅展示了配置对象和设置回调的部分，实际集成还需要包括调用 API 和处理响应的代码。
```java
// 事件代码和结果记录
Log.d("Event", "eventCode=" + eventCode + "  eventResult=" + eventResult.toString());

// 初始化结账支付对象
AMSCashierPayment checkout = new AMSCashierPayment.Builder(activity, configuration).build();

// 提交支付
public void handleSubmit(View view) {
    // 步骤2：调用createPaymentSession API获取paymentSessionData
    String paymentSessionData = requestSessionData();

    // 步骤3：创建并渲染卡片组件
    // 最佳实践
    checkout.createComponent(activity, paymentSessionData);
}
```

```
#### 此页面是否有帮助？
要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。

![图片3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)
![图片4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)
```

请注意，上述代码是Java语言，用于支付宝的支付集成。文档中提到了如何记录事件、初始化支付组件以及提交支付的步骤。同时，页面底部提供了反馈帮助信息和链接到发行说明，以及支付宝的法律信息。