支付宝集成指南 | 中国领先的第三方在线支付解决方案
==================================================

[![支付宝, 中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![支付宝, 中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fintegration_guide_en)  
[首页](/docs/)  
[在线支付](/docs/onlinepayment)  
[店内支付](/docs/instorepayment)  
[解决方案](/docs/solutions)  
[营收提升](/docs/ac/revenuebooster_en/overview)  
[组合支付](/docs/ac/combinedpay_en/overview)  
[灵活结算](/docs/ac/flexiblesettlement_en/overview)  
[集成指南](/docs/integration_guide_en)  
[Antom 仪表盘](/docs/dashboard_en)  
[SDKs](/docs/sdks)  
[APIs](https://global.alipay.com/docs/ac/ams/api)  
[对账](https://global.alipay.com/docs/ac/reconcile)  
[数字签名](https://global.alipay.com/docs/ac/ams/digital_signature)  
[沙箱](https://global.alipay.com/docs/ac/ref/sandbox)  
[工具](https://global.alipay.com/docs/ac/ref/key_config_en)  
[测试钱包](https://global.alipay.com/docs/ac/ref/testwallet)  
[争议](https://global.alipay.com/docs/ac/dispute)  
[商户服务](https://global.alipay.com/docs/ac/merchant_service)  
[版本更新](/docs/releasenotes)  
[支持](/docs/support)  
[术语表](/docs/glossary)  
[帮助中心](https://cshall.alipay.com/enterprise/global/klgList?sceneCode=un_login&routerId=d9aa1f608c4145d6b3c8030c17cf6f9a000&categoryId=50479)  
[旧版文档](https://global.alipay.com/docs/ac/legacy/legacydoc)  
集成指南
==========

本指南将引导您完成整个集成过程。按照以下步骤完成集成，您可以标记卡片来跟踪进度。

集成准备
---------

首先，[注册](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fintegration_guide_en) 并登录到 Antom 仪表盘。为了全面了解平台，请熟悉 Antom 文档。

1.  1

在沙箱中集成
-------------

5 步骤 全部折叠 全部展开

按照以下步骤在测试模式下完成与 Antom 产品的集成。

1.  ### 1. 完成沙箱配置
   标记卡片 取消标记卡片

   在 Antom 仪表盘中完成以下配置：

   * 通过 **开发者** > **快速开始** > **集成资源和工具** 获取沙箱环境的网关 URL、客户端 ID 和密钥。
   * 通过 **开发者** > **通知 URL** 设置您的通知 URL。
   * [沙箱配置](https://global.alipay.com/docs/dashboard_en#kZRFb)
2.  ### 2. 实施系统部署和调试
   标记卡片 取消标记卡片

   使用 [Antom SDKs](http://global.alipay.com/docs/sdks) 或自定义编码实现系统集成。

   以下工具将有助于集成过程：

   * API 调用模拟
   * 通知 URL
   * 错误场景模拟
   * 请求日志
   * 通知日志
   * [Antom SDKs](https://global.alipay.com/docs/sdks)
   * [API 调用模拟](https://global.alipay.com/docs/ac/ref/api_call_sim_en)
   * [错误场景模拟](https://global.alipay.com/docs/ac/ref/error_scenario_sim_en)
3.  ### 3. 进行端到端测试
   标记卡片 取消标记卡片

   使用测试钱包和测试账户进行端到端测试。要获取测试钱包和测试账户，请访问 [测试资源](http://global.alipay.com/docs/ac/cashierpay/test)。

   * [测试资源](https://global.alipay.com/docs/ac/cashierpay/test)
4.  ### 4. 进行验收测试（可选）
   标记卡片 取消标记卡片

   在 Antom 仪表盘的 **测试用例** 中执行并通过所有强制性测试用例。

   完成验收测试以提高应用程序系统的质量和稳定性。
5.  ### 5. 查看报告
   标记卡片 取消标记卡片

   沙箱集成后，您可以在网上查看交易详情和结算详情。联系 Antom 技术支持以查看 SFTP 报告。

2.  2

上线
----

2 步骤

在进行生产环境集成之前，请确保您的商户账户已激活并切换到生产模式。

1.  ### 1. 获取生产环境集成资源
   标记卡片 取消标记卡片

   * 登录 Antom 仪表盘。通过 **开发者** > **快速开始** > **集成资源和工具** 获取生产环境的网关 URL、客户端 ID 和密钥。
   * 将您代码项目中的沙箱客户端 ID 和密钥替换为生产环境的客户端 ID 和密钥。
2.  ### 2. 设置通知 URL
   标记卡片 取消标记卡片

   通过 **Antom 仪表盘** > **开发者** > **通知 URL** 设置通知 URL，以便接收 Antom 通知。

3.  3

进行试点测试
------------

3 步骤

1.  ### 1. 下载钱包应用
   标记卡片 取消标记卡片

   从应用商店下载钱包应用。
2.  ### 2. 创建钱包账户
   标记卡片 取消标记卡片

   创建您的生产钱包账户。如果需要帮助创建生产钱包账户，请联系 Antom 技术支持。
3.  ### 3. 完成试点测试
   标记卡片 取消标记卡片

   使用生产钱包账户执行端到端生产测试用例，确保应用程序运行顺畅。

4.  4

开始业务
--------

全部折叠 全部展开

一旦您的应用程序被激活为业务状态，请通知 Antom，以便我们监控您的系统行为并检查可能影响业务的任何不可预见的错误。

#### 本页面是否有帮助？

![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)