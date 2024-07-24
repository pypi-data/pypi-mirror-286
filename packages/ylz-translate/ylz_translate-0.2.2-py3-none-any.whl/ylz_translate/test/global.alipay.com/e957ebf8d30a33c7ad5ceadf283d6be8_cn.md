集成模式 | 开发参考 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg) ![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fref%2Foy9921)  
[返回首页](../../)

开发参考  
[沙箱环境](/docs/ac/ref/sandbox)  
[集成模式](/docs/ac/ref/oy9921)  
[安全文件传输](/docs/ac/ref/xgcpey)  
常见问题  
Antom 控制台  
工具  
其他参考  
[MCC 代码](/docs/ac/ref/mcccodes)  
[Amount 对象使用规则](/docs/ac/ref/cc)  
[支付方式](/docs/ac/ref/payment_method)  
[风险管理方法](/docs/ac/ref/risk_methods)  
[品牌资产](/docs/ac/ref/brandasset)  

集成模式
================

2022-03-03 08:49

集成实施可以通过以下三种模式进行：

1.  由具备开发能力的商家或收单机构（ACQ）自行完成。
2.  由商家或收单机构授权的独立软件供应商（ISV）进行，如果商家或收单机构允许ISV进行实施。
3.  由商家或收单机构邀请的系统集成商完成。

商家/ACQ 集成
------------------------

作为商家或ACQ，如果您为自己的公司进行集成，您将直接与支付宝对接。在这种集成模式下，您必须具备开发能力。
在与支付宝签约后，您将自行实施集成过程并管理商家账户和密钥。这种模式的实施成本高于通过ISV（独立软件供应商）或系统集成商进行集成。以下图表展示了采用此集成模式时支付宝与商家/ACQ（收单机构）之间的关系：

![图片3: image.png](https://cdn.nlark.com/yuque/0/2020/png/561635/1589985252291-616bd2a2-b120-4f89-bb46-c2af9ef7e85c.png)
图1. 商家/ACQ集成

ISV集成
--------
作为商家或ACQ，您可以授权ISV为您实施集成，通过与ISV签订授权服务合同。此外，您还需要与支付宝签订商户服务合同，以便支付宝为您提供支付、退款和结算等服务。

作为授权的ISV，您也需要直接与支付宝签订合同，然后为商家/ACQ提供服务，包括但不限于商户推荐、营销运营和集成服务。

以下图表展示了支付宝、商家/ACQ和ISV之间的关系：

![图片4: image.png](https://cdn.nlark.com/yuque/0/2020/png/561635/1589985252530-80a41689-ab84-4650-ad85-efdb4eee27ff.png)
图2. ISV集成

系统集成商集成
----------------
作为商家或ACQ，如果您没有开发能力，并且邀请系统集成商帮助您与支付宝进行集成，那么您是在采用系统集成商集成模式。

在与支付宝签约后，您将您的商家账户提供给系统集成商，系统集成商会使用您的账户为您与支付宝进行集成。

系统集成商集成模式是一种便捷且成本较低的方式，可以快速实现收款功能。以下图表展示了支付宝、商家/ACQ和系统集成商之间的关系：
**图3. 系统集成商集成**

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

![图6](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图7](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

**2024年支付宝** [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面有帮助吗？

#### 本页面内容

[商家/收单机构集成](#otgKB "商家/收单机构集成")  
[ISV集成](#raoYQ "ISV集成")  
[系统集成商集成](#iN3X3 "系统集成商集成")