API调用模拟 | 开发参考 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)](/docs/) [![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fref%2Fapi_call_sim_en)  
[返回首页](../../)

开发参考  
[沙箱环境](/docs/ac/ref/sandbox)  
[集成模式](/docs/ac/ref/oy9921)  
[安全文件传输](/docs/ac/ref/xgcpey)  
常见问题  
蚂蚁开放平台仪表盘  
工具  
[API密钥配置](/docs/ac/ref/key_config_en)  
[API调用模拟](/docs/ac/ref/api_call_sim_en)  
[错误场景模拟](/docs/ac/ref/error_scenario_sim_en)  
[测试用例](/docs/ac/ref/test_case_en)  
其他参考  
[MCC代码](/docs/ac/ref/mcccodes)  
[Amount对象使用规则](/docs/ac/ref/cc)  
[支付方式](/docs/ac/ref/payment_method)  
[风险管理方法](/docs/ac/ref/risk_methods)  
[品牌资产](/docs/ac/ref/brandasset)  

API调用模拟
===================

2024-04-03 10:23  
API调用模拟帮助开发者在测试模式下调试接口。

开始前
----------------

在进行API调用模拟之前，请登录蚂蚁开放平台仪表盘，进入**密钥配置**页面，配置沙箱环境的设置。

1.  进入**开发者** > **密钥配置**，点击**生成密钥**。或者，进入**开发者** > **快速开始**，找到**集成资源和工具**，选择**集成资源**，然后点击**生成密钥**。
    **![图片3：image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1712137029801-92e42b3f-efb4-43c0-9b07-3864718772e5.png)**
2.  点击**确认**。密钥将自动生成。
**注意**: 私钥只显示一次，蚂蚁金服不会存储它。请确保保存你的私钥以备后用。  
3. 如果你需要更换密钥，可以通过一键替换或使用工具来完成。前往 **开发者** > **密钥配置**，点击 **替换密钥**。或者去 **开发者** > **快速入门**，找到 **集成资源和工具**，选择 **集成资源**，然后点击 **替换密钥**。  
![图片 4: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1712137093493-64297d14-bf25-4101-bc77-044d9ca7717c.png)  
**注意**:

  * 可以点击 **一键替换密钥** 来用蚂蚁金服生成的新密钥替换旧密钥。
  * 或者，点击 **使用自己的公钥和私钥** 后弹出的离线工具，自己生成公钥和私钥。  
![图片 5: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1712137154451-9ad33435-6993-4b1b-885b-ad3d20e8b855.png)  
4. 前往 **开发者** > **通知URL**。选择 **配置** 选项卡。在 **操作** 下点击 **添加**，并在 **通知URL** 中输入你的通知接口URL。  
**注意**: 除了使用API调用模拟，你也可以下载 **Postman脚本** 在本地进行调试。  
API调用模拟
------------

  1. 登录蚂蚁金服仪表盘，前往 **开发者** > **API调用模拟**。在 **请求配置** 选项卡中，选择你需要测试的具体API和产品。例如：  
![图片 6: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1712137223313-ff2c29da-5ec0-465f-a526-b4fee263b6e8.png)  
  2. 输入你的私钥。平台不会保存你的私钥。
3. (可选) 在“请求体”字段中编辑请求消息。
4. 点击**发送**以发送请求。
5. 请求发送后，响应消息将在屏幕右侧的“响应”标签中显示。

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

![图片10](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片11](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面有帮助吗？

#### 在这个页面上
[开始之前](#H2bHb "开始之前")
[API调用模拟](#YVPOv "API调用模拟")