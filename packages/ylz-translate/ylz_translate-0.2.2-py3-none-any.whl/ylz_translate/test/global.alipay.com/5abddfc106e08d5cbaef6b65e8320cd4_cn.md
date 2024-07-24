概览 | 自动扣款 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fautodebit_en%2Foverview)  
[返回首页](../../)  
自动扣款  
[概览](/docs/ac/autodebit_en/overview)  
接收支付  
支付后  
其他资源  
概览
========  
2024-05-20 08:50  
[中文版](https://global.alipay.com/docs/ac/autodebit_cn/overview)  
自动扣款功能允许在您的网站或应用上实现在线自动扣款，并支持在多种客户端类型（Web、WAP、App）上部署。只需一次性授权，即可实现一键未来支付。您只需集成一次，即可享受数字钱包和银行转账等多种支付方式。优秀的无缝支付体验减少了因扣款失败导致的客户流失。接受多种支付方式也有助于您的业务发展和拓展。

功能
============  
授权  
支付  
支付后
### 授权  
*   **获取授权**：  
    *   **启用支付方式**：签署合同以支持所需的支付方式。
    *   **获取授权页面URL**：使用[**consult**](https://global.alipay.com/docs/ac/ams/authconsult) API 获取用于渲染授权页面的URL，然后向买家展示支付方式授权页面。建议根据买家所在地区动态渲染支持的支付方式。
    *   **获取授权结果**：如果已配置接收授权结果通知的地址，买家授权成功后，会从Antom收到[**授权成功通知**](https://global.alipay.com/docs/ac/ams/notifyauth)。
    *   **获取支付令牌**：买家同意为支付方式授权自动扣款服务后，可以通过[**applyToken**](https://global.alipay.com/docs/ac/ams/accesstokenapp) API 获取支付令牌。此外，当支付令牌即将过期时，也可以通过[**applyToken**](https://global.alipay.com/docs/ac/ams/accesstokenapp) API 更新支付令牌。
*   **取消授权**：  
    *   如果买家在您的客户端内取消授权，需要通过[**revoke**](https://global.alipay.com/docs/ac/ams/authrevocation) API 使支付方式的支付令牌失效。
    *   如果买家在支付方式客户端内取消授权，您将收到[授权取消通知](https://global.alipay.com/docs/ac/ams/notifyauth)。
### 支付
*   **发起支付**: 买家提交订单并点击**确认支付**后，您的客户端调用[**pay**](https://global.alipay.com/docs/ac/ams/payment_agreement) API 向蚂蚁服务器发送支付请求，请求处理成功后即完成扣款。
*   **获取支付结果**:
    *   **同步重定向**: 支付完成后，买家会被重定向到您在[**consult**](https://global.alipay.com/docs/ac/ams/authconsult) API 中设置的 _authRedirectUrl_ 指定的支付结果页面。
    *   **异步通知**: 在[**pay**](https://global.alipay.com/docs/ac/ams/payment_agreement) API 中设置异步通知地址（_paymentNotifyUrl_），支付完成后或支付过期时，蚂蚁会向该地址发送异步通知。
*   **主动查询**: 通过[**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API 查询交易状态。
### 支付后操作  
*   **退款**: 您可以通过[Antom 商户门户](https://global.alipay.com/docs/ac/cashier_payment_cn/refund#Ote0I)发起退款，或者使用[**refund**](https://global.alipay.com/docs/ac/ams/refund_online) API。Antom 会通过[**notifyRefund**](https://global.alipay.com/docs/ac/ams/notify_refund)通知发送退款结果。您也可以调用[**inquiryRefund**](https://global.alipay.com/docs/ac/ams/ir_online) API 查询退款状态。
*   **取消交易**: 您可以调用[**cancel**](https://global.alipay.com/docs/ac/ams/paymentc_online) API 来取消交易。
*   **结算和对账**: 您可以使用Antom提供的结算文件进行对账。  
**集成**  
下表列出了自动扣款的所有API、通知和报告，以支持支付和支付后的流程：  
| **功能** | **开发资源** | |
| --- | --- | --- |
| **获取授权** | [咨询](https://global.alipay.com/docs/ac/ams/authconsult) | [notifyAuthorization](https://global.alipay.com/docs/ac/ams/notifyauth) |
| **撤销授权** | [撤销](https://global.alipay.com/docs/ac/ams/authrevocation) | [notifyAuthorization](https://global.alipay.com/docs/ac/ams/notifyauth) |
| **申请支付令牌** | [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) |  |
| **发起支付** | [pay（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement)[inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) | [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) |
| **取消支付** | [cancel](https://global.alipay.com/docs/ac/ams/paymentc_online) |  |
| **退款支付** | [退款](https://global.alipay.com/docs/ac/ams/refund_online)[查询退款](https://global.alipay.com/docs/ac/ams/ir_online) | [退款通知](https://global.alipay.com/docs/ac/ams/notify_refund) |
| **申报商品** | [申报](https://global.alipay.com/docs/ac/ams/declare)[查询申报请求](https://global.alipay.com/docs/ac/ams/inquirydeclare) |  |
| **结算对账** |  | [交易详情](https://global.alipay.com/docs/ac/reconcile/transaction_details)[结算详情](https://global.alipay.com/docs/ac/reconcile/settlement_details)[结算汇总](https://global.alipay.com/docs/ac/reconcile/settlement_summary) |  
表1. 自动扣款所用的API和通知  
支持的支付方式
----------------

  
自动扣款支持以下支付方式：

| **支付方式类型** | **支付方式** | **客户区域** |
| --- | --- | --- |
| Alipay+ 支付方式 | [支付宝](https://global.alipay.com/docs/ac/antomad/alipay) | 中国 |
| Alipay+ 支付方式 | [AlipayHK](https://global.alipay.com/docs/ac/antomad/alipayhk) | 中国香港 |
| Alipay+ 支付方式 | [Boost](https://global.alipay.com/docs/ac/antomad/boost) | 马来西亚 |
| Alipay+ 支付方式 | [DANA](https://global.alipay.com/docs/ac/antomad/dana) | 印度尼西亚 |
| Alipay+ 支付方式 | [GCash](https://global.alipay.com/docs/ac/antomad/gcash) | 菲律宾 |
| Alipay+ 支付方式 | [KakaoPay](https://global.alipay.com/docs/ac/antomad/kakaopay) | 韩国 |
| Alipay+ 支付方式 | [NAVER Pay](https://global.alipay.com/docs/ac/antomad/naverpay) | 韩国 |
| Alipay+ 支付方式 | [Rabbit LINE Pay](https://global.alipay.com/docs/ac/antomad/rabbitlinepay) | 泰国 |
| Alipay+ 支付方式 | [Toss Pay](https://global.alipay.com/docs/ac/antomad/toss_pay_autodebit) | 韩国 |
| Alipay+ 支付方式 | [Touch'n Go](https://global.alipay.com/docs/ac/antomad/touchngo) | 马来西亚 |
| 支付宝+支付方式 | [TrueMoney](https://global.alipay.com/docs/ac/antomad/truemoney) | 泰国 |
| 支付宝+支付方式 | [Zalopay](https://global.alipay.com/docs/ac/antomad/zalopay) | 越南 |
| 银行直接借记 | [KrungThai Bank](https://global.alipay.com/docs/ac/antomad/ktb) | 泰国 |
| 银行直接借记 | [Siam Commercial Bank](https://global.alipay.com/docs/ac/antomad/scb) | 泰国 |
| 钱包 | [GrabPay](https://global.alipay.com/docs/ac/antomad/grabpay) | 马来西亚，新加坡，印度尼西亚 |
| 钱包 | [Maya](https://global.alipay.com/docs/ac/antomad/maya) | 菲律宾 |
| 钱包 | [PayPay](https://global.alipay.com/docs/ac/antomad/paypay) | 日本 |
| 钱包 | [K PLUS](https://global.alipay.com/docs/ac/antomad/kplus) | 泰国 |

表2. 支持的支付方式

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。

![图片3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面是否有帮助？

#### 本页内容

[功能](#uugdl "功能")  
[集成](#KrAZU "集成")  
[支持的支付方式](#xtvNz "支持的支付方式")  
反馈