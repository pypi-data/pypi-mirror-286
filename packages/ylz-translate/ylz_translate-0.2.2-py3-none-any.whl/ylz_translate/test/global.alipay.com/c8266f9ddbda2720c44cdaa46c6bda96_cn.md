简介 | 自动扣款 | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg) ![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fagreementpayment%2Fintro)  
[返回首页](../../)

自动扣款
[Introduction](/docs/ac/agreementpayment/intro)  
[开始使用](/docs/ac/agreementpayment/getting_started)  
[授权与支付](/docs/ac/agreementpayment/payment)  
[后支付服务](/docs/ac/agreementpayment/post_payment)  
[报表与对账](/docs/ac/agreementpayment/report)  
[最佳实践](/docs/ac/agreementpayment/autodebit_bp)  
[幂等性](/docs/ac/agreementpayment/api_idemptcy)  
开发
[API 列表](/docs/ac/agreementpayment/apis)  
参考
[版本发布说明](/docs/ac/agreementpayment/releasenotes)  

简介
============

2022-03-09 05:52

> **注意**：这不是自动扣款文档的最新版本。此版本不再更新，但将在2022年9月之前仍可访问，之后将被弃用并从支付宝文档中移除。建议您阅读[**最新版本**](https://global.alipay.com/docs/ac/autodebitpay/overview)的自动扣款文档。

自动扣款支付是一种允许商家预先授权从用户账户中扣除资金的支付解决方案。

用户首先需要通过支付协议（如三方代扣协议）向商家授予同意。

当用户再次在商家网站上购买商品时，商家可以使用授权令牌直接从用户的账户中扣款。
随后，商家可以使用该令牌发起自动扣款支付请求。

用户体验
==========

这是一个消费者使用GCash在苹果App Store中支付商品的示例流程：

![图片3：协议支付.jpg](https://cdn.nlark.com/yuque/0/2020/jpeg/561635/1590650669066-2bcc259f-8226-47ef-bc60-0711e4b4c440.jpeg)
图1. 自动扣款支付演示

假设用户已下载了GCash应用，以下是示例流程：

1. 用户在App Store（商家端）选择价值1000 PHP的商品，下单并选择GCash作为支付方式。
2. 用户被重定向到GCash的授权页面，显示授权协议。
3. 用户完成授权并返回App Store，显示授权结果和关联的GCash账户。
4. 用户选择GCash账户完成支付。App Store随后返回支付成功的结果。

工作原理
==========

在自动扣款支付中，涉及以下角色：

* **客户**：使用支付服务的个人或机构。
* **商家**：进行商品或服务交易的公司或个人。
* **支付宝**：提供自动扣款支付服务。
* **Alipay+ MPP**：Alipay+ 移动支付伙伴。在自动扣款中，Alipay+ MPP是一个数字钱包，如GCash。

以下是自动扣款支付的授权和支付流程图：

![图片4：image](https://yuque.antfin.com/images/lark/0/2021/png/303011/1637829072662-88172015-ec1a-4ab4-b7b7-15d2691591c1.png)
图2. 授权流程

授权完成后，商家可以使用访问令牌发起支付请求。

![图片5：支付流程.png](https://cdn.nlark.com/yuque/0/2021/png/12884741/1634545288810-0ee3a394-9706-42b9-a8d0-1b5ee9e1651c.png)
图3. 支付流程

更多信息
---

**开始使用**  
[开始使用 Alipay 协议支付](https://global.alipay.com/doc/agreementpayment/getting_started)  
**授权与支付**  
[Alipay 协议支付的授权与支付流程](https://global.alipay.com/doc/agreementpayment/payment)  
要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。  
![图片 6](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 7](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)  
©2024 Alipay [法律信息](https://global.alipay.com/docs/ac/platform/membership)  

#### 这个页面是否有帮助？  

#### 在这个页面上  
**用户体验**  
[用户体验](#PTczH "用户体验")  
**工作原理**  
[协议支付的工作原理](#bLN9M "工作原理")  
**更多信息**  
[了解更多详情](#VLkwD "更多信息")