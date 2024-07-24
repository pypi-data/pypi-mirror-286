在线支付
--------------

*   从**notifyPayment**接口中移除了以下结果代码：

    *   KEY\_NOT\_FOUND
    *   ACCESS\_DENIED
    *   API\_INVALID
    *   CLIENT\_INVALID
    *   METHOD\_NOT\_SUPPORTED
    *   MEDIA\_TYPE\_NOT\_ACCEPTABLE  

*   修改了以下内容，涉及“结算项目”文件名、“结算汇总”文件名和“交易项目”文件名：

    *   将settlementItems\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv 更新为settlementItems\_<pspName>\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv。
    *   将settlementSummary\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv 更新为settlementSummary\_<pspName>\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv。
    *   将transactionItems\_<transactionCurrency>\_<seq>.csv 更新为transactionItems\_<pspName>\_<transactionCurrency>\_<transactionDate>\_<seq>.csv。

店内支付
-------------

*   从**notifyPayment**接口中移除了以下结果代码：