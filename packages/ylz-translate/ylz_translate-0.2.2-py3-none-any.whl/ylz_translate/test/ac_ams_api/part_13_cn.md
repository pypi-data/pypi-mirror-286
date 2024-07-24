*   _declarationRequestId_ 必须与原始请求相同，否则将被视为新的请求。
*   在重新传输中，仅能修改 _merchantCustomsCode_、_merchantCustomsName_、_customsPlace_、_declarationAmount_、suborderId 和 _buyer_。重新传输的 _declarationAmount_ 不计入海关申报的总金额。

**重新传输条件**

在重新触发接口之前，请确保满足以下条件：

*   支付宝系统中存在与 _declarationRequestId_ 相同的申报记录。
*   自上次调用以来已超过5分钟。（支付宝可能会根据实际情况调整此时间值。）
*   除了以下字段的值外，所有信息应保持不变：

*   _merchantCustomsCode_
*   _merchantCustomsName_
*   _customsPlace_ 
*   _declarationAmount_
*   _suborderId_
*   _buyerCertificate.holderName.fullName_ 
*   _buyerCertificate.certificateNo_