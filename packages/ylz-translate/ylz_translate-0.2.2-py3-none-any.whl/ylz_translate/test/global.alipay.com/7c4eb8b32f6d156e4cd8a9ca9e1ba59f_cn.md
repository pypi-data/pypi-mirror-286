网页/手机WAP | 结算支付 | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fcashierpay%2Fbank_webwap)  
[返回首页](../../)  

结算支付
[概览](/docs/ac/cashierpay/overview)  
接收支付  
支付后处理  
支付方式  
其他资源  
高级功能  
[预前端解决方案API](/docs/ac/cashierpay/prefront)  
[先买后付API](/docs/ac/cashierpay/bnpl)  
[卡存储API](/docs/ac/cashierpay/cv)  
[卡存储SDK](/docs/ac/cashierpay/cvsdk)  
[卡支付功能API/SDK](/docs/ac/cashierpay/mf)  

网页/WAP
========

在这个主题中，你将学习如何在网页或手机WAP客户端集成银行SDK，以便在计算机浏览器或移动浏览器中渲染支付页面。

先决条件
在集成SDK之前，请确保已完成以下任务：

1.  安装npm。
2.  处理兼容性问题：为Internet Explorer和其他旧版浏览器提供相应的polyfills。我们建议在构建项目时使用[babel-preset-env](https://babeljs.io/docs/en/babel-preset-env)来解决浏览器兼容性问题。
3.  使用以下推荐的浏览器版本：
    *   对于移动浏览器：
        *   iOS 11及以上版本
        *   Android 5.0及以上版本
    *   对于计算机浏览器，推荐以下版本：
| [Web/Wap](http://godban.github.io/browsers-support-badges/)**Edge** 无限制 | [Web/Wap](http://godban.github.io/browsers-support-badges/)**Firefox** 最后2个版本 | [Web/Wap](http://godban.github.io/browsers-support-badges/)**Chrome** 最后2个版本 | [Web/Wap](http://godban.github.io/browsers-support-badges/)**Safari** 最后2个版本 | [Web/Wap](http://godban.github.io/browsers-support-badges/)**Opera** 最后2个版本 | [Web/Wap](http://godban.github.io/browsers-support-badges/)**Electron** 最后2个版本 |
| --- | --- | --- | --- | --- | --- |

关键集成步骤

按照以下步骤集成SDK：

1. 导入SDK包
   客户端
   你可以通过以下任一方法添加SDK包：
   * 使用npm：在命令行界面输入安装命令。
   * 使用CDN资源：在HTML文件中使用脚本标签。

使用npm添加SDK包。
Shell
```bash
1
npm install @alipay/ams-checkout
```
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

使用CDN资源添加SDK包。
HTML
```html
1
<script src="https://sdk.marmot-cloud.com/package/ams-checkout/1.10.1/dist/umd/ams-checkout.min.js"></script>
```
ההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההההה
### 显示可用的支付方式

客户端：

在联系支付宝技术支持获取可用支付方式后，您可以通过以下模式展示支付方式：

1. **单一银行模式**：按银行展示支付方式。
2. **银行类型模式**：按银行类型展示，如手机银行应用、网上银行和银行转账。
3. **银行国家模式**：按银行国家展示，如泰国和印度尼西亚。

请参考[用户体验](https://global.alipay.com/docs/ac/cashierpay/bank_sdk#7WPiN)了解三种支付方式展示类型。

**注意**：在银行类型模式下，Web客户端无法显示手机银行应用类型的支付方式。

### 使用`AMSCashierPayment`方法创建SDK实例：

客户端：

1. 创建一个`_config`对象：必需。对象必须包含以下所有配置参数：
   * `_locale`：可选字符串，用于商户客户端识别买家浏览器的语言。设置此参数以确保SDK以正确语言显示页面。有效值如下，如果传递其他值，将默认使用英语。
   * `en_US`：英语
   * `in_ID`：印尼语
   * `th_TH`：泰语
   * `_environment`：必需字符串，用于指定**环境**信息。有效值为：
     * `SANDBOX`：沙箱环境
     * `PROD`：生产环境
   * `_analytics`：可选对象，用于配置和分析数据。包含值：
1. 参数设置:
   * `enabled`: 可选的布尔值，默认为`true`，表示允许SDK上传和分析操作数据，以提供更好的服务。如果不允许上传和分析数据，将其设置为`false`。
   * `onLog`: 可选。回调函数，用于在SDK执行过程中生成日志和API异常的错误信息。
   * `onClose`: 可选。当买家关闭弹出窗口时触发的回调函数。
   * `onEventCallback`: 可选。在支付过程中发生特定事件时，用于触发回调并返回事件代码的函数。

2. 初始化`AMSCashierPayment`方法:
   获取浏览器语言。
   JavaScript
   ```javascript
   let language = navigator.language || navigator.userLanguage;
   language = language.replace("-", "_"); // 将"-"替换为"_" 
   ```

   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

   创建SDK实例:
   npm
   ```javascript
   import { AMSCashierPayment } from '@alipay/ams-checkout';

   // 管理包
   const checkoutApp = new AMSCashierPayment({
       environment: "sandbox",
       locale: "en_US",
       analytics: {
           enabled: true
       },
       onLog: ({code, message}) => {},
       onEventCallback: ({code, message}) => {}
   });
   ```

这段代码展示了如何使用蚂蚁金服的`AMSCashierPayment` SDK 初始化一个实例，设置不同的配置选项，如环境（这里是沙箱环境）、语言、日志回调和事件回调。
创建 SDK 实例：

CDN

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
// 通过 CDN 资源引入 SDK 包： 初始化
window.AMSCheckout
const checkoutApp = new window.AMSCashierPayment({
environment: "sandbox", // 设置为沙箱环境
locale: "en_US", // 设置为英文（美国）环境
analytics: {
enabled: true // 启用分析
},
onLog: ({code, message}) => {}, // 日志回调
onEventCallback: ({code,  
message}) => {} // 事件回调
});
创建支付会话（结账支付）请求：

服务器端

当用户选择支付方式并且客户端检测到支付按钮点击事件后，服务器需要发送一个 **[创建支付会话（结账支付）](https://global.alipay.com/docs/ac/ams/session_cashier)** 请求。从 createPaymentSession 响应中获取 paymentSesssionData 值，并在步骤5中使用。

在 **创建支付会话（结账支付）** 请求中传递以下参数：
*   paymentRequestId: 商家为识别支付请求分配的唯一ID。
*   productCode: 表示正在使用的支付产品，值固定为`AGREEMENT_PAYMENT`。
*   paymentNotifyUrl: 用于接收支付结果通知的URL。
*   paymentRedirectUrl: 支付完成后用户重定向到的商家页面URL。
*   paymentAmount: 商家在订单货币中请求接收的支付金额。
*   order.orderAmount: 商家订单金额。在促销活动中，_orderAmount_值可能与_paymentAmount_值不同。
*   order.orderDescription: 订单描述。
*   order.referenceOrderId: 商家端的订单ID。当一个订单有多个支付请求时，支付宝建议使用一个_referenceOrderId_对应多个_paymentRequestId_。
*   paymentMethod.paymentMethodType: 设置为`BANK`。
*   paymentMethod.paymentMethodMetaData:
    *   在单一银行模式下，设置_bankName_为银行名称。
    *   在银行类型模式下，设置_paymentMethodCaregory_为支付方法类型。有效值包括`BANK_TRANSFER`，`MOBILE_BANKING_APP`和`ONLINE_BANKING`。
    *   在银行国家模式下，设置_paymentMethodRegion_为国家。有效值为`TH`和`ID`。

单一银行模式示例：

```json
{
  "order": {
    "orderAmount": {
      "currency": "THB",
      "value": "160"
    },
    "orderDescription": "Cappuccino #grande (Mika's coffee shop)",
    "referenceOrderId": "ORDER_20230803165257496"
  },
  "paymentAmount": {
    "currency": "THB",
    "value": "160"
  },
  "paymentMethod": {
    "paymentMethodType": "BANK",
    "paymentMethodMetaData": "{\"bankName\":\"Siam Commerical Bank\"}"
  },
  // 其他可能的字段...
}
```

请注意，以上JSON示例仅展示了部分字段，实际文档可能包含更多内容。
结算策略:
结算货币: USD

支付通知URL: <https://kademo.intlalipay.cn/payments/notifySuccess>

支付重定向URL: <https://kademo.intlalipay.cn/melitigo/Test_114.html>

支付请求ID: PAY_20230804165257508

产品代码: CASHIER_PAYMENT

银行类型模式
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

订单信息:
订单金额:
货币: THB
值: 160

订单描述: 卡布奇诺#大杯 (Mika's咖啡店)

参考订单ID: ORDER_20230803165257496

支付金额:
货币: THB
值: 160

支付方式:
支付方式类型: 银行
支付方式元数据: {"paymentMethod Gregory": "BANK_TRANSFER"}

结算策略:
结算货币: USD

支付通知URL: <https://kademo.intlalipay.cn/payments/notifySuccess>

支付重定向URL: <https://kademo.intlalipay.cn/melitigo/Test_114.html>

支付请求ID: PAY_20230804165257508

产品代码: CASHIER_PAYMENT

请注意，上面的示例包含了一段混合了希伯来语和英语的文本，但已将其翻译成中文。如果原始文档中不应该包含希伯来语，请忽略这部分内容。
银行国家模式  
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
{  
"订单": {  
"订单金额": {  
"货币": "THB",  
"值": "160"  
},  
"订单描述":  
"卡布奇诺#大杯  
(Mika的咖啡店  
)",  
"参考订单号":  
"ORDER\_202308031652  
57496"  
},  
"支付金额": {  
"货币": "THB",  
"值": "160"  
},  
"支付方式": {  
"支付方式类型":  
"银行",  
"支付方式元数据"  
:  
"{\\"支付方式地区\\":\\"TH\\"}"  
},  
"结算策略": {  
"结算货币":  
"USD"  
},  
"支付通知URL": "https  
://kademo.intlalipay.cn  
/payments  
/notifySuccess",  
"支付重定向URL":  
"https://kademo  
.intlalipay.cn/melitigo  
/Test\_114.html",  
"支付请求ID":  
"PAY\_20230804165257508"  
,  
"产品代码":  
"CASHIER\_PAYMENT"  
}  
呈现支付页面  
客户端  
在配置对象中使用`createComponent`方法：  
1. 使用_sessionData_参数创建配置对象：将步骤4中获取的_paymentSessionData_值传递给`createComponent`方法的_sessionData_参数。
2. 调用实例对象的 `createComponent()` 方法。返回值为 `Promise`，内容为使用此方法获取的实例对象。支付组件的 DOM 对象会根据环境参数渲染支付方式并在当前页面上显示。可以配置以下参数：
*   _appearance_: 可选对象，用于自定义网页样式。有效值为：
*   _showLoading_: 可选布尔值，默认为 `true`，表示使用默认加载样式。如果不使用默认加载样式，将其设置为 `false`。

调用 `unmount()` 方法在以下情况下释放 SDK 组件资源：
*   当用户离开结账页面时，释放 `createPaymentSession` 中创建的组件资源。
*   当用户发起多次支付时，释放前一次 `createPaymentSession` 中创建的组件资源。

调用 `createComponent` 方法：
```javascript
async function create(sessionData) {
  await checkoutApp.createComponent({
    sessionData: sessionData,
    appearance: {
      showLoading: true, // 默认为 true，启用默认加载样式
    },
  });
}

// 释放 SDK 组件资源
checkoutApp.unmount();
```

6. 获取支付结果
   服务器端
当支付达到最终的成功或失败状态时，支付宝会通过[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API 向您在[**createPaymentSession**](https://global.alipay.com/docs/ac/ams/createpaymentsession_easypay) API 中传递的 _paymentNotifyUrl_ 发送异步通知。收到支付宝的通知后，您必须按照[要求](https://global.alipay.com/docs/ac/ams/paymentrn_online)返回响应。您也可以通过调用[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API 来查询支付结果。

事件代码
SDK 提供以下状态代码：
*   `SDK_START_OF_LOADING`：在创建支付组件时开始播放加载动画。
*   `SDK_END_OF_LOADING`：在创建支付组件时加载动画结束。

SDK 提供以下错误代码：
*   `SDK_INTERNAL_ERROR`：SDK 内部错误发生。联系支付宝技术支持解决问题。
*   `SDK_CREATEPAYMENT_PARAMETER_ERROR`：传递给 `AMSCashierPayment` 方法的参数不正确。确保参数正确传递并发送新请求。
*   `SDK_INIT_PARAMETER_ERROR`：传递给 `createComponent` 方法的参数不正确。确保参数正确传递并发送新请求。
*   `SDK_CREATECOMPONENT_ERROR`：调用 `createComponent` 方法时发生异常。联系支付宝技术支持解决问题。
*   `SDK_CALL_URL_ERROR`：支付方式客户端撤销失败。联系支付宝技术支持解决问题。

#### 这个页面有帮助吗？
要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。
请注意，由于我是一个文本生成的AI，我无法直接处理或翻译图片内容。但是，我可以帮助翻译文本和提供一般性的指导。如果图片中包含文本或者需要解释的内容，请提供图片的文字描述或者直接输入图片上的文字，我将很乐意帮助翻译。关于2024年支付宝的法律信息，通常这类链接会指向服务条款、隐私政策或使用协议等，但具体信息需要访问链接才能查看。如果你需要这些法律文档的中文翻译，建议直接访问[https://global.alipay.com/docs/ac/platform/membership](https://global.alipay.com/docs/ac/platform/membership)。如果该页面提供多语言版本，你应该能找到中文版本。