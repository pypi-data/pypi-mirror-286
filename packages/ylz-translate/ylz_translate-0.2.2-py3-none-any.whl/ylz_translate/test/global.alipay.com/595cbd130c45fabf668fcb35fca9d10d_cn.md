对账 | 对账 | 支付宝文档
===============  
![图片 1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片 2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)  
[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Freconcile%2Fperform)  
[返回首页](../../)  
对账
[概览](/docs/ac/reconcile/overview)  
[结算规则](/docs/ac/reconcile/rules)  
[结算生命周期](/docs/ac/reconcile/lifecycle)  
[执行对账](/docs/ac/reconcile/perform)  
[交易详情报告](/docs/ac/reconcile/transaction_details)  
[结算详情报告](/docs/ac/reconcile/settlement_details)  
[结算汇总报告](/docs/ac/reconcile/settlement_summary)  
[报告字段摘要](/docs/ac/reconcile/field_summary)  
执行对账
======================  
2023-09-18 12:51  
您可以使用以下两种方式执行对账：  
*   [使用报告对账](#bQZkg)
*   [使用门户对账](#eGvPL)  
报告
=======  
本节解释如何获取对账报告以及如何使用报告进行对账。  
获取报告
--------------  
您可以以下列两种方式获取对账报告：  
*   [从SFTP服务器下载](#LYsyS)：从SFTP服务器下载的对账报告可以根据您的需求定制。除非另有要求，否则SFTP服务器中配置的内容在对账报告功能更新时不会自动更新。
* 从全球商家门户下载：从门户下载的对账报告无法根据您的需求进行定制。当对账报告功能更新时，门户中的对账报告也会发生变化。
### SFTP
您可以从SFTP服务器上的特定目录下载对账报告。支付宝将所有报告编码为UTF-8并上传到SFTP服务器。从SFTP服务器下载的报告包括.csv和.xlsx格式。

#### 服务器登录
在从SFTP服务器获取对账报告之前，请完成以下步骤：

1. 联系支付宝商户服务技术支持（[overseas_support@service.alibaba.com](mailto:overseas_support@service.alibaba.com)）以获取SFTP登录凭据，并提交访问SFTP服务器的公共IP地址。
2. 使用以下信息登录SFTP服务器：
   * 端口：22
   * 主机名：isftp.alipay.com（如果此链接加载速度慢，可尝试sftp.alipay.com）
   * 用户名和密码

**注意：**

* 90天未使用的SFTP账户将被禁用。
* SFTP服务器上超过7天的对账报告可能会被删除。如果报告被删除，您可以在[支付宝全球商户门户](#jfNCL)下载。
* 如果无交易，您可以联系支付宝商户服务技术支持（[overseas\_support@service.alibaba.com](mailto:overseas_support@service.alibaba.com)）配置是否生成对账报告。

对于报告的具体下载路径，请参阅以下报告下载路径部分。

#### 报告下载路径
所有对账报告的下载路径为报告目录 + 报告名称。例如，结算详情报告的下载路径：`/v1/settlements/102*************234/20221024/settlementItems_USD_202*************234_000.csv`。

##### 报告目录
不同报告类型的下载目录格式和示例如下：

| **报告类型** | **报告目录格式** | **示例** |
| --- | --- | --- |
| 交易详情报告 | `/v1/settlements/<商户支付宝ID>/<交易日期>/` | `/v1/settlements/102*************234/20181225` |
| 结算详情报告 | `/v1/settlements/<商户支付宝ID>/<结算日期>/` | `/v1/settlements/102*************234/20181227` |
| 结算汇总报告 |  |  |

**表1. 不同报告的下载目录**

报告目录格式中的概念解释如下：

*   **merchantIdByAcquirer**: 支付宝为商户分配的标识
*   **transactionDate**: 交易日期
*   **settlementDate**: 支付宝与商户结算的日期

**报告名称**

不同报告的默认报告名称和格式如下。您也可以联系支付宝商户服务技术支持（[overseas\_support@service.alibaba.com](mailto:overseas_support@service.alibaba.com)）自定义报告名称。

| **报告类型** | **默认报告名称格式** | **示例** |
| --- | --- | --- |
| 交易详情报告 | `transactionItems_<交易日期>_000.csv` | `transactionItems_20181225_000.csv` |
| 结算详情报告 | `settlementItems_<结算货币>_<结算批次ID>_000.csv` | `settlementItems_USD_202*************234_000.csv` |
| 结算汇总报告 | `settlementSummary_<结算货币>_<结算批次ID>_000.csv` | `settlementSummary_USD_202*************234_000.csv` |

**表2. 不同报告的默认报告名称**

报告名称格式中的概念解释如下：

*   **transactionDate**: 交易的日期。
*   **settlementCurrency**: 合同中指定的结算货币。与结算报告中的结算货币相同。
*   **settlementBatchId**: 与报告中结算批次ID对应的结算批次ID。
### 支付宝全球商家平台  
要通过[支付宝全球商家平台](https://global.alipay.com/ilogin/account_login.htm?_route=QK)获取实时对账报告或特定批次的对账报告，请按照以下步骤操作：  
1. 登录平台并找到**账务**模块。具体操作请参阅[账务](https://global.alipay.com/docs/ac/merchant_service/billing)。
2. 下载不同类型的报告：  
   * [交易明细报告](https://global.alipay.com/docs/ac/merchant_service/transactions#MS62k)
   * [结算报告](https://global.alipay.com/docs/ac/merchant_service/settlements#WeUoP)  
使用报告进行对账
----------------  
您可以使用以下三种财务报告执行不同的对账任务：  
| **报告类型** | **任务** |
| --- | --- |
| 交易明细报告 | * 将报告中显示的成功交易与您的记录进行比较，确保一致。 * 查看每个交易日的交易详情，包括所有支付和退款记录，确认支付和退款资金。 |
| 结算汇总报告 | * 查看每个结算批次的所有结算汇总数据。 * 与结算详情报告进行对账，检查是否存在任何问题或差异。 |
| 结算详情报告 | * 查看结算批次内每笔交易的具体结算详情。 * 根据每笔特定交易计算总结算金额，并与结算汇总报告进行资金对账。 |  
表3. 报告与任务  
平台功能
========  
除了通过[支付宝全球商家平台](https://intl-sea.alipay.com/ilogin/account_login.htm?_route=QK)下载对账报告外，您还可以使用平台**账务**模块中的以下功能来辅助对账：  
* 搜索实时交易和结算信息
*   查看结算合同信息和结算日历
*   查看余额信息
*   下载服务费发票
更多关于门户中 **账单** 模块的操作详情，请参阅 [账单](https://global.alipay.com/docs/ac/merchant_service/billing)。  
要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。  
![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)  
@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)  

#### 这个页面有帮助吗？  

#### 本页内容  

[报告](#bQZkg "报告")  
[获取报告](#l3AK9 "获取报告")  
[SFTP](#LYsyS "SFTP")  
[服务器登录](#Uva8T "服务器登录")  
[报告下载路径](#gydYT "报告下载路径")  
[支付宝全球商家门户](#jfNCL "支付宝全球商家门户")  
[使用报告进行对账](#kkid7 "使用报告进行对账")  
[门户](#eGvPL "门户")