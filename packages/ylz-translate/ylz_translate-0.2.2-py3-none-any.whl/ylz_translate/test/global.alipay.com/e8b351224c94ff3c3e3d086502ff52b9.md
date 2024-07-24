Release notes | Alipay, China's leading third-party online payment solution
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Freleasenotes)

[Home](/docs/)

[Online payment](/docs/onlinepayment)

[In-store payment](/docs/instorepayment)

[Solutions](/docs/solutions)

[Revenue Booster](/docs/ac/revenuebooster_en/overview)

[Combined Payment](/docs/ac/combinedpay_en/overview)

[Flexible Settlement](/docs/ac/flexiblesettlement_en/overview)

[Integration guide](/docs/integration_guide_en)

[Antom Dashboard](/docs/dashboard_en)

[SDKs](/docs/sdks)

[APIs](https://global.alipay.com/docs/ac/ams/api)

[Reconciliation](https://global.alipay.com/docs/ac/reconcile)

[Digital signature](https://global.alipay.com/docs/ac/ams/digital_signature)

[Sandbox](https://global.alipay.com/docs/ac/ref/sandbox)

[Tools](https://global.alipay.com/docs/ac/ref/key_config_en)

[Test wallet](https://global.alipay.com/docs/ac/ref/testwallet)

[Dispute](https://global.alipay.com/docs/ac/dispute)

[Merchant service](https://global.alipay.com/docs/ac/merchant_service)

[Release notes](/docs/releasenotes)

[Support](/docs/support)

[Glossary](/docs/glossary)

[Help center](https://cshall.alipay.com/enterprise/global/klgList?sceneCode=un_login&routerId=d9aa1f608c4145d6b3c8030c17cf6f9a000&categoryId=50479)

[Legacy documentation](https://global.alipay.com/docs/ac/legacy/legacydoc)

Subscribe to updates

Subscribe to product updates and receive email notifications about updates to the documentation. You can unsubscribe via the **Unsubscribe** button on the right or the link provided in every email notification.

Subscribe

Release notes
=============

2024-04-03 03:29

March 2024
----------

### Enhanced

*   Added the _funding_ and _cardCategory_ fields in the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier), [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online), and [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) APIs.
*   Added the _funding_ field in the [**consult (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/consult) API.
*   Added the _requireIssuerAuthentication_ field in the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Updated the description of the _selectedCardBrand_ field in the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the _transit_, _lodging_, and _gaming_ fields in the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier), [**createPaymentSession (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/session_cashier), and [**decide**](https://global.alipay.com/docs/ac/risk_control/decide) APIs.
*   Added the embeded [Web/WEP](https://global.alipay.com/docs/ac/cashierpay/embeded_webwap_en) integration guide for Card payments.

February 2024
-------------

### Enhanced

*   Added the [**acceptDispute**](https://global.alipay.com/docs/ac/ams/accept), [**supplyDefenseDocument**](https://global.alipay.com/docs/ac/ams/supply_evidence), [**downloadDisputeEvidence**](https://global.alipay.com/docs/ac/ams/download), and [**notfiyDispute**](https://global.alipay.com/docs/ac/ams/notify_dispute) APIs for Dispute.
*   Added the enumeration value `DEFENSE_DUE_ALERT` for the _disputeNotificationType_ field in the [**notifyDispute**](https://global.alipay.com/docs/ac/ams/notify_dispute) API.
*   Updated the description of the _defenseDueTime_ field in the [**notifyDispute**](https://global.alipay.com/docs/ac/ams/notify_dispute) API.

January 2024
------------

### Enhanced

*   Added the payment method Yapily to the [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method) document.
*   Added the _paymentMethodId_ field in the [**create**](https://global.alipay.com/docs/ac/ams/create_sub) API.
*   Added the enumeration value `CARD` for the _paymentMethodType_ field in the [**create**](https://global.alipay.com/docs/ac/ams/create_sub) API.
*   Updated the description of the _subscriptionEndTime_ field in the [**create**](https://global.alipay.com/docs/ac/ams/create_sub) API.
*   Added the _phaseNo_ field in the [**notifyPayment**](https://global.alipay.com/docs/ac/ams/notify_subpayment) API.

December 2023
-------------

### Enhanced

*   Added the sample codes for K PLUS in the [**consult**](https://global.alipay.com/docs/ac/ams/authconsult) API.
*   Added the _authExpiryTime_ field in the response of [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Updated the download link of test wallet for the Android version in the [Test wallet](https://global.alipay.com/docs/ac/ref/testwallet) document.
*   Added the error code `INVALID_AMOUNT` to the following APIs: [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier), [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online), [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) .
*   Updated the description of enumeration value `TOKEN_CREATED` for the _authorizationNotifyType_ field in the [**notifyAuthorization**](https://global.alipay.com/docs/ac/ams/notifyauth) API.
*   Updated the component name `AMSEasyPay` in the [Web/WEP](https://global.alipay.com/docs/ac/easypay_en/webwap_en), [Android](https://global.alipay.com/docs/ac/easypay_en/android_en), and [iOS](https://global.alipay.com/docs/ac/easypay_en/ios_en) Integration guide of Easy Pay.
*   Updated the component name `AMSCashierPayment` in the Card payments Web/WEP, [Android](https://global.alipay.com/docs/ac/cashierpay/android), and [iOS](https://global.alipay.com/docs/ac/cashierpay/ios) Integration guide of Checkout Payment.
*   Updated the component name `AMSCashierPayment` in the Bank related payments [Web/WEP](https://global.alipay.com/docs/ac/cashierpay/bank_webwap), [Android](https://global.alipay.com/docs/ac/cashierpay/bank_android), and [iOS](https://global.alipay.com/docs/ac/cashierpay/bank_ios) Integration guide of Checkout Payment.

November 2023
-------------

### Enhanced

*   Added the error code `ORDER_IS_CANCELED` to the [**refund**](https://global.alipay.com/docs/ac/ams/refund_online) API.
*   Added the event code `SDK_PAYMENT_CANCEL` to the [Android](https://global.alipay.com/docs/ac/easypay_en/android_en) Integration guide of [Easy Pay](https://global.alipay.com/docs/ac/easypay_en/sdk).
*   Added the payment methods Pagaleve and Bancomat Pay to the [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method) document.
*   Added the scenario of Pagaleve to the field _paymentMethod.paymentMethodMetaData_ of the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Updated the description of the fields _order.buyer_ and _order.buyer.buyerPhoneNo_ of the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the [**createVaultingSession**](https://global.alipay.com/docs/ac/ams/vaulting_session)**,** [**vaultPaymentMethod**](https://global.alipay.com/docs/ac/ams/vault_method)**,** [**notifyVaulting**](https://global.alipay.com/docs/ac/ams/notify_vaulting)**,** and [**inquireVaulting**](https://global.alipay.com/docs/ac/ams/inquire_vaulting) APIs for [Vault](https://global.alipay.com/docs/ac/ams/inquire_vaulting).
*   Added the [Web/WEP](https://global.alipay.com/docs/ac/cashierpay/bank_webwap), [Android](https://global.alipay.com/docs/ac/cashierpay/bank_android), and [iOS](https://global.alipay.com/docs/ac/cashierpay/bank_ios) Integration guides for [Bank related payments](https://global.alipay.com/docs/ac/cashierpay/bank_sdk).
*   Updated the code sample in the [Web/WEP](https://global.alipay.com/docs/ac/easypay_en/webwap_en), [Android](https://global.alipay.com/docs/ac/easypay_en/android_en), and [iOS](https://global.alipay.com/docs/ac/easypay_en/ios_en) Integration guide of [Easy Pay](https://global.alipay.com/docs/ac/easypay_en/sdk).

In-store payments

*   Added the error code `ORDER_STATUS_INVALID` to the [**cancel**](https://global.alipay.com/docs/ac/ams/paymentc) API.
*   Added the error codes `ACCESS_DENIED` and `ORDER_IS_CANCELED` to the [**refund**](https://global.alipay.com/docs/ac/ams/refund) API.

### Deprecated

Removed the domain used by GAGW: [https://open-global.alipay.com](https://open-global.alipay.com).

October 2023
------------

### Enhanced

*   Added the scenarios of KONBINI, BANKTRANSFER\_PAYEASY, and ONLINEBANKING\_PAYEASY to the fields _order.buyer.buyerEmail_, _order.buyer.buyerEmail.buyerPhoneNo_, _order.buyer.buyerEmail.buyerName.firstName_, and _order.buyer.buyerEmail.buyerName.lastName_ of the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the error code `DO_NOT_HONOR` to the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online), [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online), and [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) APIs.
*   Added the auto-capture ability to card payment in the _paymentFactor.captureMode_ field in the [createPaymentSession (Checkout Payment)](https://global.alipay.com/docs/ac/ams/session_cashier) document.
*   Updated the integration solution of LINE Pay, Pay-easy, and Konbini in the [Non-card payment](https://global.alipay.com/docs/ac/cashierpay/noncard_payment) document.
*   Added the [Quickstart](https://global.alipay.com/docs/ac/cashierpay/quickstart) and [Test resources](https://global.alipay.com/docs/ac/cashierpay/test) documents to the Checkout Payment documentation.
*   Added the payment methods `DIRECT_DEBIT_SIAMCOMMERCIALBANK` and `DIRECT_DEBIT_KRUNGTHAIBANK` to the [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method#vgXw6) document.
*   Added the payment methods DOKU, KPLUS, Pay-easy online banking, and Pay-easy bank transfer for Checkout Payment to the [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method) document.
*   Added the payment methods KPLUS for Auto Debit and Subscription Payment to the [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method) document.
*   Added the optional field [_agent-token_](https://global.alipay.com/docs/ac/ams/api_fund#sjPLz) to the request header to authorize ISVs for API calls.

### Deprecated

*   Deleted the scenarios of Pay-easy and Konbini from the field _paymentMethod.paymentMethodMetaData_ of the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Deleted the error code INVALID\_API from the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) and [**pay (Auto Debit)**](https://global.alipay.com/docs/ac/ams/payment_agreement) APIs.
*   Deprecated the payment method of Pay-easy (with enumeration value `PAYEASY`).

September 2023
--------------

### Enhanced

*   Added the field _paymentFactor.captureMode_ to the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Modified the description of the field _paymentResultInfo_ in the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) and [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) APIs.
*   Added the fields _WalletPaymentResultInfo.creditPayPlan_, _paymentResultInfo.funding_, and _WalletPaymentResultInfo.creditPayPlan.installmentNu_ to the [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) and [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online) APIs.
*   Modified the description of the fields _order.shipping.shippingAddress.state_, _order.shipping.shippingAddress.zipCode_, _paymentMethod.paymentMethodMetaData.billingAddress.state_, _and paymentMethod.paymentMethodMetaData.billingAddress.zipCode_ in the [**pay (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier) and [**createPaymentSession (Checkout Payment)**](https://global.alipay.com/docs/ac/ams/session_cashier) APIs.
*   Added the field _authCodeForm_ to the [**consult**](https://global.alipay.com/docs/ac/ams/authconsult) API.
*   Added the auto-capture ability to card payment in the [Card payment](https://global.alipay.com/docs/ac/cashierpay/card_payment), [API integration](https://global.alipay.com/docs/ac/cashierpay/api), and [Capture](https://global.alipay.com/docs/ac/cashierpay/capture) documents of the Checkout Payment documentation.
*   Added new payment methods JKOPay and LINE Pay for Checkout Payment to the [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method) document.
*   Modified the maximum length of the field _funding_ from 6 to 20 to the [Transaction details report](https://global.alipay.com/docs/ac/reconcile/transaction_details) and [Settlement details report](https://global.alipay.com/docs/ac/reconcile/settlement_details) documents in the Reconciliation documentation.
*   Added the enumeration values `COLLATERAL_WITHHOLDING`, `RESERVE_WITHHOLDING`, `RESERVE_RELEASE` to the field _summaryType_ in the [Settlement summary report](https://global.alipay.com/docs/ac/reconcile/settlement_details) document of the Reconciliation documentation.
*   Added the enumeration values `COLLATERAL_WITHHOLDING`, `RESERVE_WITHHOLDING`, `RESERVE_RELEASE` to the field _transactionType_ in the [Settlement details report](https://global.alipay.com/docs/ac/reconcile/settlement_details) document of the Reconciliation documentation.
*   Added the [Best practices for configuring the payment continuation URL](https://global.alipay.com/docs/ac/cashierpay/redirection) document to the Checkout Payment documentation.
*   Update the Settlement & Transactions documentation.

### Deprecated

*   Deprecated the payment methods of Dolfin, BPI, bKash for Direct Debit and Periodic Subscriptions, and Easypaisa for Direct Debit and Periodic Subscriptions.

August 2023
-----------

### Enhanced

*   Added the three video tutorials about merchant service operations: [How to issue a refund](https://global.alipay.com/docs/ac/merchant_service/videos#How-to-issue-a-refund), [How to view transaction details](https://global.alipay.com/docs/ac/merchant_service/videos#How-to-view-transaction-details), and [How to manage invoices](https://global.alipay.com/docs/ac/merchant_service/videos#How-to-manage-invoices).
*   Added the documentation of the value-added services: [Revenue Booster](https://global.alipay.com/docs/ac/revenuebooster_en/overview), [Combined Payment](https://global.alipay.com/docs/ac/combinedpay_en/overview), and [Flexible Settlement](https://global.alipay.com/docs/ac/flexiblesettlement_en).
*   Added the documentation of the payment products: [Scan to Bind](https://global.alipay.com/docs/ac/scantopay_en/overview) and [Subscription Payment](https://global.alipay.com/docs/ac/subscriptionpay_en/overview).
*   Added the [Card payment documents](https://global.alipay.com/docs/ac/cashierpay/card_payment) in Checkout Payment documentation.
*   Added the enumeration values `AMEX`, `DISCOVER`, `DINERS`, `CUP`, `JCB`, `MAESTRO`, and`CARTES_BANCAIRES` for Card brands in [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method).
*   Added payment methods supported by Subscription Payment in [_Payment methods_](https://global.alipay.com/docs/ac/ref/payment_method).
*   Added the document [Risk management methods](https://global.alipay.com/docs/ac/ref/risk_methods).
*   Added the accelerated domain name [https://open-de-global.alipay.com](https://open-de-global.alipay.com) for merchant servers based in Europe.
*   Added the [**create**](https://global.alipay.com/docs/ac/ams/create_sub), [**notifySubscription**](https://global.alipay.com/docs/ac/ams/notify_sub), [**notifyPayment**](https://global.alipay.com/docs/ac/ams/notify_subpayment), [**change**](https://global.alipay.com/docs/ac/ams/change_sub), and [**cancel**](https://global.alipay.com/docs/ac/ams/cancel_sub) APIs for Subscription Payment.
*   Added the error codes `CARD_NOT_SUPPORTED`, `USER_BALANCE_NOT_ENOUGH`, `INVALID_EXPIRATION_DATE`, and `INVALID_CARD_NUMBER`in the [**pay (Cashier Payment)**](https://global.alipay.com/docs/ac/ams/payment_cashier), [**notifyPayment**](https://global.alipay.com/docs/ac/ams/paymentrn_online), and [**inquiryPayment**](https://global.alipay.com/docs/ac/ams/paymentri_online) APIs.
*   Added the [**createPaymentSession (Cashier Payment)**](https://global.alipay.com/docs/ac/ams/session_cashier) API for card payment.
*   Updated the [Auto Debit](https://global.alipay.com/docs/ac/autodebit_en/overview) documentation. The new version offers a restructured guide on integration and operations following the payment.
*   Updated the product name from Cashier Payment to Checkout Payment.
*   Updated the [Reconciliation](https://global.alipay.com/docs/ac/reconcile) documentation. The new version provides comprehensive information on reconciliation, covering settlement rules and lifecycle.

July 2023
---------

### Enhanced

*   Added the [createPaymentSession (Easy Pay)](https://global.alipay.com/docs/ac/ams/createpaymentsession_easypay) API for Easy Pay product.
*   Added both the [English](https://global.alipay.com/docs/ac/easypay_en/overview_en) and [Chinese](https://global.alipay.com/docs/ac/easypay/overview) version of the integration guide for Easy Pay product.
*   Added the enumeration value `TOKEN_CREATED` to the field _authorizationNotifyType_ in the request parameters of the [notifyAuthorization](https://global.alipay.com/docs/ac/ams/notifyauth) API.
*   Supported the acquirer AlipayBR for the Brazilian cards and PIX.

### Deprecated

*   Deprecated the field _customerId_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier), [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement), [pay (User-presented Mode Payment)](https://global.alipay.com/docs/ac/ams/upm), [pay (Order Code Payment)](https://global.alipay.com/docs/ac/ams/oc), and [pay (Entry Code Payment)](https://global.alipay.com/docs/ac/ams/ec).

June 2023
---------

### Enhanced

*   Added the enumeration value `NAVERPAY` for Cashier Payment and Auto Debit, and `TOSS` for Cashier Payment in [_Payment methods_](https://global.alipay.com/docs/ac/ref/payment_method).
*   Added the [documentation for merchant service](https://global.alipay.com/docs/ac/merchant_service), which provides tutorials about merchant operations.
*   Added the contact information of [Alipay Merchant Service risk operation support](https://global.alipay.com/docs/support#QULaN).

### Document improvements

*   Modified the domain names for Cashier Payment and Auto Debit to which API requests are sent. For details, see [Call an API](https://global.alipay.com/docs/ac/ams/api#call).
*   Modified the format of `Request-Time` to a timestamp whose value is accurate to milliseconds. For details, see [Construct the content to be signed](https://global.alipay.com/docs/ac/ams/digital_signature#Adgbs).

May 2023
--------

### Enhanced

*   Added the enumeration value `ZALOPAY` for Cashier Payment and Auto Debit in [_Payment methods_](https://global.alipay.com/docs/ac/ref/payment_method).
*   Expressed the transaction amount in major units. For more information, see the following documents:

*   [_Settle and reconcile_](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle) for Cashier Payment
*   [_Transaction Items_](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [_Settlement Items_](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [_Settlement Summary_](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [_Settle and reconcile_](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle) for Auto Debit
*   [_Transaction Items_](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [_Settlement Items_](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [_Settlement Summary_](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Changed the length of the parameter _customerBelongsTo_ from 16 to 64 in the request parameters of the [consult](https://global.alipay.com/docs/ac/ams/authconsult) and [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) APIs.
*   Changed the length of the parameter _paymentMethod.paymentMethodType_ from 32 to 64 in the request parameters of the [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement) API.

April 2023
----------

### Enhanced

*   Added the payment method type OTC in [_Payment methods_](https://global.alipay.com/docs/ac/cashierpay/payment_method).
*   Added the enumeration value `KREDIVO_ID` for Cashier Payment in [_Payment methods_](https://global.alipay.com/docs/ac/ref/payment_method).
*   Changed the download address of the test wallet for Android in [_Test wallet_](https://global.alipay.com/docs/ac/ref/testwallet).
*   Added the parameter _cardInfo.threeDSResult_ in the response parameters of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Added the parameter _cardInfo.threeDSResult_ in the request parameters of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.

### Deprecated

*   Deprecated the parameter _redirectActionForm_ in the response parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Deprecated the parameter _authUrl_ in the response parameters of the [consult](https://global.alipay.com/docs/ac/ams/authconsult) API.
*   Deprecated the parameter _cardInfo.eci_ in the response parameters of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Deprecated the parameter _cardInfo.eci_ in the request parameters of the [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) API.

### Document improvements

*   Added the description of Blik in the _Collect or display extra information_ section of [_Pay with card-excluded payment methods_](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)_._
*   Updated the description of the parameters _order.env.clientIp_ and _order.env.userAgent_ for the payment method Blik in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

March 2023
----------

### Enhanced

*   Added [_Best practices for BNPL channels_](https://global.alipay.com/docs/ac/cashierpay/best_practice) for Cashier Payment_._
*   Added the enumeration values `KONBINI`, `FPX`, and `PAYEASY` for Cashier Payment; `PAYPAY` and `GrabPay` for Auto Debit in [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method).
*   Added the parameter _payerEmail_ for the scenario Payeasy and Konbini to the parameter _paymentMethod.paymentMethodMetaData_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the error code `AUTH_IN_PROCESS` in the [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) API.
*   Added the sample codes for QRIS in the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the enumeration value `OTC` to the field _paymentOptions.paymentMethodCategory_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.

### Document improvements

*   Updated the description of the two card collection modes in [_Pay with card payment methods_](https://global.alipay.com/docs/ac/cashierpay/card_payment)_._
*   Updated the description of the parameters _order.shipping.shippingPhoneNo, order.buyer.buyerPhoneNo, order.buyer.buyerName.firstName,_ and _order.shipping.shippingName.firstName_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Changed the length of the parameter _clientIp_ from 32 to 64 in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier), [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement), [pay (User-presented Mode Payment)](https://global.alipay.com/docs/ac/ams/upm), [pay (Order Code Payment)](https://global.alipay.com/docs/ac/ams/oc), and [pay (Entry Code Payment)](https://global.alipay.com/docs/ac/ams/ec).
*   Updated the description of the parameter _result.resultStatus_ in the request parameters of the [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) API.
*   Updated the card brands supported by Brazil, Peru, Mexico, and Chile in [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method).
*   Deleted the statement that the canceled transaction is not included in the settlement files in [_Cancel_](https://global.alipay.com/docs/ac/cashierpay/cancel).
*   Added a note of the default order expiry time of Mercado Pago in the _Obtain an asynchronous notification_ section of [_Pay with card-excluded payment methods_](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)_._
*   Added the description of Mercado Pago in the _Collect or display extra information_ section of [_Pay with card-excluded payment methods_](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)_._
*   Added the description of _codeValue_ in the _Invoke the payment process_ section of [_Pay with card-excluded payment methods_](https://global.alipay.com/docs/ac/cashierpay/noncard_payment?version=v1.40&pageVersion=3)_._
*   Updated the description of the [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) notification in [_Notifications_](https://global.alipay.com/docs/ac/cashierpay/notifications).
*   Renamed the "Payment method-incorporated solution" as the "Payment method-preposed solution".
*   Added the enumeration values `KONBINI`, `FPX`, and `PAYEASY` to the field _paymentMethodType._ For more information, see the following documents:

*   [_Transaction Items_](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [_Settlement Items_](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment

*   Added the enumeration values `PAYPAY` and `GrabPay` to the field _paymentMethodType._ For more information, see the following documents:

*   [_Transaction Items_](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [_Settlement Items_](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Updated the report sample in the _Sample 5_ section. For more information, see the following documents:

*   [_Settlement Items_](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [_Settlement Items_](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Updated the description of the parameter _originalTransactionId._ For more information, see the following documents:

*   [_Settle and reconcile_](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle) for Cashier Payment
*   [_Settle and reconcile_](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle) for Auto Debit
*   [_Transaction Items_](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [_Transaction Items_](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [_Settlement Items_](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [_Settlement Items_](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

February 2023
-------------

### Enhanced

*   Added the Cashier Payment documentation in [Chinese](https://global.alipay.com/docs/ac/cashier_payment_cn/introduction) and [English](https://global.alipay.com/docs/ac/cashierpay/overview) versions.
*   Added [Payment methods](https://global.alipay.com/docs/ac/ref/payment_method) for the use in the description of parameters.
*   Added the enumeration values `BILLEASE`, `QRIS`, `MERCADOPAGO_BR`, `MERCADOPAGO_MX`, `MERCADOPAGO_CL`, and `MERCADOPAGO_PE` to the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the enumeration values `BILLEASE`, `QRIS`, `MERCADOPAGO_BR`, `MERCADOPAGO_MX`, `MERCADOPAGO_CL`, and `MERCADOPAGO_PE` to the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the parameters _cpf_ and _payerEmail_ for the scenario Mercado Pago to the parameter _paymentMethod.paymentMethodMetaData_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the enumeration values `BILLEASE`, `QRIS`, `MERCADOPAGO_BR`, `MERCADOPAGO_MX`, `MERCADOPAGO_CL`, and `MERCADOPAGO_PE` to the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment

*   Added the enumeration value `REFUND_REVERSAL` to the parameter _transactionType._ For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Added the enumeration value `REFUND_REVERSAL` to the parameter _summaryType_. For more information, see the following documents:

*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

### Document improvements

*   Updated the capitalization of the request headers in [Overview](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur).
*   Updated the code sample in the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) and [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) APIs.
*   Updated the description of the parameter _paymentMethod.paymentMethodMetaData_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

January 2023
------------

### Enhanced

*   Added the enumeration values `AKULAKU_PAYLATER_PH` and `GRABPAY_MY` to the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the enumeration values `AKULAKU_PAYLATER_PH` and `GRABPAY_MY` to the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Changed the parameter _allowedPspRegions_ to _allowedPaymentMethodRegions_ in the request parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added [a list of enumeration values](https://global.alipay.com/docs/ac/ref/payment_method) to the parameter _PaymentOptions.paymentOptionDetail.supportCardBrands.cardBrand_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added [a list of enumeration values](https://global.alipay.com/docs/ac/ref/payment_method) to the parameter _PaymentOptions.paymentOptionDetail.supportCardBrands.logo.logoName_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the parameter _PaymentOptions.paymentOptionDetail.funding_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the parameters _paymentMethod.paymentMethodMetaData.dateOfBirth, paymentMethod.paymentMethodMetaData.businessNo, paymentMethod.paymentMethodMetaData.cardPasswordDigest, paymentMethod.paymentMethodMetaData.payerEmail,_ and _paymentMethod.paymentMethodMetaData.payMentMethodRegion_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the parameters _cardInfo.issuingCountry_, _cardInfo.funding_, and _cardInfo.paymentMethodRegion_ in the request parameters of the [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) API.
*   Added the parameters _cardInfo.issuingCountry_, _cardInfo.funding_, and _cardInfo.paymentMethodRegion_ in the response parameters of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Added the enumeration values `AKULAKU_PAYLATER_PH` and `GRABPAY_MY` to the parameter _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment

*   Added the parameters _issuingCountry_, _funding_, and _cardBrand._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment

*   Added the parameters _interchangeFeeAmountValue, interchangeFeeCurrency, schemeFeeAmountValue, schemeFeeCurrency, AcquirerMarkupFeeAmountValue,_ and _AcquirerMarkupFeeCurrency._ For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment

*   Added the enumeration values `AUTHORIZATION`, `VOID`, `CAPTURE`, and `DISPUTE` to the parameter _summaryType_. For more information, see the following documents:

*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment

### Document improvements

*   Modified the data type of the parameter _PaymentOptions.installment_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API to an object.
*   Updated the description of the parameter _PaymentOptions.paymentMethodRegion_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Updated the description of the parameter _feeAmountValue._ For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment

December 2022
-------------

### Enhanced

*   Added a drop-down box to filter the child parameters of the field _paymentMethodMetaData_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added a note indicating the rounding rule applied to IDR to the fields _paymentAmount.value_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API, _paymentAmount.value_ in the request parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API, _captureAmount.value_ in the request parameters of the [capture (Cashier Payment)](https://global.alipay.com/docs/ac/ams/capture) API, _paymentAmount.value_ in the request parameters of the [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement) API, _refundAmount.value_ in the request parameters of the [refund](https://global.alipay.com/docs/ac/ams/refund_online) API, and _declarationAmount.value_ in the request parameters of the [declare](https://global.alipay.com/docs/ac/ams/declare) API.
*   Added the enumeration values `DOLFIN`, `GRABPAY_SG`, `LINKAJA`, `OVO`, `GOPAY_ID`, `OCTOCLICKS`, `ONLINEBANKING_BNI`, `ONLINEBANKING_MANDIRI`, `ONLINEBANKING_BRI`, `ONLINEBANKING_BCA`, `BANKTRANSFER_MAYBANK`, `BANKTRANSFER_BNI`, `BANKTRANSFER_PERMATA`, `CIMBNIAGA`, `BANKTRANSFER_MANDIRI`, `BANKTRANSFER_BSI`, `ATMTRANSFER_ID`, and `PAYNOW` to the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the enumeration values `DOLFIN`, `GRABPAY_SG`, `LINKAJA`, `OVO`, `GOPAY_ID`, `OCTOCLICKS`, `ONLINEBANKING_BNI`, `ONLINEBANKING_MANDIRI`, `ONLINEBANKING_BRI`, `ONLINEBANKING_BCA`, `BANKTRANSFER_MAYBANK`, `BANKTRANSFER_BNI`, `BANKTRANSFER_PERMATA`, `CIMBNIAGA`, `BANKTRANSFER_MANDIRI`, `BANKTRANSFER_BSI`, `ATMTRANSFER_ID`, and `PAYNOW`to the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the enumeration value `MAYA` to the field _customerBelongsTo_ in the request parameters of the [consult](https://global.alipay.com/docs/ac/ams/authconsult) API.
*   Added the enumeration value `MAYA` to the field _customerBelongsTo_ in the request parameters of the [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) API.
*   Added the enumeration value `MAYA` to the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement) API.
*   Added the enumeration value `DOLFIN`, `GRABPAY_SG`, `LINKAJA`, `OVO`, `GOPAY_ID`, `OCTOCLICKS`, `ONLINEBANKING_BNI`, `ONLINEBANKING_MANDIRI`, `ONLINEBANKING_BRI`, `ONLINEBANKING_BCA`, `BANKTRANSFER_MAYBANK`, `BANKTRANSFER_BNI`, `BANKTRANSFER_PERMATA`, `CIMBNIAGA`, `BANKTRANSFER_MANDIRI`, `BANKTRANSFER_BSI`, `ATMTRANSFER_ID`, and `PAYNOW` to the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment

*   Added the enumeration value `MAYA` to the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

November 2022
-------------

### Enhanced

*   Added the error code FRAUD\_REJECT in the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier), [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online), and [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) APIs.
*   Added the error code SUSPECTED\_RISK in the [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) and [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) APIs.
*   Added the enumeration value `PROMPTPAY` to the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the enumeration value `PROMPTPAY` to the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the enumeration value `EASYPAISA` to the field _customerBelongsTo_ in the request parameters of the [consult](https://global.alipay.com/docs/ac/ams/authconsult) and [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) APIs.
*   Added the enumeration value `EASYPAISA` to the field _paymentMethodType_ in the request parameters of the [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement) API.
*   Added the error code `NO_PAY_OPTIONS` in the [consult](https://global.alipay.com/docs/ac/ams/authconsult) and [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp) APIs.
*   Added the enumeration value `PROMPTPAY` to the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment

*   Added the enumeration value `EASYPAISA` to the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

### Deprecated

*   Deprecated the field _cookieId_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

### Document improvements

*   Modified the description of the error code RISK\_REJECT in the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier), [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online), and [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) APIs.
*   Modified the description of the fields _orderCodeForm, orderCodeForm.codeDetails. codeValue_ in the response parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Modified the description of the fields _order.env.deviceTokenId, shipToEmail,_ and _goodsCategory_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

October 2022
------------

### Enhanced

*   Added the _paymentOptions.intallments_ field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the _paymentOptions.paymentOptionDetail.supportBanks_ field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the enumeration value `PAYPAY` to the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the enumeration value `WALLET` to the field _paymentOptions.paymentMethodCategory_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the error code CURRENCY\_NOT\_SUPPORT in the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the fields _blikCode_ and _payerEmail_ as child parameters to the field _paymentMethodMetaData_._paymentMethodMetaData_ in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the _paymentMethod.paymentMethodMetaData.bankIdentifierCode_ field in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the _paymentMethod.paymentMethodMetaData.cpf_ field in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the description of the fields order.buyer.buyerPhoneNo and order.buyer.buyerEmail in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the description of the field paymentMethod.paymentMethodMetaData.billingAddress in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the description of the field _paymentMethod.paymentMethodMetaData.cpf_ in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the value range to the field _creditPayPlan.installmentNum_ in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the enumeration value `PAYPAY` to the field _paymentMethod.paymentMethodType_ in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the error code MULTI\_CAPTURE\_NOT\_SUPPORTED in the [capture (Cashier Payment)](https://global.alipay.com/docs/ac/ams/capture) and [notifyCapture (Cashier Payment)](https://global.alipay.com/docs/ac/ams/notify_capture) APIs.
*   Added the field _disputeJudgedTime_ in the request parameters of [notifyDispute](https://global.alipay.com/docs/ac/ams/notify_dispute) API.
*   Added the description of the field _disputeJudgedResult_ in the request parameters of [notifyDispute](https://global.alipay.com/docs/ac/ams/notify_dispute) API.
*   Added the field _installmentsNum._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Added the fields _disputeHandlingFee_, _disputeHandlingFeeCurrency_, _disputeReverseFee_, and _disputeReverseFeeCurrency_. For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Added the enumeration value `PAYPAY` to the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Updated the description of the fields _settlementAmountValue_, _feeAmountValue_, and _taxFeeAmountValue._ For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Added the sample 4 applicable when the acquirer is Hundsun. For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

### Deprecated

*   Deprecated the _card_ child field of the _paymentOptions.paymentOptionDetail_ field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Deprecated the `ACCEPT_BY_ALIPAY` value of the _disputeJudgedResult_ field in the request parameters of [notifyDispute](https://global.alipay.com/docs/ac/ams/notify_dispute) API.
*   Deprecated the error codes of the [notifyDispute](https://global.alipay.com/docs/ac/ams/notify_dispute) API.

### Document improvements

*   Modified the enumeration value `MIXEDCARD` to `CARD` of the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Capitalized the enumeration values of the field _paymentOptions.paymentMethodCategory_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Modified the description of the field _paymentOptions.paymentOptionDetail_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Modified the paymentOptions.installments.interestRate to an optional field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Modified the data type of the _paymentMethod.paymentMethodMetaData_ field to an object and modified its description.
*   Modified the enumeration value `MIXEDCARD` to `CARD` of the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Modified the enumeration value `MIXEDCARD` to `CARD` of the field _paymentMethodType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

September 2022
--------------

### Enhanced

*   Updated the [sign a request and verify the signature](https://global.alipay.com/docs/ac/ams/digital_signature) documentation.
*   Updated the [Support](https://global.alipay.com/docs/support) documentation.
*   Added the _merchantRegion_ field in the request parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added enumeration values to the field _paymentOptions.paymentMethodType_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the _paymentOptions.paymentMethodCategory_ field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the field _paymentOptions.paymentOptionDetail_ in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Added the fields _paymentFactor, paymentMethod.paymentMethodId_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added enumeration values to the field _paymentMethod.paymentMethodType_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the field _card_ as a child parameter to the field _paymentMethodMetaData_ in the request parameters of [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the _merchantRegion_ field in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added the [capture (Cashier Payment)](https://global.alipay.com/docs/ac/ams/capture) API.
*   Added the fields _cardInfo and acquirerReferenceNo_ in the request parameters of the [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online) API.
*   Added the [notifyCapture (Cashier Payment)](https://global.alipay.com/docs/ac/ams/notify_capture) API.
*   Added the fields _cardInfo and acquirerReferenceNo_ in the response parameters of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Added the field _acquirerReferenceNo_ in the response parameters of the [refund](https://global.alipay.com/docs/ac/ams/refund_online) API.
*   Added the error code ORDER\_STATUS\_INVALID in the [cancel](https://global.alipay.com/docs/ac/ams/paymentc_online) API.

### Deprecated

*   Deprecated the field _paymentMethod.card_ in the request parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

### Document improvements

*   Modified the description of the _paymentOptions.paymentMethodRegion_ field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Modified the minimum length of the _paymentOptions.logo.logoName_ field in the response parameters of the [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier) API.
*   Modified the description of the _result.resultStatus_ field in the response parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Modified the name of the error code `PAYMENT_METHOD_NOT_SUPPORTED` in the [refund](https://global.alipay.com/docs/ac/ams/refund_online) API.
*   Updated the result process logic of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Modified the description of the _transactions_ field in the response parameters of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Updated the payment result codes of the [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online) API.
*   Modified the description of the file path naming rule and the field _seq_. For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Modified the description of the field _customerId._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Added the field _acquirer._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Added the field _acquirerReferenceNo._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Modified the description of the fields _transactionId, originalTransactionId, transactionRequestId, referenceTransactionId, paymentMethodType,_ and _transactionType._ For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Modified the description of the field _settlementBatchId._ For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Added the fields _taxFeeAmountValue and taxFeeCurrency._ For more information, see the following documents:

*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

August 2022
-----------

### Enhanced

*   Deprecated the **Data dictionary** for APIs.
*   Deprecated the APIs about registration for online payments: **registration**, **notifyRegistrationStatus**, **inquiryRegistrationStatus**, **inquiryRegistrationInfo**.

### Document improvements

*   Modified the description of the _referenceTransactionId_ field. For more information, see the following documents:

*   [Transaction Items](https://global.alipay.com/docs/ac/cashierpay/transactionitems) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Transaction Items](https://global.alipay.com/docs/ac/autodebitpay/transactionitems) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit

*   Added the fields _processingFeeAmountValue_ and _processingFeeCurrency_ to the **Settle and reconcile** documents. For more information, see the following documents:

*   [Settle and reconcile](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle) for Cashier Payment
*   [Settle and reconcile](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle) for Auto Debit

*   Modified the description of the _feeAmountValue_ field. For more information, see the following documents:

*   [Settle and reconcile](https://global.alipay.com/docs/ac/cashierpay/reconcile_settle) for Cashier Payment
*   [Settlement Items](https://global.alipay.com/docs/ac/cashierpay/settlementitems) for Cashier Payment
*   [Settlement Summary](https://global.alipay.com/docs/ac/cashierpay/settlementsummary) for Cashier Payment
*   [Settle and reconcile](https://global.alipay.com/docs/ac/autodebitpay/reconcile_settle) for Auto Debit
*   [Settlement Items](https://global.alipay.com/docs/ac/autodebitpay/settlementitems) for Auto Debit
*   [Settlement Summary](https://global.alipay.com/docs/ac/autodebitpay/settlementsummary) for Auto Debit

*   Modified the description of the _paymentMethodMetaData_ field in the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.

July 2022
---------

### Enhanced

*   Added the _userRegion_ field in the request parameters and the _paymentData_ field in the response parameters of the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Added two error codes `REFUND_NOT_SUPPORTED`and `PARTIAL_REFUND_NOT_SUPPORTED` in the [refund](https://global.alipay.com/docs/ac/ams/refund_online) API.
*   Added [Best practices for BNPL channels](https://global.alipay.com/docs/ac/cashierpay/best_practice#QSnOx) for Cashier Payment.
*   Added the _goodsCategory_ field to [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) and [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement) APIs.
*   Added Akulaku PayLater payment method to Cashier Payment, and Boost eWallet to Cashier Payment and Auto Debit. For more information, see the following documents:

*   [consult (Cashier Payment)](https://global.alipay.com/docs/ac/ams/consult_cashier)
*   [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier)
*   [Transaction Items for Cashier Payment](https://global.alipay.com/docs/ac/cashierpay/transactionitems)
*   [Settlement Items for Cashier Payment](https://global.alipay.com/docs/ac/cashierpay/settlementitems)
*   [consult](https://global.alipay.com/docs/ac/ams/authconsult)
*   [applyToken](https://global.alipay.com/docs/ac/ams/accesstokenapp)
*   [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement)
*   [Transaction Items for Auto Debit](https://global.alipay.com/docs/ac/autodebitpay/transactionitems)
*   [Settlement Items for Auto Debit](https://global.alipay.com/docs/ac/autodebitpay/settlementitems)

### Document improvements

*   Updated the result process logic in the [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier) API.
*   Updated the error codes in the interfaces: **consult**, **applyToken**, **revoke**, **pay (Cashier Payment)**, **pay (Auto Debit)**, **notifyPayment**, **inquiryPayment**, **cancel**, **refund**, **inquiryRefund**, **notifyRefund**, **declare**, **inquiryDeclarationRequests**, **pay (User-presented Mode Payment)**, **pay (Order Code Payment)**, **pay (Entry Code Payment)**.

May 2022
--------

Added the consult (Cashier Payment) and notifyRefund interfaces.

Updated the pay (Cashier Payment) document:

*   Added the paymentMethod.paymentMethodMetaData field in Request parameters.
*   Added some new enumeration values in the paymentMethod.paymentMethodType field.
*   Modfied the field description of settlementStrategy.settlementCurrency.
*   Added the following error codes:

*   INVALID\_PAYMENT\_METHOD\_META\_DATA
*   INCORRECT\_BLIKCODE
*   SETTLE\_CONTRACT\_NOT\_MATCH

Updated the notifyPayment document:

*   Added the new enumeration value of `PAYMENT_PENDING` in the notifyType field.

Updated the inquiryPayment document:

*   Added the new enumeration value of `PENDING` in the paymentStatus field.

Updated the refund document:

*   Added the refundNotifyUrl field in Request parameters.
*   Added the error code: REFUND\_IN\_PROCESS

Updated the Transaction Items, Settlement Items, and Settlement Summary documents under Cashier Payment:

*   Added the following new enumeration values in the paymentMethodType field in Transaction Items and Settlement Items:

*   IDEAL
*   GIROPAY
*   SOFORT
*   PAYU
*   P24
*   BLIK
*   EPS
*   BANCONTACT
*   PIX

*   Added the following fields in Settlement Items and Settlement Summary:

*   processingFeeAmountValue
*   processingFeeCurrency

*   Modified the Report path and name parts in Settlement Items and Settlement Summary.

April 2022
----------

*   Added the merchantRegion field in the request parameters of the following interfaces:

*   pay (Cashier Payment)
*   consult
*   applyToken
*   pay (User-presented Mode Payment)
*   pay (Order Code Payment)
*   pay (Entry Code Payment)

*   Modified Customs codes in the sample codes of the following interfaces:

*   declare: modified ZHENGZHOU to ZONGSHU
*   inquiryDeclarationRequests: modified shenzhen to ZONGSHU

*   The Business Registration Country/Region field is moved from the **Welcome** page to the **Create New Application** page.

March 2022
----------

*   Added the [Sandbox](https://global.alipay.com/docs/ac/ref/sandbox) documentation.
*   Added a new version of the [Cashier Payment](https://global.alipay.com/docs/ac/cashierpay/overview) documentation.
*   Added a new version of the [Auto Debit](https://global.alipay.com/docs/ac/autodebitpay/overview) documentation.
*   Added the redirectActionForm field in the response parameters of the inquiryPayment interface.

February 2022
-------------

*   Deleted the initAuthentication and verifyAuthentication interfaces.
*   Added the USER\_NOT\_EXIST error code in the pay (Auto Debit).

January 2022
------------

Added the grossSettlementAmount and settlementQuote fields in the following interfaces:

*   notifyPayment
*   inquiryPayment
*   refund
*   inquiryRefund

Updated the pay (Cashier Payment) document:

*   Added the following error codes:

*   INVALID\_MERCHANT\_STATUS
*   MERCHANT\_KYB\_NOT\_QUALIFIED
*   NO\_PAY\_OPTIONS

*   Deleted the following error codes:

*   SUCCESS
*   ORDER\_NOT\_EXIST

Updated the pay (Auto Debit) document:

*   Deleted the following fields:

*   Request parameters:

*   merchant.store
*   order.env.storeTerminalId
*   order.env.storeTerminalRequestTime
*   payToMethod
*   paymentMethod.paymentMethodMetaData
*   isAuthorization
*   paymentVerificationData
*   paymentFactor

*   Response parameters:

*   authExpiryTime
*   challengeActionForm
*   redirectActionForm
*   orderCodeForm

*   Modified the following fields from Optional to Required:

*   Request parameters:

*   paymentMethod.paymentMethodId
*   env
*   env.terminalType
*   settlementStrategy.settlementCurrency

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   INVALID\_MERCHANT\_STATUS
*   MERCHANT\_KYB\_NOT\_QUALIFIED
*   USER\_PAYMENT\_VERIFICATION\_FAILED

*   Deleted the following error codes:

*   USER\_NOT\_EXIST
*   ORDER\_NOT\_EXIST

Updated the notifyPayment document:

*   Deleted the following fields:

*   Request parameters:

*   notifyType: OFFLINE\_PAYMENT\_CODE
*   result.resultStatus: U

*   Modified the following fields from Optional to Required:

*   Request parameters:

*   paymentCreateTime
*   paymentId
*   result.resultMessage

*   Added the error codes of pay (Cashier Payment) and pay (Auto Debit).

Updated the inquiryPayment document:

*   Deleted the following fields:

*   Response parameters:

*   authExpiryTime
*   redirectActionForm
*   transaction.transactionType: PAYMENT, CANCEL, AUTHORIZATION, CAPTURE, VOID
*   transactionTime

*   Modified the following fields from Optional to Required:

*   Response parameters:

*   result
*   result.resultMessage
*   transactions.transactionId

*   Added the following two result codes tables:

*   Payment result codes
*   Transaction result codes

*   Deleted the following error codes:

*   RISK\_REJECT
*   USER\_KYC\_NOT\_QUALIFIED

Updated the cancel document:

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

Updated the refund document:

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   INVALID\_MERCHANT\_STATUS
*   ORDER\_IS\_CLOSED

Updated the inquiryRefund document:

*   Added the following field:

*   Response parameters:

*   refundStatus: FAIL

*   Deleted the following error codes:

*   RISK\_REJECT
*   MERCHANT\_NOT\_REGISTERED
*   INVALID\_CONTRACT

*   Added a Refund result codes table.

Updated the consult document:

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   INVALID\_CLIENT\_STATUS
*   OAUTH\_FAILED
*   UNKNOWN\_CLIENT

Updated the applyToken document:

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   INVALID\_CLIENT\_STATUS
*   OAUTH\_FAILED
*   UNKNOWN\_CLIENT
*   USER\_NOT\_EXIST
*   USER\_STATUS\_ABNORMAL

Updated the revoke document:

*   Modified the following field from Optional to Required:

*   Response parameters:

*   result.resultMessage

*   Added the following error codes:

*   CLIENT\_FORBIDDEN\_ACCESS\_API
*   INVALID\_CLIENT\_STATUS
*   OAUTH\_FAILED
*   UNKNOWN\_CLIENT

Added the grossSettlementAmount and settlementQuote fields in the inquiryRefund interface.

Updated the pay (User-presented Mode Payment) document:

*   Deleted the following fields:

*   Request parameters:

*   isAuthorization
*   paymentFactor.isPaymentEvaluation
*   paymentMethod.paymentMethodMetaData
*   paymentRedirectUrl
*   paymentVerificationData
*   payToMethod

*   Response parameters:

*   authExpiryTime
*   challengeActionForm.challengeRenderValue
*   orderCodeForm

*   Added the settlementStrategy field.
*   Modified the paymentMethod.paymentMethodId field from Optional to Required.

Updated the pay (Order Code Payment) document:

*   Deleted the following fields:

*   Request parameters:

*   isAuthorization
*   paymentFactor.isPaymentEvaluation
*   paymentMethod.paymentMethodMetaData
*   paymentVerificationData
*   payToMethod

*   Response parameters:

*   authExpiryTime
*   challengeActionForm.challengeRenderValue

*   Added the settlementStrategy field.
*   Modified the orderCodeForm field from Optional to Required.

Updated the pay (Entry Code Payment) document:

*   Deleted the following fields:

*   Request parameters:

*   isAuthorization
*   paymentFactor.isPaymentEvaluation
*   paymentMethod.paymentMethodMetaData
*   paymentVerificationData
*   payToMethod

*   Response parameters:

*   authExpiryTime
*   challengeActionForm.challengeRenderValue
*   orderCodeForm

*   Added the settlementStrategy field.
*   Modified the order.env and the order.env.userAgent fields from Optional to Required.

December 2021
-------------

*   Auto Debit added the authorization result notification functionality. Therefore, the following documentation are reorganized:

*   [Introduction](https://global.alipay.com/docs/ac/agreementpayment/intro)
*   [Authorization and payment](https://global.alipay.com/docs/ac/agreementpayment/payment)
*   [Best practice](https://global.alipay.com/docs/ac/agreementpayment/autodebit_bp)
*   [API list](https://global.alipay.com/docs/ac/agreementpayment/apis)

For Online payment and In-store payment:

*   Added the refund inquiry functionality in the following products:

*   Cashier Payment
*   Auto Debit
*   User-presented Mode Payment
*   Order Code Payment
*   Entry Code Payment

*   Therefore, the following documentation are reorganized:

*   Post-payment service
*   Best practice
*   API list

Updated the pay (Cashier Payment) document:

**Request parameters**

*   Deleted the following fields:

*   merchant.store
*   order.env.storeTerminalId
*   order.env.storeTerminalRequestTime
*   payToMethod
*   paymentMethod.paymentMethodId
*   paymentMethod.paymentMethodMetaData
*   isAuthorization
*   paymentVerificationData
*   paymentFactor

*   Modified the following fields from Optional to Required:

*   order.env
*   settlementStrategy.settlementCurrency

**Response parameters**

*   Deleted the following fields:

*   result.resultStatus: S 
*   paymentTime
*   authExpiryTime
*   challegeActionForm
*   redirectActionForm.method: SCAN
*   orderCodeForm.paymentMethodType
*   settlementQuote
*   grossSettlementAmount

*   Modified the following fields from Optional to Required:

*   orderCodeForm.expireTime
*   orderCodeForm.codeDetails
*   result.resultMessage

Added the userLoginId field in the applyToken interface.

Added the following fields in the pay (Cashier Payment) and pay (Auto Debit) interfaces:

*   schemeUrl
*   applinkUrl
*   normalUrl
*   appIdentifier

Added the new enumeration values of `BPI` and `RABBIT_LINE_PAY` in the following APIs:

*   pay (Cashier Payment): paymentMethod.paymentMethodType

Added the new enumeration value of `RABBIT_LINE_PAY` in the following APIs:

*   pay (Auto Debit): paymentMethod.paymentMethodType
*   consult: customerBelongsTo
*   applyToken: customerBelongsTo

November 2021
-------------

*   Auto Debit: Updated the [Client side integration with wallet](https://global.alipay.com/docs/ac/agreementpayment/clientsideint) document.

October 2021
------------

*   Cashier Payment: Updated the [Client side integration with wallet](https://global.alipay.com/docs/ac/cashierpayment/clientsideint) document.

*   Auto Debit added the payment result notification functionality. Therefore, the following documentation are reorganized:

*   [Introduction](https://global.alipay.com/docs/ac/agreementpayment/intro)
*   [Authorization and payment](https://global.alipay.com/docs/ac/agreementpayment/payment)
*   [Best practice](https://global.alipay.com/docs/ac/agreementpayment/autodebit_bp)
*   [API list](https://global.alipay.com/docs/ac/agreementpayment/apis)

*   Added the following new APIs in online payments:

*   [notifyAuthorization](https://global.alipay.com/docs/ac/ams/notifyauth)
*   [inquiryRefund](https://global.alipay.com/docs/ac/ams/ir_online)
*   [declare](https://global.alipay.com/docs/ac/ams/declare)
*   [inquiryDeclarationRequests](https://global.alipay.com/docs/ac/ams/inquirydeclare)

*   Added the following new API in in-store payments:

*   [inquiryRefund](https://global.alipay.com/docs/ac/ams/ir)

September 2021
--------------

*   The following terms are renamed:



| **Obsolete term** | **Current term** | **Comments** |
| --- | --- | --- |
| PMP | Alipay+ MPP | The meaning of the current term is the same as the obsolete term. |
| Connect Wallet |
| H5 | WAP |
| mobile website |



*   New introduction videos of online payment and in-store payment scenarios are added. You can go to [Online payment](https://global.alipay.com/docs/onlinepayment) and [In-store payment](https://global.alipay.com/docs/instorepayment) to view details.

August 2021
-----------

*   Added MULTIPLE\_REFUNDS\_NOT\_SUPPORTED of error code in the following APIs:

*   [refund](https://global.alipay.com/docs/ac/ams/refund_online)
*   [refund](https://global.alipay.com/docs/ac/ams/refund)

*   Removed the inquiryUserInfo interface is removed.

*   Added the _paymentNotifyUrl_ field in the [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement) interface.

July 2021
---------

*   Added the error code of USER\_KYC\_NOT\_QUALIFIED in the following APIs:

*   [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier)
*   [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement)
*   [pay (User-presented Mode Payment)](https://global.alipay.com/docs/ac/ams/upm)
*   [pay (Order Code Payment)](https://global.alipay.com/docs/ac/ams/oc)
*   [pay (Entry Code Payment)](https://global.alipay.com/docs/ac/ams/ec)
*   [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn_online)
*   [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri_online)
*   [notifyPayment](https://global.alipay.com/docs/ac/ams/paymentrn)
*   [inquiryPayment](https://global.alipay.com/docs/ac/ams/paymentri)

*   Modified the _orderCodeForm.codeDetails_ field from Required to Optional for the following interfaces:

*   [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier)
*   [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement)
*   [pay (User-presented Mode Payment)](https://global.alipay.com/docs/ac/ams/upm)
*   [pay (Entry Code Payment)](https://global.alipay.com/docs/ac/ams/ec)

*   Deleted the orderCodeForm.codeDetails.codeValueType field in the following APIs:

*   [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier)
*   [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement)

May 2021
--------

*   Alipay Docs redesigned with improved user experience and new information architecture. New docs to assist new users:

*   [Integration Guide](https://global.alipay.com/docs/integration)
*   [Tools](https://global.alipay.com/docs/tools)

*   Reorganized the structure of API-related instruction documentation.

*   Added the following documentation:

*   [Message encoding](https://global.alipay.com/docs/ac/ams/me)

*   Renamed the following documentation titles:

*   API fundamentals -> [Overview](https://global.alipay.com/docs/ac/ams/api_fund)
*   Digital signature -> [Sign a request and validate the signature](https://global.alipay.com/docs/ac/ams/digital_signature)
*   Encryption -> [Encrypt and decrypt a message](https://global.alipay.com/docs/ac/ams/cgl4ti)

*   Removed the following documentation to the corresponding product documentation:

*   Settlement Items
*   Settlement Summary
*   Transaction Items

For example, you can go to Cashier Payment > Reports and reconciliation > Settlement Items ([https://global.alipay.com/docs/ac/cashierpayment/settlementitems\_online](https://global.alipay.com/docs/ac/cashierpayment/settlementitems_online)) to view details.

*   Terminology renaming. The following term is renamed:

*   Consumer\-presented Mode Payment -> User-presented Mode Payment

April 2021
----------

*   Added a new field and enum (appId and MINI\_APP) to the following APIs:

*   [pay (Cashier Payment)](https://global.alipay.com/docs/ac/ams/payment_cashier)
*   [pay (Auto Debit)](https://global.alipay.com/docs/ac/ams/payment_agreement)
*   [consult](https://global.alipay.com/docs/ac/ams/authconsult)

March 2021
----------

*   Added new settlement modes to the following products:

*   [Cashier Payment](https://global.alipay.com/docs/ac/cashierpayment/reports)
*   [Auto Debit](https://global.alipay.com/docs/ac/agreementpayment/report)
*   [User-presented Mode Payment](https://global.alipay.com/docs/ac/ams_upm/settlmt_recon)
*   [Order Code Payment](https://global.alipay.com/docs/ac/ams_oc/settlmt_recon)
*   [Entry Code Payment](https://global.alipay.com/docs/ac/ams_ec/settlmt_recon)

Removed the following fields from the Settlement Summary file for each product:

*   transactionAmountValue
*   transactionCurrency

*   Deleted INVALID\_CODE of error code in the following APIs:

*   [pay (User-presented Mode Payment)](https://global.alipay.com/docs/ac/ams/upm)
*   [pay (Order Code Payment)](https://global.alipay.com/docs/ac/ams/oc)
*   [pay (Entry Code Payment)](https://global.alipay.com/docs/ac/ams/oc)

*   Added INVALID\_PAYMENT\_CODE of error code in the following API:

*   [pay (User-presented Mode Payment)](https://global.alipay.com/docs/ac/ams/upm)

December 2020
-------------

*   Renamed the following term:



| **Obsolete term** | **Current term** | **Comments** |
| --- | --- | --- |
| PSP | PMP | The obsolete term might be still displayed in codes, for example, API specifications, Java code specifications, or other places where technical elements exist. The meaning of the obsolete term is not changed. |



*   New versions of Product APIs for online payment and in-store payment products are released in December. The API documentation format has been updated to a new version for better user experience. You can now access subfields in the same documentation. Previously, subfields were only available in data dictionary. You can go to **API Reference** > **Product APIs** \> **Online payments** ([https://global.alipay.com/docs/ac/ams/payment\_cashier](https://global.alipay.com/docs/ac/ams/payment_cashier)) to explore the new version.

May 2020
--------

A new version of Alipay Docs is released in May. Technical documentation on original portal ([https://global.alipay.com/open/doc.htm](https://global.alipay.com/open/doc.htm)) is merged to this new site for a better user experience. You can go to **Documentation** > **Legacy Documentation** ([https://global.alipay.com/docs/ac/legacy/legacydoc](https://global.alipay.com/docs/ac/legacy/legacydoc)) to view details.

Tab 1

![Image 3](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 4](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)

#### Is this page helpful?

#### On this page

[March 2024](#qe1T2 "March 2024")

[Enhanced](#NbsIu "Enhanced")

[February 2024](#pOU4K "February 2024")

[Enhanced](#MOtKI "Enhanced")

[January 2024](#28qpf "January 2024")

[Enhanced](#ZmIHJ "Enhanced")

[December 2023](#tp1qM "December 2023")

[Enhanced](#zUTuB "Enhanced")

[November 2023](#mQybi "November 2023")

[Enhanced](#ip1Wv "Enhanced")

[Deprecated](#sjXzp "Deprecated")

[October 2023](#v6dZi "October 2023")

[Enhanced](#BYA9u "Enhanced")

[Deprecated](#fcd9y "Deprecated")

[September 2023](#nDrFA "September 2023")

[Enhanced](#gCLUn "Enhanced")

[Deprecated](#sOtQI "Deprecated")

[August 2023](#bFp89 "August 2023")

[Enhanced](#Y22UQ "Enhanced")

[July 2023](#KT6zv "July 2023")

[Enhanced](#BPYQZ "Enhanced")

[Deprecated](#TlWyC "Deprecated")

[June 2023](#6uGBq "June 2023")

[Enhanced](#gsgop "Enhanced")

[Document improvements](#FnQjz "Document improvements")

[May 2023](#BcswH "May 2023")

[Enhanced](#AVU4b "Enhanced")

[April 2023](#G1LX3 "April 2023")

[Enhanced](#vfefy "Enhanced")

[Deprecated](#Wa9KJ "Deprecated")

[Document improvements](#KqFnN "Document improvements")

[March 2023](#19VCl "March 2023")

[Enhanced](#J38Xi "Enhanced")

[Document improvements](#Taf43 "Document improvements")

[February 2023](#T9T3T "February 2023")

[Enhanced](#wNbNc "Enhanced")

[Document improvements](#KYA1A "Document improvements")

[January 2023](#CoI6G "January 2023")

[Enhanced](#i2Z2X "Enhanced")

[Document improvements](#NqLwZ "Document improvements")

[December 2022](#PyhWv "December 2022")

[Enhanced](#RVDH4 "Enhanced")

[November 2022](#IbizC "November 2022")

[Enhanced](#qwyXh "Enhanced")

[Deprecated](#czoPW "Deprecated")

[Document improvements](#ypW6N "Document improvements")

[October 2022](#6Yfov "October 2022")

[Enhanced](#GIsZx "Enhanced")

[Deprecated](#urPYY "Deprecated")

[Document improvements](#YqHZe "Document improvements")

[September 2022](#C1sXp "September 2022")

[Enhanced](#Wmjf9 "Enhanced")

[Deprecated](#ooZbF "Deprecated")

[Document improvements](#Brmjv "Document improvements")

[August 2022](#jMYC2 "August 2022")

[Enhanced](#l6yGw "Enhanced")

[Document improvements](#me3S4 "Document improvements")

[July 2022](#c1SE1 "July 2022")

[Enhanced](#zevaL "Enhanced")

[Document improvements](#1uQS6 "Document improvements")

[May 2022](#DUcmN "May 2022")

[April 2022](#Ol3oh "April 2022")

[March 2022](#RA3mX "March 2022")

[February 2022](#dHoc6 "February 2022")

[January 2022](#jRJhq "January 2022")

[December 2021](#BI8S8 "December 2021")

[November 2021](#pSfYF "November 2021")

[October 2021](#cH6R0 "October 2021")

[September 2021](#TBZWK "September 2021")

[August 2021](#BCzvi "August 2021")

[July 2021](#tXTLa "July 2021")

[May 2021](#btKIK "May 2021")

[April 2021](#k25f6 "April 2021")

[March 2021](#ClKlz "March 2021")

[December 2020](#wSY1q "December 2020")

[May 2020](#7NFSO "May 2020")

      

Feedback