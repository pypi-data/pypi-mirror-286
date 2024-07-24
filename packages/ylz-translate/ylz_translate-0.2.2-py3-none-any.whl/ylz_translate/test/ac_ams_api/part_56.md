Online payments
---------------

*   Removed the following result codes from the **notifyPayment** interface:

*   KEY\_NOT\_FOUND
*   ACCESS\_DENIED
*   API\_INVALID
*   CLIENT\_INVALID
*   METHOD\_NOT\_SUPPORTED
*   MEDIA\_TYPE\_NOT\_ACCEPTABLE  
    

*   Modified the following to the _Settlement Items_ file name, _Settlement Summary_ file name, and _Transaction Items_ file name:

*   Updated settlementItems\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv to settlementItems\_<pspName>\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv.
*   Updated settlementSummary\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv to settlementSummary\_<pspName>\_<settlementCurrency>\_<settlementBatchId>\_<seq>.csv.
*   Updated transactionItems\_<transactionCurrency>\_<seq>.csv to transactionItems\_<pspName>\_<transactionCurrency>\_<transactionDate>\_<seq>.csv.

In-store payments
-----------------

*   Removed the following result codes from the **notifyPayment** interface: