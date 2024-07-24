接受支付 | 订单码支付 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams_oc%2Facceptpayment)

[返回首页](../../)

订单码支付
----------

[介绍](/docs/ac/ams_oc/introduction)

[开始使用](/docs/ac/ams_oc/start)

[接受支付](/docs/ac/ams_oc/acceptpayment)

[支付后服务](/docs/ac/ams_oc/postpayment)

[最佳实践](/docs/ac/ams_oc/bp)

开发
----

[API 列表](/docs/ac/ams_oc/apilist)

[对账](/docs/ac/ams_oc/reconcile)

参考
----

[版本发布说明](/docs/ac/ams_oc/releasenotes)

[旧版本](/docs/ac/ams_oc/legacyv)

接受支付
===============

2023年6月29日 10:32

要集成支付宝，您可以使用支付宝提供的开放 SDK 或者直接调用 API。

使用开放 SDK
=============

支付宝全球开放 SDK 封装了集成过程，包括调用支付宝 API 的签名添加和验证。更多详情，请参阅：

- [_Java 版支付宝 SDK_](https://github.com/alipay/ams-java-sdk)
- [_PHP 版支付宝 SDK_](https://github.com/alipay/global-open-sdk-php)
- [_Python 版支付宝 SDK_](https://github.com/alipay/global-open-sdk-python)
- [_.Net 版支付宝 SDK_](https://github.com/alipay/global-open-sdk-dotnet)

API 集成
==========

集成支付宝订单码支付产品后，可以通过让用户扫描订单码来接受支付。以下图表展示了从客户那里接收支付的交互流程：
![图片3: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1592969442054-8ced3a34-22c5-4cf3-bfb2-4f3afea2b05a.png)  
图1. 订单码支付产品的支付流程  
支付流程包括以下步骤：  
1. 商户向支付宝发送请求，请求生成订单码。  
1.1 支付宝返回订单码给商户。  
1.2 支付宝通知商户支付结果。（在客户完成支付后。）  
1.3 商户向支付宝发送确认消息，确认收到支付通知。  
2. 商户向客户展示订单码。  
3. 客户打开电子钱包并扫描订单码。商户扫描钱包以启动支付流程。  
4. 客户确认支付。  
5. ISV（独立软件供应商）向支付宝发送支付请求。  
发起支付请求
--------------------------
在开始集成支付宝的订单码支付产品之前，请先阅读“开发”部分，了解如何在沙箱和生产环境中调用接口。然后继续完成以下步骤：
### 步骤1：构建请求  
您需要构建的请求由四个部分组成：  
*   请求URL格式：**https://open-sea-global.alipay.com/ams/api/v1/payments/pay**
*   方法：**POST**
*   HTTP头：主要包括字段如\_Client-Id\_，\_Signature\_，\_Encrypt\_，\_Content-Type\_，\_Request-Time\_和\_Agent-Token\_。
*   HTTP正文：包含JSON格式的详细业务请求信息，且业务请求信息需要签名。更多详情参见[**支付**](https://global.alipay.com/doc/ams/upm)接口文档。  
以下是一个订单码支付请求的HTTP正文示例：  
复制  
```json
{
"productCode": "IN_STORE_PAYMENT",
"paymentNotifyUrl": "http://xmock.inc.alipay.net/api/Ipay/globalSite/automtion/paymentNotify.htm",
"paymentRequestId": "102775745075669",
"paymentFactor": {
"inStorePaymentScenario": "OrderCode"
},
"order": {
"referenceOrderId": "102775745075669",
"orderDescription": "Mi Band 3 Wrist Strap Metal Screwless Stainless Steel For Xiaomi Mi Band 3 ",
"orderAmount": {
"currency": "USD",
"value": "10"
},
"merchant": {
"referenceMerchantId": "seller231117459@login.com",
"merchantName": "cup Hu",
"merchantMCC": "1234",
"store": {
"referenceStoreId": "S0000000001",
"storeName": "UGG-2",
"storeMcc": "1405"
}
}
},
"paymentAmount": {
"currency": "USD",
"value": "10"
},
"paymentMethod": {
"paymentMethodType": "CONNECT_WALLET"
}
}
```
**注意事项**：  
*   对于订单码支付，需要在支付接口中指定\_inStorePaymentScenario\_为\_OrderCode\_。
*   所有交易金额应以货币的最小单位表示。例如，当货币代码为USD时，$5.99表示为599，当货币代码为JPY时，￥599表示为599。详情请参考[_ISO 4217货币代码_](https://www.iso.org/iso-4217-currency-codes.html)。
### 步骤2：向支付宝提交支付请求  
按照步骤1的建议构建请求后，使用以下网关地址向支付宝提交请求：

*   **open-na.alipay.com**：适用于北美地区的商家。
*   **open-sea.alipay.com**：适用于亚洲地区的商家。
*   **open-eu.alipay.com**：适用于欧洲地区的商家。

**注意：**
网关地址可能会发生变化，请保持关注更新。
### 步骤3：处理支付结果  
支付结果通知可以是同步的，异步的，或者两者都有。  
为了处理支付结果通知，您需要执行以下操作：  
1. 通过验证通知的签名来处理支付结果响应或通知。
2. 对于异步通知，向支付宝返回一个收据确认消息。  

#### 验证通知的签名  
支付宝发送给商家的通知是经过签名的。商家需要验证签名以确认通知是否来自支付宝。  
以下是一个典型的通知头和正文示例。  

通知头：  
复制  
"Content-Type": "application/json",
"Request-Time": "2019-07-12T12:08:56.253+05:30",
"client-id": "T_111222333",
"Signature": "algorithm=RSA256,keyVersion=1,signature=jTOHqknjk%2fnDjEn8lfg%2beNODdoh2eHGJV%2blvrKaDwP782WxJ7ro49giqUu23MUM8sFVVNvhg32qHS3sd4O6uf5kAVLqztqNOPJFZcjw141EVi1vrs%2bIB4vU0%2fK%2f8z2GyWUByh2lHOWFsp%2b5QKCclXp%2bjacYqWYUur5IVbuebR1LoD5IiJ7u7J9qYriFxodkxmIAJYJyJs7mks2FWHh2YePLj3K%2f4B65idy7RBKqY1NN1XcvqnbQmlfCH8CIv75bg%2fr9sGmPE5a%2bYgL8N9Q41buGwMSq1IcNsbceMbyPhw5Z5HnJ7tPz12fvdSi0cEicPikDthQ2EQFmtpntXcAc%2fHA%3d%3d"  

通知正文（成功支付示例）：  
复制  
{
"notifyType": "PAYMENT_RESULT",
"result": {
"resultCode": "SUCCESS",
"resultStatus": "S",
"resultMessage": "success"
},
"paymentRequestId": "pay_test_1106_0002", // 商家为识别支付请求分配的唯一ID。
"paymentId": "20200101234567890132", // 支付宝为识别支付分配的唯一ID。
"paymentAmount": { // 商家在订单货币中请求接收的支付金额。
"value": "8000",
"currency": "EUR"
},
"paymentCreateTime": "2020-01-01T12:01:00+08:30" // 支付创建的日期和时间。
支付完成时间：2020-01-01 12:01:01 (北京时间+8:30) //支付成功或失败的最终状态时间

失败支付通知体：
```
{
"notifyType":"PAYMENT_RESULT",
"result": {
"resultCode":"USER_BALANCE_NOT_ENOUGH",
"resultStatus":"F",
"resultMessage":"余额不足"
},
"paymentRequestId":"pay_test_1106_0002",
"paymentId":"20200101234567890132"
}
```
基于上述通知头和通知体，需要验证的内容如下：
```
POST {使用您的通知地址，如 /merchant/notify}
T_111222333.2019-07-12T12:08:56+05:30.{"notifyType":"PAYMENT_RESULT","result":{"resultCode":"SUCCESS","resultStatus":"S","resultMessage":"success"},"paymentRequestId":"pay_test_1106_0002","paymentId":"20200101234567890132","paymentAmount":{"value":"8000","currency":"EUR"},"actualPaymentAmount":{"value":"8000","currency":"EUR"},"paymentCreateTime":"2020-01-01T12:01:00+08:30","paymentTime":"2020-01-01T12:01:01+08:30"}
```
#### 接收通知
您可以利用通知来自动化业务流程。处理通知时，您需要：

1. **配置接收通知的服务器地址。**
   在支付宝开发者平台或支付接口中配置服务器地址以接收支付宝的通知。

2. **接收通知并返回必要的确认响应。**
   为了确保服务器正常接收通知，支付宝要求您对每个通知返回一个**成功**响应以确认接收。

3. **应用业务逻辑。**
   如果您使用HTTPS接收通知，服务器证书必须按照认证要求进行配置。

**返回必要的确认响应**
当客户支付成功后，支付宝会向商家发送支付结果通知。接收通知的地址在发起支付请求时指定。商家收到通知后，必须向支付宝返回一个确认接收的响应消息。

如果商家未对通知进行回应，支付宝会认为通知未送达并持续发送通知。发送给支付宝的响应（确认接收消息）不需要签名。

**注意：**
只有在接收到支付宝支付成功的通知后，才能确认支付成功，商家可以继续进行如发货等购买流程。不要仅依赖支付结果页面来判断支付是否成功。客户可能在结果到达前关闭了页面，或者结果页面上可能显示了被恶意篡改的信息。

以下示例展示了商家发送给支付宝的响应头和响应体：

响应头：
```
"Content-Type": "application/json",
"response-time": "2019-07-12T12:08:56+05:30",
"client-id": "T_111222333",
```
响应体：
```
{
"result": {
"resultCode":"SUCCESS",
"resultStatus":"S",
"resultMessage":"success"
}
}
```
异常情况
----------------
客户支付成功，但商家未收到支付结果通知。

在这种情况下，客户完成了支付，资金被扣除，但商家未收到支付结果通知，因此交易失败。

**可能的原因：**
*   客户的支付达到最终状态（支付成功或支付失败）后，支付宝未能及时通知商家。
*   支付宝已通知商家，但由于网络原因，商家未收到支付结果。

**应对措施：**
1. 商家应检查网络连接，确保与支付宝的通信畅通。
2. 查看支付宝的回调日志，确认是否收到通知，或是否有错误信息。
3. 如果长时间未收到通知，商家可以通过调用查询接口主动查询交易状态。
4. 联系支付宝技术支持以获取帮助。
建议商家在交易关闭时间之前调用[**查询支付**](https://global.alipay.com/docs/ac/ams/paymentri)接口查询支付状态。如果获取到成功支付状态，继续进行交易。如果返回的支付状态不明确，应继续尝试查询请求。如果获取到失败的支付状态，或者交易超时，调用[**取消**](https://global.alipay.com/doc/ams/paymentc)接口取消交易。

**注意：**

*   支付页面展示后，如果在规定时间内未完成支付，交易会默认关闭。
*   商家可以通过在[**支付**](https://global.alipay.com/doc/ams/oc)接口中设置_paymentExpireTime_参数来设定交易关闭时间，也可以调用[**取消**](https://global.alipay.com/doc/ams/paymentc)接口关闭未支付的交易或取消已支付的交易。
*   若商家未指定_paymentExpireTime_参数，交易关闭时间将按照合同协议默认设置。

**更多信息：**

*   [后支付服务](https://global.alipay.com/docs/ac/ams_oc/postpayment)
*   [结算与对账](https://global.alipay.com/docs/ac/ams_oc/settlmt_recon)
*   查看文档最新更新，请访问[版本更新日志](https://global.alipay.com/docs/releasenotes)。

![Image 4](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![Image 5](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面有帮助吗？

#### 本页面内容：

[使用开放SDK](#2uykJ "使用开放SDK")  
[API集成](#JOjOe "API集成")  
[发起支付请求](#PZQej "发起支付请求")
**步骤1：构建请求**

在这一阶段，你需要根据蚂蚁金服的API规范，组装支付请求的参数。这通常包括交易类型、金额、商品描述、回调URL等关键信息。

**步骤2：向支付宝提交支付请求**

完成请求参数的构建后，使用你的应用密钥和签名算法，对请求进行签名，然后将请求发送到支付宝的支付接口。确保所有的请求数据都已加密，以保证交易的安全性。

**步骤3：处理支付结果**

当用户完成支付后，支付宝会将支付结果通过回调URL返回给你的服务器。你需要监听这个URL，接收并解析返回的数据，以确定支付是否成功。

**验证通知的签名**

在接收到支付宝的支付通知时，你需要验证其签名以确认消息的来源和完整性。使用你的应用私钥和支付宝提供的签名算法，对比计算出的签名与通知中的签名，确保数据未被篡改。

**接收通知**

确保你的服务器能够持续接收并处理支付宝发送的支付状态更新。这些通知可能包括支付成功、退款、撤销交易等信息。

**异常情况**

处理可能出现的异常情况，如网络故障、支付失败、用户取消支付等。确保有适当的错误处理机制和重试策略。

**更多信息**

要获取更详细的文档、示例代码和最佳实践，可以访问蚂蚁金服的开发者中心。在那里，你可以找到关于如何集成支付功能到你的应用中的详细指南。