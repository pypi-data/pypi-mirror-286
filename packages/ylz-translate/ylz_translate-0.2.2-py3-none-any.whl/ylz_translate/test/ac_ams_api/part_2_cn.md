支付宝分配的用于识别支付的唯一ID。

关于此字段的更多信息：

*   最大长度：64 个字符

#### declarationAmount Amount 对象 **必需**

累计交易申报金额，不能超过总交易金额。仅支持中国海关申报。默认货币为 `CNY`（人民币）。

注意：此字段可以从 **notifyPayment** 请求和 **inquiryPayment** 响应中的 `_customsDeclarationAmount` 字段获取。

显示子参数

#### customs CustomsInfo 对象 **必需**

海关信息

显示子参数

#### merchantCustomsInfo MerchantCustomsInfo 对象 **必需**

在海关系统中注册的商家信息。

显示子参数

#### splitOrder 布尔值 **必需**