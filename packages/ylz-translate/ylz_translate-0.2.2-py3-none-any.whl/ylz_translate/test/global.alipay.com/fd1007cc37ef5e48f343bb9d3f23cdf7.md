Antom Dashboard | Alipay, China's leading third-party online payment solution
===============
                        

[![Image 1: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/d66c43c0-440d-4c97-9976-f2028a2c8c5e.svg)![Image 2: Alipay, China's leading third-party online payment solution](https://ac.alipay.com/storage/2024/3/26/a48bd336-aea0-4f16-bf83-616eacbb4434.svg)](/docs/)

[Log In](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fdashboard_en)

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

Antom Dashboard
===============

2024-05-15 06:07

Get started receiving online payments in just a few steps. Antom Dashboard allows you to conduct sandbox testing with a suite of integration resources and tools, activate your merchant account and execute live testing before accepting online payments. Antom is dedicated to providing a convenient and efficient payment solution for you and your customers.

Register & log in
-----------------

To register for an Antom Dashboard account, you must first obtain an internal invitation link from Antom. Contact [Antom Business Support](https://global.alipay.com/docs/support#AVq3T) to get the invitation link and complete the sign-up process.

After registration, log in to [Antom Dashboard](https://dashboard.alipay.com/global-payments/home). Your merchant account name is displayed in the upper-left corner of the page.

![Image 3: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712460187565-b69dde23-6b90-49f0-8994-cde2cbfc08da.png)

You can create a new merchant account by clicking **\+ Create a merchant account**. After creating the account, you can modify the account information by clicking **Settings**![Image 4: image.png](https://yuque.antfin.com/images/lark/0/2023/png/119656509/1703062036421-1dea58a9-ac6d-4864-91fa-7a8bdce64ff7.png) > **Merchant account information** in the upper-right corner.

![Image 5: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712460292181-fa50eb9e-2723-41b9-8188-6aa3a2f5a029.png)

Test in sandbox
---------------

Before receiving online live payments, it is recommended to complete sandbox testing in test mode through the following steps:

1.  Sandbox configuration
2.  Sandbox integration
3.  Sandbox testing  
    

### Sandbox configuration

Before sandbox testing, you must first generate your keys and get the related integration sources for the sandbox environment.

#### Generate keys

You can generate keys using either one of the following methods:

*   Go to **Developer** > [**Quick Start**](https://dashboard.alipay.com/global-payments/developers/quickStart), find **Integration sources and tools**, select **Integration sources**, and click **Generate key**.
*   Go to **Developer** > [**Key configuration**](https://dashboard.alipay.com/global-payments/developers/iKeys), click **Generate key**.

For more details about generating keys, visit [API key configuration](https://global.alipay.com/docs/ac/ref/key_config_en).

![Image 6: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712476659413-59ad9033-5b9e-4b95-941d-2a439f884b7d.png)

> **Note**: In the event your private key is lost, click **Replace keys** to generate new keys. Remember to safeguard your private key for subsequent use.

#### Get integration resources

Antom provides the following integration resources for your sandbox integration and testing:

*   Gateway URL and client ID: Retrieve your sandbox environment's gateway URL and client ID using either one of the following methods:

*   Go to **Developer** > [**Quick start**](https://dashboard.alipay.com/global-payments/developers/quickStart), find **Integration resources and tools**, and select **Integration resources**.
*   [**Home Page**](https://dashboard.alipay.com/global-payments/home) > **Integration resources**.

*   Integration testing: Access testing resources for various payment methods tailored for integration testing at **Developer** > **Quick Start** > **Integration sources and tools** \> **Integration testing**.
*   Test wallet: Antom offers a test wallet app to facilitate end-to-end testing throughout your integration process. For details, see **Test App download** in [Testing resources](https://global.alipay.com/docs/ac/cashierpay/test).
*   Testing accounts: Use specified accounts to log in to the test wallet app. For details, see **Testing account** in [Testing resources](https://global.alipay.com/docs/ac/cashierpay/test).

### Sandbox integration  

Complete the sandbox integration and deployment in test mode by following the steps and code samples listed below:

*   [Checkout Payment](https://global.alipay.com/docs/ac/cashierpay/quickstart)
*   [Easy Pay](https://global.alipay.com/docs/ac/easypay_en/sdk)
*   [Auto Debit](https://global.alipay.com/docs/ac/autodebit_en/auth)
*   [Subscription Payment](https://global.alipay.com/docs/ac/subscriptionpay_en/activation)

### Sandbox testing

For effective sandbox testing, It is recommended to employ the following tools:



| **Testing tools** | **Description** | **Path** |
| --- | --- | --- |
| [API call simulation](https://global.alipay.com/docs/ac/ref/api_call_sim_en) | Test your APIs with online debugging tools and Postman script. | **Developer** > **API call simulation** |
| [Notification URL](https://dashboard.alipay.com/global-payments/developers/iNotify) | Configure your notification URL and use the developer tool to simulate the process of receiving and processing asynchronous notifications. | **Developer** > **Notification URL** |
| [Error scenario simulation](https://global.alipay.com/docs/ac/ref/error_scenario_sim_en) | Provide simulations of different API results and return the specified response for integration testing. | **Developer** > **Error scenario simulation** |
| [Test case](https://global.alipay.com/docs/ac/ref/test_case_en) | Validate your integration to ensure that your system is working correctly and is built with a high level of quality. | **Developer** > **Test case** |
| [Request log](https://dashboard.alipay.com/global-payments/developers/requestLog) | Search for your simulation requests. | **Developer** > **Request Log** |
| [Notification log](https://dashboard.alipay.com/global-payments/developers/notificationLog) | Search for your received simulation notifications. | **Developer** > **Notification Log** |



Go live
-------

Before conducting the integration testing in the live environment, ensure that your merchant account is activated and the Antom Dashboard mode is switched to live mode. Complete the integration testing in the live environment through the following steps:

1\. Activate account

Access the **Home Page**, click **Activat****e now**, enter the information as prompted on the page, and contact Antom Business Support to activate your payment methods and link your settlement account.

![Image 7: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712460538696-4df686c0-e54e-4ab8-a246-00564a6c4d0c.png)

> **Note**: After your merchant account is activated, the Antom Dashboard mode can be switched to live mode.
> 
> ![Image 8: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712460633181-cf3a8bac-736d-4927-991e-a6674f88fc45.png)

2\. Generate keys: Go to **Developer** > Keys configuration, click Generate key.

> **Note**: In the event your private key is lost, click **Replace keys** to generate new keys. Remember to safeguard your private key for subsequent use.

3\. Get gateway URL and client ID: Get your gateway URL and client ID for the live environment through Developer > Quick start > Integration resources and tools > Integration resources.

4.  Set notification URL: Set your notification URL to receive Antom notifications through **Developer** \> **Quick start** \> **Integration resources and tools** \> **Notification URL**.
5.  Update your coding in the live environment. After ensuring a test payment is received in the live environment, you can start to receive online payments.

View settlement info  

-----------------------

After you start receiving online payments, your settlement information is accessible under **Finance** in live mode.

### Balance info

Log in to Antom Dashboard, go to **Finance** > **Settlement overview** > **Bank account**, and click **\+ Add a new bank account** to link your bank account. Funds will be settled into your bank account by Antom within the specified settlement period. You can check your settled funds, unsettled funds, and settlement history in **Balance** under **Finance**.

![Image 9: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712461095770-6642219b-3bc2-492f-8769-8e78c9d9fdba.png)

### Settlement currency  

Antom settles funds in the default currency of your registration region. You can also set USD as your default settlement currency through the following steps:

1.  Go to **Finance** > **Settlement overview** > **Settlement currency,** click **Set up**, and then click + **Settlement currency** to add USD as a settlement currency.

![Image 10: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712475926023-d28b7f5a-c22a-4816-a2b7-82c3ceb01b4e.png)

> **Note**: To withdraw in USD, you must link a bank account associated with this currency. Each settlement currency can have its corresponding bank account linked.

2.  Click **Set up** again to enter the **Settlement currency management** page, click the ellipsis icon ![Image 11: image.png](https://yuque.antfin.com/images/lark/0/2024/png/119656509/1710837746654-4cd058eb-ebfe-47c9-ade1-3168464f8a01.png) on the line of USD and select **Add a bank account** to link a bank account.
3.  After your bank account is linked successfully, click the ellipsis icon ![Image 12: image.png](https://yuque.antfin.com/images/lark/0/2024/png/119656509/1710837746654-4cd058eb-ebfe-47c9-ade1-3168464f8a01.png) on the line of USD and select **Set as default settlement currency** to set USD as the default settlement currency.

![Image 13: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712476154917-8a06c01c-0f06-41c5-8044-2802ac6400fc.png)

> **Note**: If the settlement currency defined here differs from that specified in the **pay** API, Antom will default to the currency specified in the **pay** API as the settlement currency.

### Settlement contract

You can check your settlement period, your linked bank accounts and other related information in **Settlement overview** under **Finance**.

![Image 14: image.png](https://cdn.nlark.com/yuque/0/2024/png/12884741/1712476335776-93755db8-48eb-4a66-b97b-9e10daf5d110.png)

To view the latest updates to the documentation, visit [Release notes](https://global.alipay.com/docs/releasenotes).

![Image 15](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png)![Image 16](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 Alipay [Legal Information](https://global.alipay.com/docs/ac/platform/membership)

#### Is this page helpful?

#### On this page

[Register & log in](#lfKaa "Register & log in")

[Test in sandbox](#9cULp "Test in sandbox")

[Sandbox configuration](#kZRFb "Sandbox configuration")

[Generate keys](#D584U "Generate keys")

[Get integration resources](#Ozw86 "Get integration resources")

[Sandbox integration](#hnwDl "Sandbox integration")

[Sandbox testing](#3cKnh "Sandbox testing")

[Go live](#to4qC "Go live")

[View settlement info](#is5Ad "View settlement info")

[Balance info](#zbBre "Balance info")

[Settlement currency](#T8mgj "Settlement currency")

[Settlement contract](#kJMxL "Settlement contract")