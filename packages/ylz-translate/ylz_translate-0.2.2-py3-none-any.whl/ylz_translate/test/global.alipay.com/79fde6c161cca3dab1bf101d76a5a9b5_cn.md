简介 | 交易二维码支付 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Ftransactionqrcode%2Fintroduction)  
[返回首页](../../)

交易二维码支付
[Introduction](/docs/ac/transactionqrcode/introduction)  
[产品流程](/docs/ac/transactionqrcode/work_flow)  
[用户体验](/docs/ac/transactionqrcode/experience)  
[主要流程](/docs/ac/transactionqrcode/main_flow)  
[快速集成](/docs/ac/transactionqrcode/integration)  
[对账文件](/docs/ac/transactionqrcode/reconciliation)  
[API 列表](/docs/ac/transactionqrcode/api)  
数字签名
==========

2021-02-26 08:07

如果您已集成新的交易二维码支付产品，请参阅[订单码支付](https://global.alipay.com/doc/ams_oc/introduction)以获取详细信息。

概述
--------

交易二维码支付解决方案利用动态生成的二维码来代表一笔交易。在这种支付方案中，顾客无需输入交易金额，只需扫描生成的二维码即可完成支付。

为了提供这种支付服务，商家需要通过为该产品开发的接口与支付宝系统进行集成。

目标受众
------------

本文档适用于打算集成交易二维码支付解决方案的技术人员。

术语和定义
--------------

**二维码**
二维码（QR Code）是由黑色方块在白色背景上组成的方形网格，可以通过成像设备读取并处理。数据从图像的水平和垂直组件中的模式中提取，如下所示：
![图片3：简介](https://os.alipayobjects.com/rmsportal/dDTkdpNaupNXiur.png)
在这个交易二维码支付解决方案中，商家系统会向支付宝系统发送包含交易数据的请求，支付宝会回应一个代表交易的二维码。
**接口**
在此背景下，接口是支付宝系统通过调用相应的API并提供必要的参数值来提供服务的通道。在本指南中，我们可能会交替使用接口和服务。
要查看文档的最新更新，请访问[版本说明](https://global.alipay.com/docs/releasenotes)。
![图片4](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![图片5](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)
@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)
#### 这个页面有帮助吗？
#### 在此页面上
[概述](#u2bko "概述")  
[目标受众](#Audience "目标受众")  
[术语和定义](#Conventions "术语和定义")