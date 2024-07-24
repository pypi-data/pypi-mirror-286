结算汇总 | 自动扣款 | 支付宝文档
===============

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fautodebitpay%2Fsettlementsummary)  
[返回首页](../../)

自动扣款  
[概览](/docs/ac/autodebitpay/overview)  
[用户体验](/docs/ac/autodebitpay/user_ex)  
开发  
[最佳实践](/docs/ac/autodebitpay/best_practice)  
其他资源  
结算汇总
==================

2023-06-29 17:25  
结算汇总报告用于向商家提供清算数据信息的总结。每个清算周期提供一份结算汇总报告，包含该期间的交易总数、轧账后的清算金额等其他相关信息。如果在清算周期内没有交易发生，仍会提供汇总文件，但总额为0。

报告路径和名称
====================

结算汇总报告是一个使用UTF-8编码的文本文件。报告的存储路径默认为`/v1/settlements/<商户获取器ID>/<结算日期>/` 加上文件名。文件名因结算模式不同而不同：

**多种支付方式结算：**
报告名称为`settlementSummary_<结算货币>_<结算批次ID>_<序列号>.csv`。

**单一支付方式结算：**
对于支付宝+ MPPs和其他支付方式，报告名称有所不同。

*   对于支付宝+ MPPs：
    *   当支付宝+ MPPs一起结算时：`settlementSummary_CONNECTWALLET_<结算货币>_<结算批次ID>_<序列号>.csv`
*   当使用支付宝+ MPPs（Mobile Payment Providers）单独结算时：`settlementSummary_<pspName>_<settlementCurrency>_<settlementBatchId>_<seq>.csv`
*   对于其他支付方式：`settlementSummary_<paymentMethodType>_<settlementCurrency>_<settlementBatchId>_<seq>.csv`
报告名称中的变量说明：
*   **merchantIdByAcquirer**：支付宝为商家分配的唯一标识。
*   **settlementDate**：结算日期。
*   **pspName**：实际的支付宝+移动支付提供商名称，如GCash。
*   **settlementCurrency**：约定的结算货币，与文件内容中的费用结算货币相同。
*   **settlementBatchId**：与汇总报告中的结算批次号对应的结算批次代码。
*   **seq**：文档序列号。

报告字段
==========

结算汇总文档分为两部分：结算汇总和文件结束符号。文件结束符号`<END>`出现在文件的最后一行作为文件结束标志。结算汇总的详细信息由几个字段及其对应的值表示。下表显示了报告正文中出现的字段详细信息：

| **字段** | **描述** |
| --- | --- |
| settlementBatchId | **必填** 字符串（64）：由收单方分配的唯一ID，用于识别一个结算周期，对应于汇总文件中的结算批次号。如果收单方未分配settlementBatchId，支付宝将生成此ID。 |
| customerId | **必填** 字符串（64）：由收单方分配的唯一ID，用于识别商家。 |
| acquirer | **必填** 字符串（64）：处理交易的收单方名称。这里的收单方特指为商家提供收单和资金结算服务的收单方。 |
| summaryType | **可选** 字符串 (16) 结算摘要的类型。有效值包括：* `AUTHORIZATION`：表示结算批次内的授权支付摘要。 * `PAYMENT`：表示结算批次内的支付摘要。 * `CAPTURE`：表示结算批次内的捕捉摘要。 * `REFUND`：表示结算批次内的退款摘要。 * `CANCEL`：表示结算批次内的取消摘要。 * `DISPUTE`：表示结算批次内的争议摘要。 * `VOID`：表示结算批次内无效授权的摘要。 * `TOTAL`：表示结算批次的总结算摘要。 * `REFUND_REVERSAL`：表示结算批次内的退款反转摘要。退款反转发生在支付方式无法正确处理退款时，资金会返回到您的账户。 |
| settlementTime | **必填** 字符串 (64) 结算文件生成的日期和时间，格式为 ISO 8601 中定义的 `YYYY-MM-DDTHH:MM:SS+hh:mm`。 |
| count | **必填** 整数 表示交易记录的总数。 |
| settlementAmountValue | **必填** 字符串 (16) 对应货币的主要单位中的净结算金额（例如，对于 USD 是美元，对于 JPY 是日元）。当收单方为 Hundsun 且 *summaryType* 的值为 `TOTAL` 时，此参数的值是准确的。当收单方为 Hundsun 且 *summaryType* 的值为其他时，此参数的值可能有偏差。更多详情，请参阅 [示例 4](#VuW21)。 |
| settlementCurrency | **必填** 字符串 (3) *settlementAmountValue* 的货币，由 ISO 4217 中定义的 3 位货币代码指定。 |
| feeAmountValue | **必填** 字符串（16）：由收单方收取的处理费用金额。此参数的值以对应货币的主要单位表示（例如，对于USD为美元，对于JPY为日元）。当收单方为恒生且*summaryType*值为`TOTAL`时，此参数的值准确。当收单方为恒生且*summaryType*为其他值时，此参数的值可能有偏差。更多详情见[示例4](#VuW21)。当收单方为2C2P且使用interchange++定价模型时，此参数的值可能代表错误校正信息。关于错误校正信息的更多信息，见[示例5](#91GHt)。 |
| feeCurrency | **必填** 字符串（3）：*feeAmountValue*的货币代码，按照[ISO 4217](https://www.iso.org/iso-4217-currency-codes.html)定义的3字母货币代码。 |
| taxFeeAmountValue | **可选** 字符串（16）：对应货币的主要单位中的税费金额（例如，对于USD为美元，对于JPY为日元）。当收单方为恒生且*summaryType*值为`TOTAL`时，此参数的值准确。当收单方为恒生且*summaryType*为其他值时，此参数的值可能有偏差。更多详情见[示例4](#VuW21)。 |
| taxFeeCurrency | **可选** 字符串（3）：*taxFeeAmountValue*的货币代码，按照[ISO 4217](https://www.iso.org/iso-4217-currency-codes.html)定义的3字母货币代码。 |
| processingFeeAmountValue | **可选** 字符串（16）：收单方为每笔交易提供的支付处理服务所收取的处理费用金额。此参数的值以对应货币的主要单位表示（例如，对于USD为美元，对于JPY为日元）。 |
| 处理费用币种 | **可选**字符串 (3) | *processingFeeAmountValue* 的币种。值为 [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) 中定义的3位货币代码。 |
| 非保障优惠券金额 | **可选**字符串 (16) | 商家未结算的折扣金额。此参数值以对应货币的大额单位表示（例如，美元对于 USD，日元对于 JPY）。 |
| 非保障优惠券币种 | **可选**字符串 (3) | *nonGuaranteeCouponValue* 的币种。值为 [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) 中定义的3位货币代码。 |
| 争议处理费用 | **可选**字符串 (16) | 支付宝向商家收取的争议处理费用金额。此参数值以对应货币的大额单位表示（例如，美元对于 USD，日元对于 JPY）。 |
| 争议处理费用币种 | **可选**字符串 (3) | *disputeHandlingFee* 的币种。值为 [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) 中定义的3位货币代码。 |
| 争议反向费用 | **可选**字符串 (16) | 当商家不同意争议时，此参数以对应货币的大额单位表示（例如，美元对于 USD，日元对于 JPY）。 |
| 争议反向费用币种 | **可选**字符串 (3) | *disputeReverseFee* 的币种。值为 [ISO 4217](https://www.iso.org/iso-4217-currency-codes.html) 中定义的3位货币代码。 |
| 交互费用金额值 | **可选** 字符串 (16) | 发卡银行收取的费用。此参数的值以对应货币的主要单位表示（例如，对于USD是美元，对于JPY是日元）。当*paymentMethodType*为`CARD`且使用交互式++定价模型时指定此参数。 |
| 交互费用货币 | **可选** 字符串 (3) | *interchangeFeeAmountValue*的货币，以[ISO 4217](https://www.iso.org/iso-4217-currency-codes.html)定义的3字母货币代码表示。当*paymentMethodType*为`CARD`且使用交互式++定价模型时指定此参数。 |
| 方案费用金额值 | **可选** 字符串 (16) | 由卡组织收取的费用。此参数的值以对应货币的主要单位表示（例如，对于USD是美元，对于JPY是日元）。当*paymentMethodType*为`CARD`且使用交互式++定价模型时指定此参数。 |
| 方案费用货币 | **可选** 字符串 (3) | *schemeFeeAmountValue*的货币，以[ISO 4217](https://www.iso.org/iso-4217-currency-codes.html)定义的3字母货币代码表示。当*paymentMethodType*为`CARD`且使用交互式++定价模型时指定此参数。 |
| 收单行附加费金额值 | **可选** 字符串 (16) | 收单行收取的费用。此参数的值以对应货币的主要单位表示（例如，对于USD是美元，对于JPY是日元）。当*paymentMethodType*为`CARD`且使用交互式++定价模型时指定此参数。 |
| 收单行附加费货币 | **可选** 字符串 (3) | *acquirerMarkupAmountValue*的货币，以[ISO 4217](https://www.iso.org/iso-4217-currency-codes.html)定义的3字母货币代码表示。当*paymentMethodType*为`CARD`且使用交互式++定价模型时指定此参数。 |

示例报告
==========
单一支付方式结算
--------------------

在处理在线支付时，单一支付方式结算涉及使用一种特定的支付手段来完成交易。以下是相关步骤和概念的简要说明：

### 1. 用户选择支付方式

用户在结账时从可用的支付选项中选择一种支付方式，例如信用卡、借记卡、支付宝、微信支付等。

### 2. 支付请求

商家系统生成一个支付请求，包含订单详情、金额、商品信息等，发送给支付网关。在蚂蚁金服的场景中，这可能通过API接口实现，如支付宝的`alipay.trade.page.pay`接口。

### 3. 支付网关处理

支付网关接收请求，验证商家和交易信息，并将支付页面或支付二维码呈现给用户。用户在确认支付详情后，输入支付信息，如银行卡号、密码或使用移动支付应用扫描二维码。

### 4. 银行或第三方支付处理

支付信息被发送到相应的银行或第三方支付机构进行处理。蚂蚁金服的支付宝会在此阶段处理交易，确保资金安全转移。

### 5. 实时通知

交易完成后，支付网关会实时向商家系统发送通知，告知交易状态（成功、失败或待处理）。商家系统可以根据这些通知更新订单状态。

### 6. 结算

在交易成功后，资金会从用户账户转移到商家账户。这个过程可能涉及资金清算和结算周期，具体时间取决于支付方式和金融机构的政策。

### 7. 退款和争议处理

如果需要，商家可以处理退款请求。退款流程通常与支付流程相反，资金从商家账户回退到用户账户。在争议情况下，可能需要通过支付平台的争议解决机制来处理。

### 8. 数据分析和报告

商家可以利用支付数据进行销售分析，了解消费者的支付习惯，优化业务策略。蚂蚁金服提供的商户后台通常包含详细的交易报告和分析工具。

### 注意事项

- 确保所有交易符合相关法规和安全标准。
- 保护用户隐私，不泄露支付信息。
- 提供清晰的支付流程和客户服务支持。

以上就是单一支付方式结算的基本流程，适用于包括蚂蚁金服在内的各种在线支付环境。
### 样例1  
2018年12月25日，商户ID为1022188000000000001的商家发生了两笔交易，一笔是支付，另一笔是退款。  
*   支付详情：  
    *   _paymentId_: 2018122519074101000000000112612，同时也是 _transactionId_ 的值。
    *   _paymentAmount_: 18,000 KRW（_transactionAmountValue_），对应结算金额为14.50 USD（_settlementAmountValue_）。
    *   商家支付给支付宝的手续费为600 KRW，结算金额为0.50 USD。
*   退款详情：  
    *   _refundId_: 2018122519074102000000000041675，同时也是 _transactionId_ 的值。
    *   _refundAmount_: 9,000 KRW（_transactionAmountValue_）的退款，对应结算金额为7.25 USD（_transactionAmountValue_）。
    *   支付宝退还给商家的手续费为300 KRW，结算金额为0.25 USD。
2018年12月27日，支付宝将生成名为`settlementSummary_KaKaoPay_USD_2018122611021040123_000.csv`的CSV文件，其中2018122611021040123是当前清算周期的代码。在这个例子中，商户客户ID是1022188000000000001。文件路径为`/v1/settlements/1022188000000000001/20181226/settlementItems_KaKaoPay_USD_2018122611021040123_000.csv`。  
交易明细如下：  
```csv
settlementBatchId,customerId,acquirer,summaryType,settlementTime,count,settlementAmountValue,settlementCurrency,feeAmountValue,feeCurrency,processingFeeAmountValue,processingFeeCurrency,nonGuaranteeCouponValue,nonGuaranteeCouponCurrency,disputeHandlingFee,disputeHandlingFeeCurrency,disputeReverseFee,disputeReverseFeeCurrency,interchangeFeeAmountValue,interchangeFeeCurrency,schemeFeeAmountValue,schemeFeeCurrency,acquirerMarkupAmountValue,acquirerMarkupCurrency
2018122611021040123,1022188000000000001,Alipay_SG,TOTAL,2018-12-26T10:00:00+08:30,2,725,USD,-25,USD,,,,,,,,,,,,,, 
```
请注意，CSV文件中的其他字段（省略的部分）可能包含与交易相关的其他费用和详细信息。
2018122611021040123,1022188000000000001,支付宝新加坡,支付,2018年12月26日10:00:00+08:30,1,1450,美元,-50,美元,,,,,,,,,,,,,,
2018122611021040123,1022188000000000001,支付宝新加坡,退款,2018年12月26日10:00:00+08:30,1,-725,美元,25,美元,,,,,,,,,,,,,,
<END>
### 样例2  
在2018年12月25日的交易日，商户ID为1022188000000000001的商家有两个交易，一个是支付，另一个是退款。  
*   支付信息：  
    *   _paymentId_: 2018122519074101000000000112612，这也是 _transactionId_ 的值。
    *   _paymentAmount_: 18000 KRW（_transactionAmountValue_）的支付，减去1200 KRW（1.00 USD）的非保证优惠券，对应结算金额为13.50 USD（_settlementAmountValue_）。
    *   商家支付给支付宝的手续费为600 KRW，结算为0.50 USD。
*   退款信息：  
    *   _refundId_: 2018122519074102000000000041675，这也是 _transactionId_ 的值。
    *   _refundAmount_: 9000 KRW（_transactionAmountValue_）的退款，包括600 KRW（0.50 USD）的非保证优惠券，对应结算金额为6.75 USD（_transactionAmountValue_）。
    *   支付宝退还给商家的手续费为300 KRW，结算为0.25 USD。
2018年12月27日，支付宝将生成名为`settlementSummary_KaKaoPay_USD_2018122611021040123_000.csv`的CSV文件，其中2018122611021040123是当前清算周期的代码。  
交易详情如下：  
```csv
settlementBatchId,customerId,acquirer,summaryType,settlementTime,count,settlementAmountValue,settlementCurrency,feeAmountValue,feeCurrency,processingFeeAmountValue,processingFeeCurrency,nonGuaranteeCouponValue,nonGuaranteeCouponCurrency,disputeHandlingFee,disputeHandlingFeeCurrency,disputeReverseFee,disputeReverseFeeCurrency,interchangeFeeAmountValue,interchangeFeeCurrency,schemeFeeAmountValue,schemeFeeCurrency,acquirerMarkupAmountValue,acquirerMarkupCurrency
2018122611021040123,1022188000000000001,Alipay_SG,TOTAL,2018-12-26T10:00:00+08:30,2,725,USD,-25,USD,,,,,,,,,,,,,,
2018122611021040123,1022188000000000001,Alipay_SG,PAYMENT,2018-12-26T10:00:00+08:30,1,1450,USD,-50,USD,,,0,USD,,,,,,,,,,
```
请注意，CSV文件中的省略部分可能包含其他费用或详细信息，如退款、争议处理费等。
2018122611021040123,1022188000000000001,支付宝新加坡,退款,2018年12月26日10:00:00+08:30,1,-725,美元,25,美元,,,,,,,,,,,,,,
<END>
### 样例 3  
2018年12月25日没有交易记录。2018年12月26日，支付宝生成了一个CSV文件，文件名为`settlementSummary_KaKaoPay_USD_0000000000000000000_000.csv`。  
交易详情如下：  
复制  
settlementBatchId, customerId, acquirer, summaryType, settlementTime, count, settlementAmountValue, settlementCurrency, feeAmountValue, feeCurrency, processingFeeAmountValue, processingFeeCurrency, nonGuaranteeCouponValue, nonGuaranteeCouponCurrency, disputeHandlingFee, disputeHandlingFeeCurrency, disputeReverseFee, disputeReverseFeeCurrency, interchangeFeeAmountValue, interchangeFeeCurrency, schemeFeeAmountValue, schemeFeeCurrency, acquirerMarkupAmountValue, acquirerMarkupCurrency  
<END>
### 样例4  
当收单机构为恒生电子时，支付宝会为商家计算每种交易类型的结算数据，因为恒生电子仅提供总结算数据。支付宝和恒生电子计算的总结算数据可能不同，因此支付宝提供金额计算差异的纠错信息。例如：  
*   如果恒生电子和支付宝计算的总_settlementAmountValue_分别为`37164`和`37140`，那么_settlementAmountValue_的纠错信息为`24`。
*   如果恒生电子和支付宝计算的总_feeAmountValue_分别为`760`和`760`，那么_feeAmountValue_的纠错信息为`0`。
*   如果恒生电子和支付宝计算的总_taxFeeAmountValue_分别为`76`和`100`，那么_taxFeeAmountValue_的纠错信息为`-24`。  
**注意**：  
*   商家以恒生电子的最终结算金额进行结算。
*   纠错信息位于结算文件的倒数第二行。  
2022年10月17日，一位商家有三笔交易，两笔支付和一笔退款，其收单机构为恒生电子。在2022年10月19日的结算日，支付宝生成了一个名为`settlementItems_PAYPAY_JPY_2022101909031102123_000.csv`的CSV文件。  
复制  
settlementBatchId,customerId,acquirer,summaryType,settlementTime,count,settlementAmountValue,settlementCurrency,feeAmountValue,feeCurrency,taxFeeAmountValue,taxFeeCurrency,processingFeeAmountValue,processingFeeCurrency,nonGuaranteeCouponValue,nonGuaranteeCouponCurrency,interchangeFeeAmountValue,interchangeFeeCurrency,schemeFeeAmountValue,schemeFeeCurrency,acquirerMarkupAmountValue,acquirerMarkupCurrency
2022101909031102123,Oxxxx742,恒生电子,PAYMENT,2022-10-30T23:00:00+08:00,2,192,JPY,8,JPY,0,JPY,,,,,,,,,,
2022101909031102123,Oxxxx742,恒生电子,REFUND,2022-10-30T23:00:00+08:00,1,-96,JPY,-4,JPY,0,JPY,,,,,,,,,,
2022101909031102123,订单号Oxxxx742,供应商Hundsun,类型:全部,截止时间:2022年10月30日23:00(北京时间),总数量:4,总金额:96日元,税费:4日元,折扣:3日元,,,,,,,,,
2022101909031102123,订单号Oxxxx742,供应商Hundsun,类型:默认,截止时间:2022年10月30日23:00(北京时间),数量:1,金额:0日元,税费:0日元,折扣:3日元,,,,,,,,,
<END>
### 样例5
Interchange++是一种定价模型，它包括由相关发卡银行、卡组织和收单机构对每笔交易处理所收取的费用。这种定价模型透明，因为它提供了最详细的费用分解。Interchange++定价模型包括以下三种费用类型：

*   **交换费**：由发卡银行收取的费用。
*   **卡组织费**（first+）：由卡组织收取的费用。
*   **收单费**（second+）：由收单机构收取的费用。

当收单机构是2C2P，并使用Interchange++定价模型时，结算报告可能包含错误修正信息。错误修正信息表示应收取的费用与实际收取的费用之间的差异，体现在结算报告的倒数第二行的`feeAmountValue`字段中。

*   如果`feeAmountValue`的值为正，意味着应收取的费用少于实际收取的费用，收单机构需要向您退还差额费用。
*   如果`feeAmountValue`的值为负，意味着应收取的费用多于实际收取的费用，您需要向收单机构支付差额费用。

收单机构不定期将错误修正信息发送给支付宝。支付宝通过结算报告将这些信息传递给您。

例如，以下结算汇总报告返回时，报告的倒数第二行显示了额外的错误修正信息：

```
（示例报告内容，此处应提供具体报告的Markdown格式数据，但原问题中未提供，故无法翻译具体内容）
```

请注意，实际报告中的Markdown格式数据应包含具体的数值和日期等信息，以便进行详细的解读和处理。
结算批次ID,客户ID,收单机构,摘要类型,结算时间,计数,结算金额,结算货币,费用金额,费用货币,税金费用金额,税金货币,处理费金额,处理费货币,非保证优惠券金额,非保证优惠券货币,争议处理费,争议处理费货币,争议反向费用,争议反向费用货币,交换费金额,交换费货币,方案费金额,方案费货币,收单方加价金额,收单方加价货币,,,,,,,,,,,,,,,,,,,
2C2PXXXXXX0101,0xxxx742,2C2P新加坡,CAPTURE,2023-01-09 02:45:29+08:00,1,96,港币,-4,港币,0,港币,,,,,,,,,-1,港币,-2,港币,-1,港币,,,,,,,,,,,,,,,,,,,
2C2PXXXXXX0101,0xxxx742,2C2P新加坡,TOTAL,2023-01-09 02:45:29+08:00,2,91,港币,-9,港币,0,港币,,,,,,,,,-1,港币,-2,港币,-1,港币,,,,,,,,,,,,,,,,,,,
2C2PXXXXXX0101,0xxxx742,2C2P新加坡,默认,2022-10-30 23:00:00+08:00,1,,,-5,新加坡元,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
<END>  
请注意以下信息：  
*   **结算金额**（_摘要类型_ = `CAPTURE`）：96
*   **结算货币**（_摘要类型_ = `CAPTURE`）：港币
*   **费用金额**（_摘要类型_ = `TOTAL`）：91
*   **费用货币**（_摘要类型_ = `TOTAL`）：港币
*   **费用金额**（_摘要类型_ = `默认`）：-5
*   **费用货币**（_摘要类型_ = `默认`）：港币  
在上述报告中，当_摘要类型_为`TOTAL`时，_费用金额_为负值，费用货币为港币，这意味着需要向收单机构额外支付5港币。在该结算批次中只有一个交易，其_摘要类型_为`CAPTURE`，结算金额为96港币。因此，最终结算金额是`96`（_摘要类型_ = `CAPTURE`）和`-5`（_摘要类型_ = `默认`）的和，即`91`（_摘要类型_ = `TOTAL`）。  
> **注意**：在同一个批次中，结算详细报告和结算汇总报告返回的错误修正信息是相同的。  
多种支付方式的结算
```markdown
# 蚂蚁金服技术文档：支付接口指南

## 1. 简介
蚂蚁金服支付接口提供了一种安全、高效的在线支付解决方案，适用于各种电子商务和移动应用。本指南将帮助开发者理解和集成此接口。

## 2. 注册与认证
在开始使用支付接口之前，开发者需要在蚂蚁金服开放平台注册并完成企业认证。请访问[注册页面](https://open.alipay.com/register)进行注册。

## 3. 获取AppID
成功注册并认证后，您将在商户后台看到一个唯一的AppID，这是您的应用在蚂蚁金服平台的身份标识。

## 4. SDK下载
请从[SDK下载页面](https://docs.alipay.com/mini/developer/getting-started)获取适用于您平台的SDK，包括iOS、Android和Web。

## 5. 配置密钥
在商户后台，您需要生成并配置公钥和私钥，用于接口调用时的数据加密和解密。

## 6. 支付接口调用
调用支付接口的基本步骤如下：
1. 构建请求参数，包括商品信息、订单金额等。
2. 使用私钥对请求参数进行签名。
3. 调用支付接口，将签名后的参数发送给蚂蚁金服。
4. 收到蚂蚁金服的响应，验证签名并处理结果。

## 7. 支付结果通知
蚂蚁金服会通过异步通知的方式将支付结果发送到您配置的回调URL。请确保该URL可访问并处理这些通知。

## 8. 异常处理与调试
在集成过程中，可能会遇到各种错误。请参考[错误码文档](https://docs.alipay.com/mini/api/errcode)进行排查。

## 9. 安全最佳实践
遵循以下建议以确保交易安全：
- 保护好您的私钥，避免泄露。
- 使用HTTPS进行通信，确保数据传输安全。
- 定期更新SDK，获取最新的安全特性。

## 10. 支持与社区
如果您在集成过程中遇到问题，可以访问[开发者论坛](https://openclub.alipay.com/)寻求帮助，或联系我们的技术支持。

---

# 蚂蚁金服技术文档：支付接口指南

## 1. 简介
蚂蚁金服的支付接口提供安全、快捷的在线支付服务，适用于电商和移动应用。本指南旨在指导开发者集成此接口。

## 2. 注册与认证
在使用支付接口前，开发者需在蚂蚁金服开放平台注册并完成企业验证。请访问[注册链接](https://open.alipay.com/register)。

## 3. 获取AppID
注册认证后，您将在商户后台看到一个唯一的AppID，作为您应用在蚂蚁金服平台的身份标识。

## 4. SDK下载
请从[SDK下载区](https://docs.alipay.com/mini/developer/getting-started)获取适合您平台的SDK，包括iOS、Android和Web版本。

## 5. 配置密钥
在商户后台生成并设置公钥和私钥，用于接口调用时的数据加密和解密。

## 6. 调用支付接口
调用接口的基本流程：
1. 组织请求参数，如商品详情、交易金额等。
2. 使用私钥对参数进行签名。
3. 调用支付接口，发送签名后的参数给蚂蚁金服。
4. 接收并验证蚂蚁金服的响应，处理交易结果。

## 7. 支付结果通知
蚂蚁金服会通过异步通知您的回调URL来发送支付结果。请确保URL可达并能处理这些通知。

## 8. 异常处理与调试
遇到问题时，参考[错误码文档](https://docs.alipay.com/mini/api/errcode)进行故障排除。

## 9. 安全最佳实践
遵循以下建议以保障交易安全：
- 严格保管私钥，防止泄露。
- 使用HTTPS协议进行通信，保证数据传输安全。
- 定期更新SDK，获取最新安全功能。

## 10. 支持与社区
如在集成中遇到困难，可访问[开发者论坛](https://openclub.alipay.com/)寻求帮助，或直接联系我们的技术支持团队。
```

请注意，由于Markdown格式的限制，部分链接可能无法直接点击，需要手动复制到浏览器中打开。
### 样例1  
在2018年12月25日的交易日，商户ID为1022188000000000001发生了两笔交易，一笔是支付，另一笔是退款。  
*   支付信息：  
    *   _paymentId_: 2018122519074101000000000112612，这也是 _transactionId_ 的值。
    *   _paymentAmount_: 18,000 KRW (_transactionAmountValue_)，对应结算金额为14.50 USD (_settlementAmountValue_)。
    *   商户支付给支付宝的手续费为600 KRW，结算金额为0.50 USD。
*   退款信息：  
    *   _refundId_: 2018122519074102000000000041675，这也是 _transactionId_ 的值。
    *   _refundAmount_: 9,000 KRW (_transactionAmountValue_) 的退款，对应结算金额为7.25 USD (_transactionAmountValue_)。
    *   支付宝退还给商户的手续费为300 KRW，结算金额为0.25 USD。
在2018年12月26日，支付宝将生成名为 `settlementSummary_USD_2018122611021040123_000.csv` 的CSV文件，其中2018122611021040123是当前清算周期的代码。商户客户ID为1022188000000000001。文件路径为 `/v1/settlements/1022188000000000001/20181226/settlementSummary_USD_2018122611021040123_000.csv`。  
交易详情如下：  
```csv
settlementBatchId,customerId,acquirer,summaryType,settlementTime,count,settlementAmountValue,settlementCurrency,feeAmountValue,feeCurrency,processingFeeAmountValue,processingFeeCurrency,nonGuaranteeCouponValue,nonGuaranteeCouponCurrency,disputeHandlingFee,disputeHandlingFeeCurrency,disputeReverseFee,disputeReverseFeeCurrency,interchangeFeeAmountValue,interchangeFeeCurrency,schemeFeeAmountValue,schemeFeeCurrency,acquirerMarkupAmountValue,acquirerMarkupCurrency
2018122611021040123,1022188000000000001,Alipay_SG,TOTAL,2018-12-26T10:00:00+08:30,2,725,USD,-25,USD,,,,,,,,,,,,,, 
```
请注意，CSV文件中的省略部分表示没有提供具体数值或不适用。
2018122611021040123,1022188000000000001,支付宝新加坡,支付,2018年12月26日10:00:00+08:30,1,1450,美元,-50,美元,,,,,,,,,,,,,,
2018122611021040123,1022188000000000001,支付宝新加坡,退款,2018年12月26日10:00:00+08:30,1,-725,美元,25,美元,,,,,,,,,,,,,,
<END>
### 示例2  
2018年12月25日，商户ID为1022188000000000001的商家发生了两笔交易，一笔是支付，另一笔是退款。

*   支付详情：
    *   _paymentId_: 2018122519074101000000000112612，同时也是 _transactionId_ 的值。
    *   _paymentAmount_: 18,000 KRW（_transactionAmountValue_）的支付金额，减去1,200 KRW（1.00 USD）的非保证优惠券，对应结算金额为13.50 USD（_settlementAmountValue_）。
    *   商家支付给支付宝的手续费为600 KRW，结算为0.50 USD。
*   退款详情：
    *   refundId: 2018122519074102000000000041675，同样是 _transactionId_ 的值。
    *   refundAmount: 9,000 KRW（_transactionAmountValue_）的退款，包括600 KRW（0.50 USD）的非保证优惠券，对应结算金额为6.75 USD（_transactionAmountValue_）。
    *   支付宝退还给商家的手续费为300 KRW，结算为0.25 USD。

2018年12月26日，支付宝将生成名为`settlementSummary_USD_2018122611021040123_000.csv`的CSV文件，其中2018122611021040123是当前清算周期的代码。

交易详情如下：

```
settlementBatchId,customerId,acquirer,summaryType,settlementTime,count,settlementAmountValue,settlementCurrency,feeAmountValue,feeCurrency,processingFeeAmountValue,processingFeeCurrency,nonGuaranteeCouponValue,nonGuaranteeCouponCurrency,disputeHandlingFee,disputeHandlingFeeCurrency,disputeReverseFee,disputeReverseFeeCurrency,interchangeFeeAmountValue,interchangeFeeCurrency,schemeFeeAmountValue,schemeFeeCurrency,acquirerMarkupAmountValue,acquirerMarkupCurrency
2018122611021040123,1022188000000000001,支付宝_SG,TOTAL,2018-12-26T10:00:00+08:30,2,725,USD,-25,USD,,,,,,,,,,,,,,
2018122611021040123,1022188000000000001,支付宝_SG,PAYMENT,2018-12-26T10:00:00+08:30,1,1450,USD,-50,USD,,,0,USD,,,,,,,,,,
```

请注意，省略的部分表示CSV文件中可能存在的其他列，但在此示例中未提供具体数值。
2018122611021040123,1022188000000000001,支付宝新加坡,退款,2018年12月26日10:00:00+08:30,1,-725,美元,25,美元,,,,,,,,,,,,,,
<END>
### 样例 3  
2018年12月25日没有交易记录。2018年12月26日，支付宝生成了一个CSV文件，文件名为`settlementSummary_USD_2018122611021040123_000.csv`，其中2018122611021040123是当前清算周期的代码。  
交易详情如下：  
（此处省略了交易详情数据，因为它们是Markdown格式的纯文本表格，无法直接显示。）  
要查看文档的最新更新，请访问[版本说明](https://global.alipay.com/docs/releasenotes)。  
![图片 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)  
@2024 支付宝 [法律信息](https://global.alipay.com/docs/ac/platform/membership)  
#### 这个页面有帮助吗？  
#### 本页面内容  
[报告路径和名称](#qzhvy "报告路径和名称")  
[报告字段](#0Uxw9 "报告字段")  
[报告样例](#AJcpI "报告样例")  
[单一支付方式结算](#ZB65G "单一支付方式结算")  
[样例 1](#jJVqt "样例 1")  
[样例 2](#wN9xX "样例 2")  
[样例 3](#MSk1A "样例 3")  
[样例 4](#VuW21 "样例 4")  
[样例 5](#91GHt "样例 5")  
[多种支付方式结算](#ykN0G "多种支付方式结算")  
[样例 1](#eiTGm "样例 1")  
[样例 2](#Cn3hy "样例 2")  
[样例 3](#MqT6k "样例 3")