| 错误代码 | 是否可上诉 | 描述 | 解决方案 |
| --- | --- | --- | --- |
| AUTHENTICATION\_REQUIRED | F | 需要3D Secure验证。 | 重新启动支付流程，并引导用户进行3D Secure验证。 |
| SELECTED\_CARD\_BRAND\_NOT\_AVAILABLE | F | 用户选择的支付卡品牌不可用。 | 用户选择的支付卡品牌不可用。 |
| PAYMENT\_PROHIBITED | F | 由于商品在该国家禁止销售，无法处理支付。 | 该交易不允许申诉。 |
| INVALID\_EXPIRATION\_DATE | F | paymentMethod.paymentMethodMetaData.expiryYear 或 paymentMethod.paymentMethodMetaData.expiryDate 的值无效。 | 检查 _paymentMethod.paymentMethodMetaData.expiryYear_ 或 _paymentMethod.paymentMethodMetaData.expiryDate_ 的值是否正确：

1.  如果不正确，请传入正确的值。
2.  如果正确，请联系支付宝技术支持获取详细原因。 |