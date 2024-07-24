版本更新 | 阿里巴巴支付宝，中国领先的第三方在线支付解决方案
==================================================

[![图片1：阿里巴巴支付宝，中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg) ![图片2：阿里巴巴支付宝，中国领先的第三方在线支付解决方案](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Freleasenotes)  
[首页](/docs/)  
[在线支付](/docs/onlinepayment)  
[店内支付](/docs/instorepayment)  
[解决方案](/docs/solutions)  
[收益增强器](/docs/ac/revenuebooster_en/overview)  
[合并支付](/docs/ac/combinedpay_en/overview)  
[灵活结算](/docs/ac/flexiblesettlement_en/overview)  
[集成指南](/docs/integration_guide_en)  
[Antom仪表盘](/docs/dashboard_en)  
[SDKs](/docs/sdks)  
[APIs](https://global.alipay.com/docs/ac/ams/api)  
[对账](https://global.alipay.com/docs/ac/reconcile)  
[数字签名](https://global.alipay.com/docs/ac/ams/digital_signature)  
[沙箱环境](https://global.alipay.com/docs/ac/ref/sandbox)  
[工具](https://global.alipay.com/docs/ac/ref/key_config_en)  
[测试钱包](https://global.alipay.com/docs/ac/ref/testwallet)  
[争议处理](https://global.alipay.com/docs/ac/dispute)  
[商家服务](https://global.alipay.com/docs/ac/merchant_service)  
[版本更新](/docs/releasenotes)  
[支持](/docs/support)  
[词汇表](/docs/glossary)  
[帮助中心](https://cshall.alipay.com/enterprise/global/klgList?sceneCode=un_login&routerId=d9aa1f608c4145d6b3c8030c17cf6f9a000&categoryId=50479)  
[旧版文档](https://global.alipay.com/docs/ac/legacy/legacydoc)  

订阅更新
------------

订阅产品更新，通过电子邮件接收文档更新的通知。您可以通过右侧的“取消订阅”按钮或每封邮件通知中的链接取消订阅。

订阅
------------

版本更新
==========

2024年4月3日 03:29  
2024年3月
----------
### 增强功能  
*   在[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)、[**查询支付**](https://global.alipay.com/docs/ac/ams/paymentri_online)和[**通知支付**](https://global.alipay.com/docs/ac/ams/paymentrn_online)API中添加了_funding_和_cardCategory_字段。
*   在[**咨询（结账支付）**](https://global.alipay.com/docs/ac/ams/consult)API中添加了_funding_字段。
*   在[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)API中添加了_requireIssuerAuthentication_字段。
*   更新了[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)API中_selectedCardBrand_字段的描述。
*   在[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)、[**创建支付会话（结账支付）**](https://global.alipay.com/docs/ac/ams/session_cashier)和[**决定**](https://global.alipay.com/docs/ac/risk_control/decide)API中添加了_transit_、_lodging_和_gaming_字段。
*   添加了嵌入式Web/WEP卡支付集成指南。  
2024年2月
-------------  
### 增强功能  
*   添加了[**接受争议**](https://global.alipay.com/docs/ac/ams/accept)、[**提供防御文件**](https://global.alipay.com/docs/ac/ams/supply_evidence)、[**下载争议证据**](https://global.alipay.com/docs/ac/ams/download)和[**通知争议**](https://global.alipay.com/docs/ac/ams/notify_dispute)的争议相关API。
*   在[**通知争议**](https://global.alipay.com/docs/ac/ams/notify_dispute)API的_disputeNotificationType_字段中添加枚举值`DEFENSE_DUE_ALERT`。
*   更新了[**通知争议**](https://global.alipay.com/docs/ac/ams/notify_dispute)API中_defenseDueTime_字段的描述。  
2024年1月
------------  
### 增强功能  
*   在[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)文档中添加了Yapily支付方法。
*   在[**创建**](https://global.alipay.com/docs/ac/ams/create_sub)API中添加了_paymentMethodId_字段。
*   在[**创建**](https://global.alipay.com/docs/ac/ams/create_sub)API的_paymentMethodType_字段中添加枚举值`CARD`。
*   更新了[**创建**](https://global.alipay.com/docs/ac/ams/create_sub)API中_subscriptionEndTime_字段的描述。
*   在[**通知支付**](https://global.alipay.com/docs/ac/ams/notify_subpayment)API中添加了_phaseNo_字段。  
2023年12月
-------------  
### 增强功能  
*   在[**咨询**](https://global.alipay.com/docs/ac/ams/authconsult)API中添加了K PLUS的示例代码。
*   在[**查询支付**](https://global.alipay.com/docs/ac/ams/paymentri_online)API的响应中添加了_authExpiryTime_字段。
*   更新了[测试钱包](https://global.alipay.com/docs/ac/ref/testwallet)文档中Android版本测试钱包的下载链接。
*   在以下API中添加了错误代码`INVALID_AMOUNT`：[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)、[**通知支付**](https://global.alipay.com/docs/ac/ams/paymentrn_online)、[**查询支付**](https://global.alipay.com/docs/ac/ams/paymentri_online)。
*   更新了[**通知授权**](https://global.alipay.com/docs/ac/ams/notifyauth)API中_authorizationNotifyType_字段的枚举值`TOKEN_CREATED`的描述。
*   更新了Easy Pay的Web/WEP、[Android](https://global.alipay.com/docs/ac/easypay_en/android_en)和[iOS](https://global.alipay.com/docs/ac/easypay_en/ios_en)集成指南中的组件名称`AMSEasyPay`。
*   更新了结账支付的卡支付Web/WEP、[Android](https://global.alipay.com/docs/ac/cashierpay/android)和[iOS](https://global.alipay.com/docs/ac/cashierpay/ios)集成指南中的组件名称`AMSCashierPayment`。
*   更新了结账支付的银行相关支付Web/WEP、[Android](https://global.alipay.com/docs/ac/cashierpay/bank_android)和[iOS](https://global.alipay.com/docs/ac/cashierpay/bank_ios)集成指南中的组件名称`AMSCashierPayment`。  
2023年11月
-------------  
### 增强功能  
*   在[**退款**](https://global.alipay.com/docs/ac/ams/refund_online)API中添加了错误代码`ORDER_IS_CANCELED`。
*   在Easy Pay的[Android](https://global.alipay.com/docs/ac/easypay_en/android_en)集成指南中添加了事件代码`SDK_PAYMENT_CANCEL`。
*   在[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)文档中添加了Pagaleve和Bancomat Pay支付方式。
*   在[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)API的_paymentMethod.paymentMethodMetaData_字段中添加了Pagaleve的场景。
*   更新了[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)API中_order.buyer_和_order.buyer.buyerPhoneNo_字段的描述。
*   为Vault功能添加了[**创建VaultingSession**](https://global.alipay.com/docs/ac/ams/vaulting_session)、[**vaultPaymentMethod**](https://global.alipay.com/docs/ac/ams/vault_method)、[**通知Vaulting**](https://global.alipay.com/docs/ac/ams/notify_vaulting)和[**查询Vaulting**](https://global.alipay.com/docs/ac/ams/inquire_vaulting)API。
*   为银行相关支付添加了Web/WEP、[Android](https://global.alipay.com/docs/ac/cashierpay/bank_android)和[iOS](https://global.alipay.com/docs/ac/cashierpay/bank_ios)集成指南。
*   更新了Easy Pay的Web/WEP、[Android](https://global.alipay.com/docs/ac/easypay_en/android_en)和[iOS](https://global.alipay.com/docs/ac/easypay_en/ios_en)集成指南中的代码示例。  
店内支付  
*   在[**取消**](https://global.alipay.com/docs/ac/ams/paymentc)API中添加了错误代码`ORDER_STATUS_INVALID`。
*   在[**退款**](https://global.alipay.com/docs/ac/ams/refund)API中添加了错误代码`ACCESS_DENIED`和`ORDER_IS_CANCELED`。
### 已废弃  
移除了GAGW使用的域名：[https://open-global.alipay.com](https://open-global.alipay.com)。  
2023年10月  
-----------
### 增强功能  
*   在[**pay（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier) API 的字段 _order.buyer.buyerEmail_，_order.buyer.buyerEmail.buyerPhoneNo_，_order.buyer.buyerEmail.buyerName.firstName_ 和 _order.buyer.buyerEmail.buyerName.lastName_ 中，添加了 KONBINI，BANKTRANSFER\_PAYEASY 和 ONLINEBANKING\_PAYEASY 的使用场景。
*   向 [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online)，[**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) 和 [**pay（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier) API 添加了错误代码 `DO_NOT_HONOR`。
*   在 [createPaymentSession（结账支付）](https://global.alipay.com/docs/ac/ams/session_cashier) 文档的 _paymentFactor.captureMode_ 字段中，为卡支付添加了自动扣款功能。
*   更新了 [非卡支付](https://global.alipay.com/docs/ac/cashierpay/noncard_payment) 文档中的 LINE Pay，Pay-easy 和 Konbini 集成解决方案。
*   在结账支付文档中添加了 [快速入门](https://global.alipay.com/docs/ac/cashierpay/quickstart) 和 [测试资源](https://global.alipay.com/docs/ac/cashierpay/test) 文档。
*   在 [支付方式](https://global.alipay.com/docs/ac/ref/payment_method#vgXw6) 文档中添加了支付方式 `DIRECT_DEBIT_SIAMCOMMERCIALBANK` 和 `DIRECT_DEBIT_KRUNGTHAIBANK`。
*   在 [支付方式](https://global.alipay.com/docs/ac/ref/payment_method) 文档中为结账支付添加了 DOKU，KPLUS，Pay-easy 网上银行和 Pay-easy 银行转账。
*   在 [支付方式](https://global.alipay.com/docs/ac/ref/payment_method) 文档中为自动扣款和订阅支付添加了 KPLUS 支付方式。
*   在请求头中添加了可选字段 [_agent-token_](https://global.alipay.com/docs/ac/ams/api_fund#sjPLz)，以授权 ISV 调用 API。
### 已废弃

* 从[**pay（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier) API 的 _paymentMethod.paymentMethodMetaData_ 字段中移除了便利店（Konbini）和轻松付（Pay-easy）的场景。
* 从[**pay（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier) 和 [**pay（自动扣款）**](https://global.alipay.com/docs/ac/ams/payment_agreement) API 中删除了错误代码 INVALID_API。
* 废弃了轻松付（Pay-easy）的支付方式（枚举值为 `PAYEASY`）。

2023年9月
### 增强  
*   在[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier) API 中添加了字段 _paymentFactor.captureMode_。
*   修改了[**查询支付**](https://global.alipay.com/docs/ac/ams/paymentri_online)和[**支付通知**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API 中的 _paymentResultInfo_ 字段描述。
*   在[**查询支付**](https://global.alipay.com/docs/ac/ams/paymentri_online)和[**支付通知**](https://global.alipay.com/docs/ac/ams/paymentrn_online) API 中添加了字段 _WalletPaymentResultInfo.creditPayPlan_、_paymentResultInfo.funding_ 和 _WalletPaymentResultInfo.creditPayPlan.installmentNu_。
*   修改了[**支付（结账支付）**](https://global.alipay.com/docs/ac/ams/payment_cashier)和[**创建支付会话（结账支付）**](https://global.alipay.com/docs/ac/ams/session_cashier) API 中的字段 _order.shipping.shippingAddress.state_、_order.shipping.shippingAddress.zipCode_、_paymentMethod.paymentMethodMetaData.billingAddress.state_ 和 _paymentMethod.paymentMethodMetaData.billingAddress.zipCode_ 的描述。
*   在[**咨询**](https://global.alipay.com/docs/ac/ams/authconsult) API 中添加了字段 _authCodeForm_。
*   在结账支付文档的[卡支付](https://global.alipay.com/docs/ac/cashierpay/card_payment)、[API 集成](https://global.alipay.com/docs/ac/cashierpay/api)和[捕捉](https://global.alipay.com/docs/ac/cashierpay/capture)部分中，为卡支付添加了自动捕捉功能。
*   在[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)文档中，为结账支付添加了新的支付方式 JKOPay 和 LINE Pay。
*   在对账文档的[交易详情报告](https://global.alipay.com/docs/ac/reconcile/transaction_details)和[结算详情报告](https://global.alipay.com/docs/ac/reconcile/settlement_details)中，将字段 _funding_ 的最大长度从6个字符增加到20个字符。
*   在对账文档的[结算汇总报告](https://global.alipay.com/docs/ac/reconcile/settlement_details)中，向字段 _summaryType_ 添加了枚举值 `COLLATERAL_WITHHOLDING`、`RESERVE_WITHHOLDING`、`RESERVE_RELEASE`。
*   在对账文档的[结算详情报告](https://global.alipay.com/docs/ac/reconcile/settlement_details)中，向字段 _transactionType_ 添加了枚举值 `COLLATERAL_WITHHOLDING`、`RESERVE_WITHHOLDING`、`RESERVE_RELEASE`。
*   在结账支付文档中添加了[设置支付继续URL的最佳实践](https://global.alipay.com/docs/ac/cashierpay/redirection)文档。
*   更新了结算与交易文档。
### 已弃用  
*   对于直接借记和定期订阅，弃用了Dolfin、BPI和bKash的支付方式。对于直接借记和定期订阅，也弃用了Easypaisa的支付方式。  
2023年8月  
-----------
### 增强功能  
*   添加了三个关于商户服务操作的视频教程：[如何退款](https://global.alipay.com/docs/ac/merchant_service/videos#如何退款)，[如何查看交易详情](https://global.alipay.com/docs/ac/merchant_service/videos#如何查看交易详情)和[如何管理发票](https://global.alipay.com/docs/ac/merchant_service/videos#如何管理发票)。
*   添加了增值服务的文档：[收益增强器](https://global.alipay.com/docs/ac/revenuebooster_en/overview)，[组合支付](https://global.alipay.com/docs/ac/combinedpay_en/overview)和[灵活结算](https://global.alipay.com/docs/ac/flexiblesettlement_en)。
*   添加了支付产品的文档：[扫码绑定](https://global.alipay.com/docs/ac/scantopay_en/overview)和[订阅支付](https://global.alipay.com/docs/ac/subscriptionpay_en/overview)。
*   在结账支付文档中添加了[卡支付文档](https://global.alipay.com/docs/ac/cashierpay/card_payment)。
*   在[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)中添加了卡品牌枚举值 `AMEX`，`DISCOVER`，`DINERS`，`CUP`，`JCB`，`MAESTRO` 和 `CARTES_BANCAIRES`。
*   在[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)中添加了订阅支付支持的支付方式。
*   添加了[风险管理方法](https://global.alipay.com/docs/ac/ref/risk_methods)文档。
*   为欧洲商户服务器添加了加速域名 [https://open-de-global.alipay.com](https://open-de-global.alipay.com)。
*   为订阅支付添加了[创建](https://global.alipay.com/docs/ac/ams/create_sub)、[订阅通知](https://global.alipay.com/docs/ac/ams/notify_sub)、[支付通知](https://global.alipay.com/docs/ac/ams/notify_subpayment)、[变更](https://global.alipay.com/docs/ac/ams/change_sub)和[取消](https://global.alipay.com/docs/ac/ams/cancel_sub)API。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)、[支付通知](https://global.alipay.com/docs/ac/ams/paymentrn_online)和[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online)API中添加了错误代码 `CARD_NOT_SUPPORTED`，`USER_BALANCE_NOT_ENOUGH`，`INVALID_EXPIRATION_DATE` 和 `INVALID_CARD_NUMBER`。
*   添加了用于卡支付的[创建支付会话（收银台支付）](https://global.alipay.com/docs/ac/ams/session_cashier)API。
*   更新了[自动扣款](https://global.alipay.com/docs/ac/autodebit_en/overview)文档。新版本提供了重新结构化的集成和操作指南，以遵循支付流程。
*   将产品名称从收银台支付更新为结账支付。
*   更新了[对账](https://global.alipay.com/docs/ac/reconcile)文档。新版本提供了全面的对账信息，包括结算规则和生命周期。
  
### 2023年7月  
#### 增强功能  
*   添加了[创建支付会话（简易支付）](https://global.alipay.com/docs/ac/ams/createpaymentsession_easypay)API，用于简易支付产品。
*   添加了简易支付产品的[英文](https://global.alipay.com/docs/ac/easypay_en/overview_en)和[中文](https://global.alipay.com/docs/ac/easypay/overview)版本的集成指南。
*   在[notifyAuthorization](https://global.alipay.com/docs/ac/ams/notifyauth) API 的请求参数中，字段 _authorizationNotifyType_ 添加了枚举值 `TOKEN_CREATED`。
*   支持了巴西卡和PIX的支付渠道AlipayBR。
### 已弃用  
*   在[收银台支付](https://global.alipay.com/docs/ac/ams/payment_cashier)、[自动扣款支付](https://global.alipay.com/docs/ac/ams/payment_agreement)、[用户出示模式支付](https://global.alipay.com/docs/ac/ams/upm)、[订单码支付](https://global.alipay.com/docs/ac/ams/oc)和[入口码支付](https://global.alipay.com/docs/ac/ams/ec)的请求参数中，弃用了字段`customerId`。  
2023年6月  
--------
### 增强功能  
*   为收银台支付和自动扣款添加了枚举值 `NAVERPAY`，以及为收银台支付添加了 `TOSS`，这些在[_支付方式_](https://global.alipay.com/docs/ac/ref/payment_method)文档中有所说明。
*   添加了[商家服务文档](https://global.alipay.com/docs/ac/merchant_service)，提供了商家操作的教程。
*   添加了[支付宝商家服务风险操作支持](https://global.alipay.com/docs/support#QULaN)的联系信息。
### 文档改进  
*   对收银台支付和自动扣款API请求的域名进行了更新。详细信息请参阅[调用API](https://global.alipay.com/docs/ac/ams/api#call_api)。
*   将`Request-Time`的格式修改为毫秒级精确的时间戳。详细信息请参阅[构建待签名内容](https://global.alipay.com/docs/ac/ams/digital_signature#构建待签名内容)。  
2023年5月
----------
### 改进

*   在《支付方式》([_Payment methods_](https://global.alipay.com/docs/ac/ref/payment_method))中，为收银台支付和自动扣款添加了枚举值 `ZALOPAY`。
*   交易金额现在以主要单位表示。详情请参阅以下文档：
    *   收银台支付的《结算与对账》([_Settle and reconcile_](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle))
    *   收银台支付的《交易项目》([_Transaction Items_](https://global.alipay.com/docs/ac/cashierpay/transactionitems))
    *   收银台支付的《结算项目》([_Settlement Items_](https://global.alipay.com/docs/ac/cashierpay/settlementitems))
    *   收银台支付的《结算汇总》([_Settlement Summary_](https://global.alipay.com/docs/ac/cashierpay/settlementsummary))
    *   自动扣款的《结算与对账》([_Settle and reconcile_](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle))
    *   自动扣款的《交易项目》([_Transaction Items_](https://global.alipay.com/docs/ac/autodebitpay/transactionitems))
    *   自动扣款的《结算项目》([_Settlement Items_](https://global.alipay.com/docs/ac/autodebitpay/settlementitems))
    *   自动扣款的《结算汇总》([_Settlement Summary_](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary))
*   将《咨询》([consult](https://global.alipay.com/docs/ac/ams/authconsult))和《申请令牌》([applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp))API请求参数中的 _customerBelongsTo_ 参数长度从16改为64。
*   将《支付（自动扣款）》([pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement))API请求参数中的 _paymentMethod.paymentMethodType_ 参数长度从32改为64。

---

### 2023年4月更新

*   在《支付方式》([_Payment methods_](https://global.alipay.com/docs/ac/cashierpay/payment_method))中添加了支付方式类型 OTC。
*   在《支付方式》([_Payment methods_](https://global.alipay.com/docs/ac/ref/payment_method))中为收银台支付添加了枚举值 `KREDIVO_ID`。
*   更新了《测试钱包》([_Test wallet_](https://global.alipay.com/docs/ac/ref/testwallet))中Android测试钱包的下载地址。
*   在《查询支付》([inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online))API的响应参数中添加了 _cardInfo.threeDSResult_ 参数。
*   在《查询支付》([inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online))API的请求参数中添加了 _cardInfo.threeDSResult_ 参数。
### 已废弃

*   废弃了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API响应参数中的`_redirectActionForm_`参数。
*   废弃了[咨询](https://global.alipay.com/docs/ac/ams/authconsult)API响应参数中的`_authUrl_`参数。
*   废弃了[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online)API响应参数中的`_cardInfo.eci_`参数。
*   废弃了[通知支付](https://global.alipay.com/docs/ac/ams/paymentrn_online)API请求参数中的`_cardInfo.eci_`参数。
### 文档改进  
*   在《使用非卡支付方式》的《收集或显示额外信息》部分，新增了对Blik的描述，链接为：[https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)。
*   更新了API [pay (收银台支付)](https://global.alipay.com/docs/ac/ams/payment_cashier) 请求参数中，针对Blik支付方式的参数 _order.env.clientIp_ 和 _order.env.userAgent_ 的描述。
  
———
2023年3月
### 增强功能  
*   添加了关于[BNPL渠道的最佳实践](https://global.alipay.com/docs/ac/cashierpay/best_practice)的说明，适用于收银台支付。
*   在[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)中，为收银台支付添加了枚举值`KONBINI`、`FPX`和`PAYEASY`；为自动扣款添加了`PAYPAY`和`GrabPay`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，向`paymentMethod.paymentMethodMetaData`参数添加了针对Payeasy和Konbini场景的`payerEmail`参数。
*   在[applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) API中添加了错误代码`AUTH_IN_PROCESS`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API中添加了QRIS的示例代码。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，向`paymentOptions.paymentMethodCategory`字段添加了枚举值`OTC`。
### 文档改进  
*   更新了在《使用银行卡支付方式》中的两种卡片收集模式的描述：[Pay with card payment methods](https://global.alipay.com/docs/ac/cashierpay/card_payment)。
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API请求参数中`order.shipping.shippingPhoneNo`，`order.buyer.buyerPhoneNo`，`order.buyer.buyerName.firstName`和`order.shipping.shippingName.firstName`的描述。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)，[支付（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement)，[支付（用户出示模式支付）](https://global.alipay.com/docs/ac/ams/upm)，[支付（订单码支付）](https://global.alipay.com/docs/ac/ams/oc)和[支付（入口码支付）](https://global.alipay.com/docs/ac/ams/ec)API的请求参数中，将`clientIp`参数的长度从32改为64。
*   更新了[notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) API请求参数中`result.resultStatus`的描述。
*   更新了巴西、秘鲁、墨西哥和智利支持的支付方式中的银行卡品牌：[Payment methods](https://global.alipay.com/docs/ac/ref/payment_method)。
*   删除了《取消》中关于已取消交易不包含在结算文件中的声明：[Cancel](https://global.alipay.com/docs/ac/cashierpay/cancel)。
*   在《使用非银行卡支付方式》的《获取异步通知》部分中，增加了Mercado Pago的默认订单过期时间的说明：[Pay with card-excluded payment methods](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)。
*   在《使用非银行卡支付方式》的《收集或显示额外信息》部分中，添加了Mercado Pago的描述：[Pay with card-excluded payment methods](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)。
*   在《使用非银行卡支付方式》的《启动支付流程》部分中，添加了`codeValue`的描述：[Pay with card-excluded payment methods](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)。
*   更新了《通知》部分中的[notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online)通知描述：[Notifications](https://global.alipay.com/docs/ac/cashierpay/notifications)。
*   将“Payment method-incorporated solution”重命名为“Payment method-preposed solution”。
*   在`paymentMethodType`字段中添加了枚举值`KONBINI`，`FPX`和`PAYEASY`。更多信息请参阅以下文档：  
    *   《收银台支付的交易项目》：[Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   《收银台支付的结算项目》：[Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems)  
*   在`paymentMethodType`字段中添加了枚举值`PAYPAY`和`GrabPay`。更多信息请参阅以下文档：  
    *   《自动扣款的交易项目》：[Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   《自动扣款的结算项目》：[Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
*   更新了《示例5》部分的报告样本。更多信息请参阅以下文档：  
    *   《收银台支付的结算项目》：[Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   《自动扣款的结算项目》：[Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
*   更新了参数`originalTransactionId`的描述。更多信息请参阅以下文档：  
    *   《收银台支付的结算和对账》：[Settle and reconcile](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle)
    *   《自动扣款的结算和对账》：[Settle and reconcile](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle)
    *   《收银台支付的交易项目》：[Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   《自动扣款的交易项目》：[Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   《收银台支付的结算项目》：[Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   《自动扣款的结算项目》：[Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
**2023年2月**
### 增强功能

*   添加了中文版[收银台支付文档](https://global.alipay.com/docs/ac/cashier_payment_cn/introduction)和英文版[收银台支付文档](https://global.alipay.com/docs/ac/cashierpay/overview)。
*   在参数描述中添加了[支付方式](https://global.alipay.com/docs/ac/ref/payment_method)。
*   在[查询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，向字段`paymentOptions.paymentMethodType`添加了枚举值`BILLEASE`, `QRIS`, `MERCADOPAGO_BR`, `MERCADOPAGO_MX`, `MERCADOPAGO_CL`, 和 `MERCADOPAGO_PE`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，向字段`paymentMethod.paymentMethodType`添加了枚举值`BILLEASE`, `QRIS`, `MERCADOPAGO_BR`, `MERCADOPAGO_MX`, `MERCADOPAGO_CL`, 和 `MERCADOPAGO_PE`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，向`paymentMethod.paymentMethodMetaData`参数添加了针对Mercado Pago场景的`cpf`和`payerEmail`参数。
*   向字段`paymentMethodType`添加了枚举值`BILLEASE`, `QRIS`, `MERCADOPAGO_BR`, `MERCADOPAGO_MX`, `MERCADOPAGO_CL`, 和 `MERCADOPAGO_PE`。更多详情，请参阅以下文档：
    *   [收银台支付交易项](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付结算项](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
*   向参数`transactionType`添加了枚举值`REFUND_REVERSAL`。更多详情，请参阅以下文档：
    *   [收银台支付结算项](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款支付结算项](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
*   向参数`summaryType`添加了枚举值`REFUND_REVERSAL`。更多详情，请参阅以下文档：
    *   [收银台支付结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)
### 文档改进  
*   在[概述](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)中更新了请求头的大小写。
*   更新了[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)和[notifyPayment（在线支付通知）](https://global.alipay.com/docs/ac/ams/paymentrn_online)API的代码示例。
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API请求参数中参数`paymentMethod.paymentMethodMetaData`的描述。
  
2023年1月
### 增强功能

*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 的响应参数中，向字段 _paymentOptions.paymentMethodType_ 添加了枚举值 `AKULAKU_PAYLATER_PH` 和 `GRABPAY_MY`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API 的请求参数中，向字段 _paymentMethod.paymentMethodType_ 添加了枚举值 `AKULAKU_PAYLATER_PH` 和 `GRABPAY_MY`。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 的请求参数中，将参数 _allowedPspRegions_ 更改为 _allowedPaymentMethodRegions_。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 的响应参数中，向参数 _PaymentOptions.paymentOptionDetail.supportCardBrands.cardBrand_ 添加了[枚举值列表](https://global.alipay.com/docs/ac/ref/payment_method)。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 的响应参数中，向参数 _PaymentOptions.paymentOptionDetail.supportCardBrands.logo.logoName_ 添加了[枚举值列表](https://global.alipay.com/docs/ac/ref/payment_method)。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 的响应参数中，添加了参数 _PaymentOptions.paymentOptionDetail.funding_。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API 的请求参数中，添加了参数 _paymentMethod.paymentMethodMetaData.dateOfBirth, paymentMethod.paymentMethodMetaData.businessNo, paymentMethod.paymentMethodMetaData.cardPasswordDigest, paymentMethod.paymentMethodMetaData.payerEmail_ 和 _paymentMethod.paymentMethodMetaData.payMentMethodRegion_。
*   在[通知支付](https://global.alipay.com/docs/ac/ams/paymentrn_online) API 的请求参数中，添加了参数 _cardInfo.issuingCountry, cardInfo.funding_ 和 _cardInfo.paymentMethodRegion_。
*   在[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online) API 的响应参数中，添加了参数 _cardInfo.issuingCountry, cardInfo.funding_ 和 _cardInfo.paymentMethodRegion_。
*   向参数 _paymentMethodType_ 添加了枚举值 `AKULAKU_PAYLATER_PH` 和 `GRABPAY_MY`。更多详情，请参阅以下文档：
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
*   添加了参数 _issuingCountry, funding_ 和 _cardBrand_。更多详情，请参阅以下文档：
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
*   添加了参数 _interchangeFeeAmountValue, interchangeFeeCurrency, schemeFeeAmountValue, schemeFeeCurrency, AcquirerMarkupFeeAmountValue_ 和 _AcquirerMarkupFeeCurrency_。更多详情，请参阅以下文档：
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
*   向参数 _summaryType_ 添加了枚举值 `AUTHORIZATION`, `VOID`, `CAPTURE` 和 `DISPUTE`。更多详情，请参阅以下文档：
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
### 文档改进  
*   修改了[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 回复参数中的 _PaymentOptions.installment_ 参数的数据类型，将其改为对象。
*   更新了[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API 回复参数中的 _PaymentOptions.paymentMethodRegion_ 参数的描述。
*   更新了 _feeAmountValue_ 参数的描述。更多详情，请参阅以下文档：  
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)  
    **2022年12月**
### 增强功能  
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，为_field paymentMethodMetaData_的子参数添加了一个下拉过滤框。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中的_paymentAmount.value_字段、[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的请求参数中的_paymentAmount.value_字段、[扣款（收银台支付）](https://global.alipay.com/docs/ac/ams/capture)API的请求参数中的_captureAmount.value_字段、[支付（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement)API的请求参数中的_paymentAmount.value_字段、[退款](https://global.alipay.com/docs/ac/ams/refund_online)API的请求参数中的_refundAmount.value_字段以及[申报](https://global.alipay.com/docs/ac/ams/declare)API的请求参数中的_declarationAmount.value_字段中，添加了关于IDR四舍五入规则的注释。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中的_paymentOptions.paymentMethodType_字段中，添加了枚举值`DOLFIN`, `GRABPAY_SG`, `LINKAJA`, `OVO`, `GOPAY_ID`, `OCTOCLICKS`, `ONLINEBANKING_BNI`, `ONLINEBANKING_MANDIRI`, `ONLINEBANKING_BRI`, `ONLINEBANKING_BCA`, `BANKTRANSFER_MAYBANK`, `BANKTRANSFER_BNI`, `BANKTRANSFER_PERMATA`, `CIMBNIAGA`, `BANKTRANSFER_MANDIRI`, `BANKTRANSFER_BSI`, `ATMTRANSFER_ID`, 和 `PAYNOW`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中的_paymentMethod.paymentMethodType_字段中，添加了枚举值`DOLFIN`, `GRABPAY_SG`, `LINKAJA`, `OVO`, `GOPAY_ID`, `OCTOCLICKS`, `ONLINEBANKING_BNI`, `ONLINEBANKING_MANDIRI`, `ONLINEBANKING_BRI`, `ONLINEBANKING_BCA`, `BANKTRANSFER_MAYBANK`, `BANKTRANSFER_BNI`, `BANKTRANSFER_PERMATA`, `CIMBNIAGA`, `BANKTRANSFER_MANDIRI`, `BANKTRANSFER_BSI`, `ATMTRANSFER_ID`, 和 `PAYNOW`。
*   在[咨询](https://global.alipay.com/docs/ac/ams/authconsult)API的请求参数中的_customerBelongsTo_字段中，添加了枚举值`MAYA`。
*   在[applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp)API的请求参数中的_customerBelongsTo_字段中，添加了枚举值`MAYA`。
*   在[支付（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement)API的请求参数中的_paymentMethod.paymentMethodType_字段中，添加了枚举值`MAYA`。
*   在以下文档中添加了枚举值`DOLFIN`, `GRABPAY_SG`, `LINKAJA`, `OVO`, `GOPAY_ID`, `OCTOCLICKS`, `ONLINEBANKING_BNI`, `ONLINEBANKING_MANDIRI`, `ONLINEBANKING_BRI`, `ONLINEBANKING_BCA`, `BANKTRANSFER_MAYBANK`, `BANKTRANSFER_BNI`, `BANKTRANSFER_PERMATA`, `CIMBNIAGA`, `BANKTRANSFER_MANDIRI`, `BANKTRANSFER_BSI`, `ATMTRANSFER_ID`, 和 `PAYNOW`：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)  
*   在以下文档中添加了枚举值`MAYA`：  
    *   [自动扣款的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
**2022年11月**  
### 增强功能  
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)、[notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online)和[inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online)API中添加了错误代码FRAUD\_REJECT。
*   在[notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online)和[inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online)API中添加了错误代码SUSPECTED\_RISK。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中的_paymentOptions.paymentMethodType_字段中，添加了枚举值`PROMPTPAY`。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中的_paymentMethod.paymentMethodType_字段中，添加了枚举值`PROMPTPAY`。
*   在[咨询](https://global.alipay.com/docs/ac/ams/authconsult)和[applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp)API的请求参数中的_customerBelongsTo_字段中，添加了枚举值`EASYPAISA`。
*   在[支付（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement)API的请求参数中的_paymentMethodType_字段中，添加了枚举值`EASYPAISA`。
*   在[咨询](https://global.alipay.com/docs/ac/ams/authconsult)和[applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp)API中添加了错误代码`NO_PAY_OPTIONS`。
*   在以下文档中添加了枚举值`PROMPTPAY`：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)  
*   在以下文档中添加了枚举值`EASYPAISA`：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
### 已废弃  
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，弃用了字段`cookieId`。
### 文档改进  
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)、[notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online)和[inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API 中的错误代码RISK\_REJECT的描述。
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API响应参数中的字段 _orderCodeForm, orderCodeForm.codeDetails, codeValue_ 的描述。
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API请求参数中的字段 _order.env.deviceTokenId, shipToEmail_ 和 _goodsCategory_ 的描述。
*   2022年10月
### 增强功能

*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，添加了字段`paymentOptions.installments`。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，添加了字段`paymentOptions.paymentOptionDetail.supportBanks`。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，向字段`paymentOptions.paymentMethodType`添加了枚举值`PAYPAY`。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，向字段`paymentOptions.paymentMethodCategory`添加了枚举值`WALLET`。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API中，添加了错误代码`CURRENCY_NOT_SUPPORT`。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，向字段`paymentMethodMetaData`添加了子参数`blikCode`和`payerEmail`。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，添加了字段`paymentMethod.paymentMethodMetaData.bankIdentifierCode`。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，添加了字段`paymentMethod.paymentMethodMetaData.cpf`。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，为字段`order.buyer.buyerPhoneNo`和`order.buyer.buyerEmail`添加了描述。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，为字段`paymentMethod.paymentMethodMetaData.billingAddress`添加了描述。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，为字段`paymentMethod.paymentMethodMetaData.cpf`添加了描述。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，为字段`creditPayPlan.installmentNum`添加了值范围。
*   在[pay（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，向字段`paymentMethod.paymentMethodType`添加了枚举值`PAYPAY`。
*   在[capture（收银台支付）](https://global.alipay.com/docs/ac/ams/capture)和[notifyCapture（收银台支付）](https://global.alipay.com/docs/ac/ams/notify_capture)API中，添加了错误代码`MULTI_CAPTURE_NOT_SUPPORTED`。
*   在[notifyDispute](https://global.alipay.com/docs/ac/ams/notify_dispute)API的请求参数中，添加了字段`disputeJudgedTime`。
*   在[notifyDispute](https://global.alipay.com/docs/ac/ams/notify_dispute)API的请求参数中，为字段`disputeJudgedResult`添加了描述。
*   添加了字段`installmentsNum`。详情请参考以下文档：
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)

*   添加了字段`disputeHandlingFee`、`disputeHandlingFeeCurrency`、`disputeReverseFee`和`disputeReverseFeeCurrency`。详情请参考以下文档：
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)

*   向字段`paymentMethodType`添加了枚举值`PAYPAY`。详情请参考以下文档：
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)

*   更新了字段`settlementAmountValue`、`feeAmountValue`和`taxFeeAmountValue`的描述。详情请参考以下文档：
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)

*   添加了适用于收购方为恒生电子的示例4。详情请参考以下文档：
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)
### 已弃用

*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中，弃用了`paymentOptions.paymentOptionDetail`字段的子字段`card`。
*   在[通知纠纷](https://global.alipay.com/docs/ac/ams/notify_dispute)API的请求参数中，弃用了`disputeJudgedResult`字段的`ACCEPT_BY_ALIPAY`值。
*   [通知纠纷](https://global.alipay.com/docs/ac/ams/notify_dispute)API的错误代码已被弃用。
### 文档改进  
*   将[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API响应参数中的字段 _paymentOptions.paymentMethodType_ 的枚举值`MIXEDCARD`修改为`CARD`。
*   将[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API响应参数中的字段 _paymentOptions.paymentMethodCategory_ 的枚举值改为大写。
*   更新了[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API响应参数中的字段 _paymentOptions.paymentOptionDetail_ 的描述。
*   将[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier) API响应参数中的字段 _paymentOptions.installments.interestRate_ 修改为可选字段。
*   将字段 _paymentMethod.paymentMethodMetaData_ 的数据类型修改为对象，并更新其描述。
*   将[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API请求参数中的字段 _paymentMethod.paymentMethodType_ 的枚举值`MIXEDCARD`修改为`CARD`。
*   将字段 _paymentMethodType_ 的枚举值`MIXEDCARD`修改为`CARD`。更多详情参见以下文档：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款支付的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
**2022年9月**
### 增强功能

*   更新了[请求签名和验证签名](https://global.alipay.com/docs/ac/ams/digital_signature)的文档。
*   更新了[支持](https://global.alipay.com/docs/support)文档。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的请求参数中添加了`merchantRegion`字段。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中向`paymentOptions.paymentMethodType`字段添加了枚举值。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中添加了`paymentOptions.paymentMethodCategory`字段。
*   在[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API的响应参数中添加了`paymentOptions.paymentOptionDetail`字段。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中添加了`paymentFactor`和`paymentMethod.paymentMethodId`字段。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中向`paymentMethod.paymentMethodType`字段添加了枚举值。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，将`card`作为子参数添加到`paymentMethodMetaData`字段中。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中添加了`merchantRegion`字段。
*   添加了[扣款（收银台支付）](https://global.alipay.com/docs/ac/ams/capture)API。
*   在[通知支付](https://global.alipay.com/docs/ac/ams/paymentrn_online)API的请求参数中添加了`cardInfo`和`acquirerReferenceNo`字段。
*   添加了[通知扣款（收银台支付）](https://global.alipay.com/docs/ac/ams/notify_capture)API。
*   在[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online)API的响应参数中添加了`cardInfo`和`acquirerReferenceNo`字段。
*   在[退款](https://global.alipay.com/docs/ac/ams/refund_online)API的响应参数中添加了`acquirerReferenceNo`字段。
*   在[取消](https://global.alipay.com/docs/ac/ams/paymentc_online)API中添加了错误代码ORDER\_STATUS\_INVALID。
### 已废弃  
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的请求参数中，已废弃字段`paymentMethod.card`。
### 文档改进  
*   修改了[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API响应参数中的_paymentOptions.paymentMethodRegion_字段描述。
*   修改了[咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)API响应参数中的_paymentOptions.logo.logoName_字段的最小长度。
*   修改了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API响应参数中的_result.resultStatus_字段描述。
*   修改了[退款](https://global.alipay.com/docs/ac/ams/refund_online)API中的错误代码`PAYMENT_METHOD_NOT_SUPPORTED`名称。
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)API的结果处理逻辑。
*   修改了[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online)API响应参数中的_transactions_字段描述。
*   更新了[查询支付](https://global.alipay.com/docs/ac/ams/paymentri_online)API的支付结果代码。
*   修改了文件路径命名规则和_field seq_的描述。更多详情，请参阅以下文档：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款支付的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)  
*   修改了_field customerId_的描述。更多详情，请参阅以下文档：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款支付的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)  
*   添加了_field acquirer_。更多详情，请参阅以下文档：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款支付的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)  
*   添加了_field acquirerReferenceNo_。更多详情，请参阅以下文档：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款支付的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
*   修改了_fields transactionId, originalTransactionId, transactionRequestId, referenceTransactionId, paymentMethodType, transactionType_的描述。更多详情，请参阅以下文档：  
    *   [收银台支付的交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款支付的交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)  
*   修改了_field settlementBatchId_的描述。更多详情，请参阅以下文档：  
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款支付的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)  
*   添加了_fields taxFeeAmountValue 和 taxFeeCurrency_。更多详情，请参阅以下文档：  
    *   [收银台支付的结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银台支付的结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付的结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款支付的结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)  
2022年8月
### 增强功能
*   废弃了API的数据字典。
*   废弃了在线支付注册相关的API：**registration**、**notifyRegistrationStatus**、**inquiryRegistrationStatus**和**inquiryRegistrationInfo**。
### 文档改进  
*   更新了 _referenceTransactionId_ 字段的描述。详情请参阅以下文档：  
    *   [收银支付 - 交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银支付 - 结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [自动扣款支付 - 交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款支付 - 结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
*   在 **结算与对账** 文档中添加了 _processingFeeAmountValue_ 和 _processingFeeCurrency_ 字段。详情请参阅以下文档：  
    *   [收银支付 - 结算与对账](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle)
    *   [自动扣款支付 - 结算与对账](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle)
*   更新了 _feeAmountValue_ 字段的描述。详情请参阅以下文档：  
    *   [收银支付 - 结算与对账](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle)
    *   [收银支付 - 结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [收银支付 - 结算汇总](https://global.alipay.com/docs/ac/cashierpay/settlementsummary)
    *   [自动扣款支付 - 结算与对账](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle)
    *   [自动扣款支付 - 结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
    *   [自动扣款支付 - 结算汇总](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary)
*   修改了 [支付（收银支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API 中的 _paymentMethodMetaData_ 字段的描述。  
**2022年7月**
### 增强功能

*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API 的请求参数中添加了 `_userRegion` 字段，响应参数中添加了 `_paymentData` 字段。
*   在[退款](https://global.alipay.com/docs/ac/ams/refund_online) API 中添加了两个错误代码 `REFUND_NOT_SUPPORTED` 和 `PARTIAL_REFUND_NOT_SUPPORTED`。
*   为收银台支付添加了[BNPL渠道的最佳实践](https://global.alipay.com/docs/ac/cashierpay/best_practice#QSnOx)。
*   在[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)和[支付（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement) API 中添加了 `_goodsCategory` 字段。
*   向收银台支付添加了 Akulaku PayLater 支付方式，向收银台支付和自动扣款添加了 Boost eWallet。更多信息，请参阅以下文档：
    *   [咨询（收银台支付）](https://global.alipay.com/docs/ac/ams/consult_cashier)
    *   [支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier)
    *   [收银台支付交易项目](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
    *   [收银台支付结算项目](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
    *   [咨询](https://global.alipay.com/docs/ac/ams/authconsult)
    *   [申请Token](https://global.alipay.com/docs/ac/ams/accesstokenapp)
    *   [支付（自动扣款）](https://global.alipay.com/docs/ac/ams/payment_agreement)
    *   [自动扣款交易项目](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
    *   [自动扣款结算项目](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)
### 文档改进  
*   更新了[支付（收银台支付）](https://global.alipay.com/docs/ac/ams/payment_cashier) API 中的结果处理逻辑。
*   更新了以下接口的错误代码：**咨询**、**申请令牌**、**撤销**、**支付（收银台支付）**、**支付（自动扣款）**、**通知支付**、**查询支付**、**取消**、**退款**、**查询退款**、**通知退款**、**申报**、**查询申报请求**、**支付（用户出示模式支付）**、**支付（订单码支付）**、**支付（入口码支付）**。
  
  2022年5月  
  --------  
  添加了**咨询（收银台支付）**和**通知退款**接口。  
  更新了支付（收银台支付）文档：  
  *   在请求参数中添加了 paymentMethod.paymentMethodMetaData 字段。
  *   在 paymentMethod.paymentMethodType 字段中添加了一些新的枚举值。
  *   修改了 settlementStrategy.settlementCurrency 字段的描述。
  *   添加了以下错误代码：  
  *   INVALID\_PAYMENT\_METHOD\_META\_DATA
  *   INCORRECT\_BLIKCODE
  *   SETTLE\_CONTRACT\_NOT\_MATCH  
  更新了通知支付文档：  
  *   在 notifyType 字段中添加了新的枚举值 `PAYMENT_PENDING`。  
  更新了查询支付文档：  
  *   在 paymentStatus 字段中添加了新的枚举值 `PENDING`。  
  更新了退款文档：  
  *   在请求参数中添加了 refundNotifyUrl 字段。
  *   添加了错误代码：REFUND\_IN\_PROCESS  
  更新了收银台支付下的交易项目、结算项目和结算汇总文档：  
  *   在交易项目和结算项目中的 paymentMethodType 字段中添加了以下新的枚举值：  
  *   IDEAL
  *   GIROPAY
  *   SOFORT
  *   PAYU
  *   P24
  *   BLIK
  *   EPS
  *   BANCONTACT
  *   PIX  
  *   在结算项目和结算汇总中添加了以下字段：  
  *   processingFeeAmountValue
  *   processingFeeCurrency  
  *   修改了结算项目和结算汇总中的报告路径和名称部分。  
  2022年4月  
  ----------  
  *   在以下接口的请求参数中添加了 merchantRegion 字段：  
  *   支付（收银台支付）
  *   咨询
  *   申请令牌
  *   支付（用户出示模式支付）
  *   支付（订单码支付）
  *   支付（入口码支付）  
  *   修改了以下接口示例代码中的海关代码：  
  *   申报：将 ZHENGZHOU 修改为 ZONGSHU
  *   查询申报请求：将 shenzhen 修改为 ZONGSHU  
  *   “业务注册国家/地区”字段从“欢迎”页面移到了“创建新应用”页面。  
  2022年3月  
  ----------  
  *   添加了[沙箱](https://global.alipay.com/docs/ac/ref/sandbox)文档。
  *   添加了[收银台支付](https://global.alipay.com/docs/ac/cashierpay/overview)文档的新版本。
  *   添加了[自动扣款](https://global.alipay.com/docs/ac/autodebitpay/overview)文档的新版本。
  *   在查询支付接口的响应参数中添加了 redirectActionForm 字段。  
  2022年2月  
  -------------  
  *   删除了 initAuthentication 和 verifyAuthentication 接口。
  *   在支付（自动扣款）中添加了 USER\_NOT\_EXIST 错误代码。  
  2022年1月  
  --------------  
  在以下接口中添加了 grossSettlementAmount 和 settlementQuote 字段：  
  *   通知支付
  *   查询支付
  *   退款
  *   查询退款  
  更新了支付（收银台支付）文档：  
  *   添加了以下错误代码：  
  *   INVALID\_MERCHANT\_STATUS
  *   MERCHANT\_KYB\_NOT\_QUALIFIED
  *   NO\_PAY\_OPTIONS  
  *   删除了以下错误代码：  
  *   SUCCESS
  *   ORDER\_NOT\_EXIST  
  更新了支付（自动扣款）文档：  
  *   删除了以下字段：  
  *   请求参数：  
  *   merchant.store
  *   order.env.storeTerminalId
  *   order.env.storeTerminalRequestTime
  *   payToMethod
  *   paymentMethod.paymentMethodMetaData
  *   isAuthorization
  *   paymentVerificationData
  *   paymentFactor  
  *   响应参数：  
  *   authExpiryTime
  *   challengeActionForm
  *   redirectActionForm
  *   orderCodeForm  
  *   将以下字段从可选修改为必需：  
  *   请求参数：  
  *   paymentMethod.paymentMethodId
  *   env
  *   env.terminalType
  *   settlementStrategy.settlementCurrency  
  *   响应参数：  
  *   result.resultMessage  
  *   添加了以下错误代码：  
  *   INVALID\_MERCHANT\_STATUS
  *   MERCHANT\_KYB\_NOT\_QUALIFIED
  *   USER\_PAYMENT\_VERIFICATION\_FAILED  
  *   删除了以下错误代码：  
  *   USER\_NOT\_EXIST
  *   ORDER\_NOT\_EXIST  
  更新了通知支付文档：  
  *   删除了以下字段：  
  *   请求参数：  
  *   notifyType: OFFLINE\_PAYMENT\_CODE
  *   result.resultStatus: U  
  *   将以下字段从可选修改为必需：  
  *   请求参数：  
  *   paymentCreateTime
  *   paymentId
  *   result.resultMessage  
  *   添加了支付（收银台支付）和支付（自动扣款）的错误代码。  
  更新了查询支付文档：  
  *   删除了以下字段：  
  *   响应参数：  
  *   authExpiryTime
  *   redirectActionForm
  *   transaction.transactionType: PAYMENT, CANCEL, AUTHORIZATION, CAPTURE, VOID
  *   transactionTime  
  *   将以下字段从可选修改为必需：  
  *   响应参数：  
  *   result
  *   result.resultMessage
  *   transactions.transactionId  
  *   添加了以下两个结果代码表：  
  *   支付结果代码
  *   交易结果代码  
  *   删除了以下错误代码：  
  *   RISK\_REJECT
  *   USER\_KYC\_NOT\_QUALIFIED  
  更新了取消文档：  
  *   将以下字段从可选修改为必需：  
  *   响应参数：  
  *   result.resultMessage  
  更新了退款文档：  
  *   将以下字段从可选修改为必需：  
  *   响应参数：  
  *   result.resultMessage  
  *   添加了以下错误代码：  
  *   INVALID\_MERCHANT\_STATUS
  *   ORDER\_IS\_CLOSED  
  更新了查询退款文档：  
  *   添加了以下字段：  
  *   响应参数：  
  *   refundStatus: FAIL  
  *   删除了以下错误代码：  
  *   RISK\_REJECT
  *   MERCHANT\_NOT\_REGISTERED
  *   INVALID\_CONTRACT  
  *   添加了退款结果代码表。  
  更新了咨询文档：  
  *   将以下字段从可选修改为必需：  
  *   响应参数：  
  *   result.resultMessage  
  *   添加了以下错误代码：  
  *   INVALID\_CLIENT\_STATUS
  *   OAUTH\_FAILED
  *   UNKNOWN\_CLIENT  
  更新了申请令牌文档：  
  *   将以下字段从可选修改为必需：  
  *   响应参数：  
  *   result.resultMessage  
  *   添加了以下错误代码：  
  *   INVALID\_CLIENT\_STATUS
  *   OAUTH\_FAILED
  *   UNKNOWN\_CLIENT
  *   USER\_NOT\_EXIST
  *   USER\_STATUS\_ABNORMAL  
  更新了撤销文档：  
  *   将以下字段从可选修改为必需：  
  *   响应参数：  
  *   result.resultMessage  
  *   添加了以下错误代码：  
  *   CLIENT\_FORBIDDEN\_ACCESS\_API
  *   INVALID\_CLIENT\_STATUS
  *   OAUTH\_FAILED
  *   UNKNOWN\_CLIENT  
  在查询退款接口中添加了 grossSettlementAmount 和 settlementQuote 字段。  
  更新了支付（用户出示模式支付）文档：  
  *   删除了以下字段：  
  *   请求参数：  
  *   isAuthorization
  *   paymentFactor.isPaymentEvaluation
  *   paymentMethod.paymentMethodMetaData
  *   paymentVerificationData
  *   payToMethod  
  *   响应参数：  
  *   authExpiryTime
  *   challengeActionForm.challengeRenderValue
  *   orderCodeForm  
  *   添加了 settlementStrategy 字段。
  *   将 paymentMethod.paymentMethodId 字段从可选修改为必需。  
  更新了支付（订单码支付）文档：  
  *   删除了以下字段：  
  *   请求参数：  
  *   isAuthorization
  *   paymentFactor.isPaymentEvaluation
  *   paymentMethod.paymentMethodMetaData
  *   paymentVerificationData
  *   payToMethod  
  *   响应参数：  
  *   authExpiryTime
  *   challengeActionForm.challengeRenderValue  
  *   添加了 settlementStrategy 字段。
  *   将 orderCodeForm 字段从可选修改为必需。  
  更新了支付（入口码支付）文档：  
  *   删除了以下字段：  
  *   请求参数：  
  *   isAuthorization
  *   paymentFactor.isPaymentEvaluation
  *   paymentMethod.paymentMethodMetaData
  *   paymentVerificationData
  *   payToMethod  
  *   响应参数：  
  *   authExpiryTime
  *   challengeActionForm.challengeRenderValue
  *   orderCodeForm  
  *   添加了 settlementStrategy 字段。
  *   将 order.env 和 order.env.userAgent 字段从可选修改为必需。  
  2021年12月  
  -------------  
  *   自动扣款添加了授权结果通知功能。因此，以下文档进行了重组：  
  *   [概述](https://global.alipay.com/docs/ac/agreementpayment/intro)
  *   [授权和支付](https://global.alipay.com/docs/ac/agreementpayment/payment)
  *   [最佳实践](https://global.alipay.com/docs/ac/agreementpayment/autodebit_bp)
  *   [API 列表](https://global.alipay.com/docs/ac/agreementpayment/apis)  
  对于在线支付和店内支付：  
  *   在以下产品中添加了退款查询功能：  
  *   收银台支付
  *   自动扣款
  *   用户出示模式支付
  *   订单码支付
  *   入口码支付  
  *   因此，以下文档进行了重组：  
  *   后支付服务
  *   最佳实践
  *   API 列表  
  更新了支付（收银台支付）文档：  
  **请求参数**  
  *   删除了以下字段：  
  *   merchant.store
  *   order.env.storeTerminalId
  *   order.env.storeTerminalRequestTime
  *   payToMethod
  *   paymentMethod.paymentMethodId
  *   paymentMethod.paymentMethodMetaData
  *   isAuthorization
  *   paymentVerificationData
  *   paymentFactor  
  *   将以下字段从可选修改为必需：  
  *   order.env
  *   settlementStrategy.settlementCurrency  
  **响应参数**  
  *   删除了以下字段：  
  *   result.resultStatus: S
  *   paymentTime
  *   authExpiryTime
  *   challegeActionForm
  *   redirectActionForm.method: SCAN
  *   orderCodeForm.paymentMethodType
  *   settlementQuote
  *   grossSettlementAmount  
  *   将以下字段从可选修改为必需：  
  *   orderCodeForm.expireTime
  *   orderCodeForm.codeDetails
  *   result.resultMessage  
  在 applyToken 接口中添加了 userLoginId 字段。  
  在支付（收银台支付）和支付（自动扣款）接口中添加了以下字段：  
  *   schemeUrl
  *   applinkUrl
  *   normalUrl
  *   appIdentifier  
  在以下 API 中添加了新的枚举值 `BPI` 和 `RABBIT_LINE_PAY`：  
  *   支付（收银台支付）：paymentMethod.paymentMethodType  
  在以下 API 中添加了新的枚举值 `RABBIT_LINE_PAY`：  
  *   支付（自动扣款）：paymentMethod.paymentMethodType
  *   咨询：customerBelongsTo
  *   申请令牌：customerBelongsTo  
  2021年11月  
  --------------  
  *   自动扣款：更新了[客户端与钱包集成](https://global.alipay.com/docs/ac/agreementpayment/clientsideint)文档。  
  2021年10月  
  ------------  
  *   收银台支付：更新了[客户端与钱包集成](https://global.alipay.com/docs/ac/cashierpayment/clientsideint)文档。  
  *   自动扣款添加了支付结果通知功能。因此，以下文档进行了重组：  
  *   [概述](https://global.alipay.com/docs/ac/agreementpayment/intro)
  *   [授权和支付](https://global.alipay.com/docs/ac/agreementpayment/payment)
  *   [最佳实践](https://global.alipay.com/docs/ac/agreementpayment/autodebit_bp)
  *   [API 列表](https://global.alipay.com/docs/ac/agreementpayment/apis)  
  *   在线支付和店内支付场景的新介绍视频已添加。您可以前往[在线支付](https://global.alipay.com/docs/onlinepayment)和[店内支付](https://global.alipay.com/docs/instorepayment)查看详细信息。  
  2021年9月  
  ------------  
  *   以下术语更名：  
  | 废弃术语 | 当前术语 | 备注 |
  | --- | --- | --- |
  | PMP | Alipay+ MPP | 当前术语的含义与废弃术语相同。 |
  *   在线支付和店内支付的报告和对账场景中添加了新的结算方式。  
  *   从每个产品的结算汇总文件中删除了以下字段：  
  *   transactionAmountValue
  *   transactionCurrency  
  *   删除了以下 API 中的 INVALID\_CODE 错误代码：  
  *   [用户出示模式支付](https://global.alipay.com/docs/ac/ams/upm)
  *   [订单码支付](https://global.alipay.com/docs/ac/ams/oc)
  *   [入口码支付](https://global.alipay.com/docs/ac/ams/oc)  
  *   在以下 API 中添加了 INVALID\_PAYMENT\_CODE 错误代码：  
  *   [用户出示模式支付](https://global.alipay.com/docs/ac/ams/upm)  
  2021年12月  
  --------------  
  *   更名了以下术语：  
  | 废弃术语 | 当前术语 | 备注 |
  | --- | --- | --- |
  | Consumer-presented Mode Payment | 用户出示模式支付 | 废弃术语可能仍会在代码中显示，例如 API 规范、Java 代码规范或其他存在技术元素的地方。废弃术语的含义没有改变。 |
  *   在12月发布了在线支付和店内支付产品的 API 新版本。API 文档格式更新为新版本，以提供更好的用户体验。现在，您可以在同一个文档中访问子字段。以前，子字段仅在数据字典中可用。您可以转到“API 参考”>“产品 API”>“在线支付”（[https://global.alipay.com/docs/ac/ams/payment\_cashier](https://global.alipay.com/docs/ac/ams/payment_cashier)）来查看新版本。  
  2020年5月  
  --------  
  发布了新版 Alipay Docs，将原门户（[https://global.alipay.com/open/doc.htm](https://global.alipay.com/open/doc.htm)）上的技术文档合并到新站点，以提供更好的用户体验。您可以转到“文档”>“遗留文档”（[https://global.alipay.com/docs/ac/legacy/legacydoc](https://global.alipay.com/docs/ac/legacy/legacydoc)）查看详细信息。