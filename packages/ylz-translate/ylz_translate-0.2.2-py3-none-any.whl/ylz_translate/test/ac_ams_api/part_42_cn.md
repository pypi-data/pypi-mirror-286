*   authExpiryTime
*   redirectActionForm
*   交易.transactionType: 支付, 取消, 授权, 捕获, 作废
*   交易时间

*   将以下字段从可选改为必需:

*   响应参数:

*   result
*   result.resultMessage
*   交易.transactionId

*   添加了以下两个结果代码表:

*   支付结果代码
*   交易结果代码

*   删除了以下错误代码:

*   RISK\_REJECT
*   USER\_KYC\_NOT\_QUALIFIED

**更新了** **_取消_** **文档:**

*   将以下字段从可选改为必需:

*   响应参数:

*   result.resultMessage

**更新了** **_退款_** **文档:**

*   将以下字段从可选改为必需:

*   响应参数:

*   result.resultMessage

*   添加了以下错误代码:

*   INVALID\_MERCHANT\_STATUS
*   ORDER\_IS\_CLOSED  

**更新了** **_查询退款_** **文档:**