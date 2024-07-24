签署请求和验证签名 | 产品API | 支付宝文档
==================

[![图片1：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_a52690f40beef33d7d37f1bda6f48c27.svg)![图片2：中国领先的第三方在线支付解决方案 - 支付宝](./img_m_d70d46fd32b98952674df01c03131d87.svg)](/docs/)

[登录](https://global.alipay.com/ilogin/account_login.htm?goto=https%3A%2F%2Fglobal.alipay.com%2Fdocs%2Fac%2Fams%2Fdigital_signature%3FpageVersion%3D34)

[返回首页](../../)

产品API

[支付宝API](/docs/ac/ams/api)

[概述](/docs/ac/ams/api_fund)

[幂等性](/docs/ac/ams/idempotency)

[消息编码](/docs/ac/ams/me)

[使用SDK签署请求和验证签名](/docs/ac/ams/signature_sdk)

[签署请求和验证签名](/docs/ac/ams/digital_signature?pageVersion=34)

[API变更历史](/docs/ac/ams/changehistory)

在线支付

店内支付

签署请求和验证签名
======================

2024年05月24日 10:06

在开始之前，请查阅[API基础文档](https://global.alipay.com/docs/ac/ams/api_fund#tLLkc)，以了解蚂蚁消息结构的基本知识。

为了确保数据传输后的真实性和完整性，蚂蚁金服要求所有请求都必须签名，并验证签名：

*   调用API时，您必须对发送给蚂蚁金服的请求进行签名，并相应地验证蚂蚁金服响应的签名。详情请参阅[调用API](#wPgXI)。
*   接收到通知时，您必须验证蚂蚁金服请求的签名。但是，您不需要对通知的响应进行签名。详情请参阅[接收通知](#WMRu5)。

调用API
========

前提条件
------------

确保您已经在[蚂蚁开放平台控制台](https://dashboard.alipay.com/global-payments/developers/quickStart)上生成了一对非对称的公钥和私钥。更多详情，请参阅[生成密钥](https://global.alipay.com/docs/dashboard_en#D584U)。

### 签名请求

以下是如何签名请求的示例：

![图片 3: image.png](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1664440939174-81dee3b9-1fe5-426c-ae5f-1ef47e716c00.png)

**图 1. 如何签名请求**

### 步骤 1：构建待签名内容

`content_to_be_signed` 的语法如下：

```plaintext
<HTTP方法> <HTTP路径>
<客户端ID>.<请求时间>.<请求正文>
```

> **注意**：在 `<HTTP方法>` 和 `<HTTP路径>` 之间应有一个空格字符。

*   `http-method`: [HTTP请求方法](https://global.alipay.com/docs/ac/ams/api_fund#dMgcH)。始终为`POST`。
*   `http-uri`: 包括[资源路径](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL#path_to_resource)和[参数](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL#parameters)（如果有）。例如，如果HTTP URL是[https://open-na-global.alipay.com/ams/api/v1/payments/pay](https://open-na-global.alipay.com/ams/api/v1/payments/pay)，此字段为`/ams/api/v1/payments/pay`。
*   `client-id`: 此参数在[请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)中是必需的，用于识别客户端。一个示例值是`SANDBOX_5X00000000000000`。

*   `request-time`: 此参数在[请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)中是必需的，它指定了请求发送的时间戳。该字段的值必须精确到毫秒。一个示例值是`1685599933871`。
*   `request-body`: [HTTP 请求体](https://global.alipay.com/docs/ac/ams/api_fund#oNtxc)。请参考以下示例代码：

以下是Markdown格式文档的中文翻译：

```
### 步骤1：构建请求体

请求体按照`content_to_be_signed`的语法构建如下：

```
POST /ams/api/v1/payments/pay
SANDBOX_5X00000000000000.1685599933871.{
    "env": {
        "terminalType": "WEB"
    },
    "order": {
        "orderAmount": {
            "currency": "CNY",
            "value": "100"
        },
        "orderDescription": "测试订单",
        "referenceOrderId": "ORDER_ID_1685599933871"
    },
    "paymentAmount": {
        "currency": "CNY",
        "value": "100"
    },
    "paymentMethod": {
        "paymentMethodType": "ALIPAY_CN"
    },
    "paymentRedirectUrl": "https://www.example.com",
    "paymentRequestId": "REQUEST_ID_1685599933871",
    "productCode": "CASHIER_PAYMENT"
}
```

### 步骤2：生成签名

生成签名的语法如下：

```
generated_signature=urlEncode(base64Encode(sha256withRSA(<content_to_be_signed>, <privateKey>)))
```

*   `generated_signature`: 生成的签名字符串。
*   `urlEncode`: 对base64编码的数字签名进行编码的方法。
*   `base64Encode`: 对生成的数字签名进行编码的方法。
*   `sha256withrsa`: 用于对提供的内容生成数字签名的方法。
*   `content_to_be_signed`: 从[步骤1](#Adgbs)获取的内容。
*   `privateKey`: 从[前提条件](#ebihb)获取的私钥值。

生成签名的示例如下：

```
SVCvBbh5Eviwaj13ouTDy%2FAqFcNDNLXtoIgxFurTgnYjfBJ6h7jl4GKr%2Bkw8easQv9EHK7CXT9QZOMrkYNOUuqRs%2FDtT4vROCiRcnqNOKVjU3zHt%2Br%2Fxal%2FYRV4dc%2FNtu1ppyWJ6a2xNFCa63Y2YKNn%2FW%2B9eABmU2oohVXwBNoCnaLDoTIJV2RKb3E%2FiUp0aIWUz0Ntv4kVR8ZqMe6DUmf7pHRq9hm2av4wwBpJbHC%2B6R%2BMBQPv%2F0ZUFBW02ie%2FTpXBrPasb15s%2FjcmRpAnmED%2FFIec4TGzDIHr%2BO3QFtIRu72vg4zHWC3FuL4i8zfMXWNi3kp7hBFUIBpYroTZH5Q%3D%3D
```

以下代码示例展示了如何使用Java对请求进行签名：

```
```

请注意，代码示例部分未翻译，因为它们通常包含特定的编程语言语法，这些语法在翻译时可能会失去其原始含义。如果您需要帮助理解代码，请提供更具体的问题。

```java
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.PrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;

public class 签名示例代码 {

    /**
     * 您的私钥，用于签名
     * 请确保私钥的安全存储，防止泄露
     */
    private static final String CLIENT_PRIVATE_KEY = "";

    /**
     * 您的client_id
     */
    private static final String CLIENT_ID = "";

    /**
     * @param requestURI  域名部分不包括，示例：/ams/api/v1/payments/pay
     * @param clientId    您的client_id，示例：SANDBOX_5X00000000000000
     * @param requestTime 时间戳（毫秒），示例：1685599933871
     * @param privateKey  您的私钥
     * @param requestBody 请求体
     * @return
     */
    public static String sign(String requestURI, String clientId, String requestTime, String privateKey, String requestBody) {

        // 需要签名的内容
        String contentToBeSigned = String.format("POST %s\n%s.%s.%s", requestURI, clientId, requestTime, requestBody);

        try {
            // 使用SHA256withRSA算法
            java.security.Signature signature = java.security.Signature.getInstance("SHA256withRSA");

            // 私钥
            PrivateKey priKey = KeyFactory.getInstance("RSA").generatePrivate(
                    new PKCS8EncodedKeySpec(Base64.getDecoder().decode(privateKey.getBytes(StandardCharsets.UTF_8))));

            signature.initSign(priKey);
            signature.update(contentToBeSigned.getBytes(StandardCharsets.UTF_8));

            // 签名
            byte[] signed = signature.sign();

            // Base64编码
            String base64EncodedSignature = new String(Base64.getEncoder().encode(signed), StandardCharsets.UTF_8);

            // URL编码
            return URLEncoder.encode(base64EncodedSignature, StandardCharsets.UTF_8.displayName());
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        System.out.println(sign("/ams/api/v1/payments/pay", CLIENT_ID, "1685599933871", CLIENT_PRIVATE_KEY, "{\n" +
                "    \"env\": {\n" +
                "        \"terminalType\": \"WEB\"\n" +
                "    },\n" +
                "    \"order\": {\n" +
                "        \"orderAmount\": {\n" +
                "            \"currency\": \"CNY\",\n" +
                "            \"value\": \"100\"\n" +
                "        },\n" +
                "        \"orderDescription\": \"Testing order\",\n" +
                "        \"referenceOrderId\": \"ORDER_ID_1685599933871\"\n" +
                "    },\n" +
                "    \"paymentAmount\": {\n" +
                "        \"currency\": \"CNY\",\n" +
                "        \"value\": \"100\"\n" +
                "    },\n" +
                "    \"paymentMethod\": {\n" +
                "        \"paymentMethodType\": \"ALIPAY_CN\"\n" +
                "    },\n" +
                "    \"paymentRedirectUrl\": \"https://www.example.com\",\n" +
                "    \"paymentRequestId\": \"REQUEST_ID_1685599933871\",\n" +
                "    \"productCode\": \"CASHIER_PAYMENT\"\n" +
                "}"));
    }

}
```

### 步骤3：将生成的签名添加到请求头

1. 根据以下语法组装签名字符串：

```
'Signature: algorithm=<算法>, keyVersion=<密钥版本>, signature=<生成的签名>'
```

*   `algorithm`, `keyVersion`: 见[消息结构](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)章节的头部。
*   `生成的签名`: 在[步骤2](#gNWs0)中生成的签名。

例如：

```
'Signature: algorithm=RSA256, keyVersion=1, signature=SVCvBbh5Eviwaj13ouTDy%2FAqFcNDNLXtoIgxFurTgnYjfBJ6h7jl4GKr%2Bkw8easQv9EHK7CXT9QZOMrkYNOUuqRs%2FDtT4vROCiRcnqNOKVjU3zHt%2Br%2Fxal%2FYRV4dc%2FNtu1ppyWJ6a2xNFCa63Y2YKNn%2FW%2B9eABmU2oohVXwBNoCnaLDoTIJV2RKb3E%2FiUp0aIWUz0Ntv4kVR8ZqMe6DUmf7pHRq9hm2av4wwBpJbHC%2B6R%2BMBQPv%2F0ZUFBW02ie%2FTpXBrPasb15s%2FjcmRpAnmED%2FFIec4TGzDIHr%2BO3QFtIRu72vg4zHWC3FuL4i8zfMXWNi3kp7hBFUIBpYroTZH5Q%3D%3D'
```

2. 将签名字符串添加到请求头。有关请求头的详细信息，请参阅[消息结构](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)章节。

发送请求
----------

构建请求
----------------

通过在请求头中添加`Client-Id`、`Request-Time`和`Signature`属性来构建请求。构建好请求后，可以使用通用工具，如cURL或Postman来发送请求。以下示例使用了cURL：

```shell
curl -X POST \
  https://open-na-global.alipay.com/ams/api/v1/payments/pay \
  -H 'Content-Type: application/json' \
  -H 'Client-Id: SANDBOX_5X00000000000000' \
  -H 'Request-Time: 1685599933871' \
  -H 'Signature: algorithm=RSA256, keyVersion=1, signature=SVCvBbh5Eviwaj13ouTDy%2FAqFcNDNLXtoIgxFurTgnYjfBJ6h7jl4GKr%2Bkw8easQv9EHK7CXT9QZOMrkYNOUuqRs%2FDtT4vROCiRcnqNOKVjU3zHt%2Br%2Fxal%2FYRV4dc%2FNtu1ppyWJ6a2xNFCa63Y2YKNn%2FW%2B9eABmU2oohVXwBNoCnaLDoTIJV2RKb3E%2FiUp0aIWUz0Ntv4kVR8ZqMe6DUmf7pHRq9hm2av4wwBpJbHC%2B6R%2BMBQPv%2F0ZUFBW02ie%2FTpXBrPasb15s%2FjcmRpAnmED%2FFIec4TGzDIHr%2BO3QFtIRu72vg4zHWC3FuL4i8zfMXWNi3kp7hBFUIBpYroTZH5Q%3D%3D' \
  -d '{
    "env": {
        "terminalType": "WEB"
    },
    "order": {
        "orderAmount": {
            "currency": "CNY",
            "value": "100"
        },
        "orderDescription": "Testing order",
        "referenceOrderId": "ORDER_ID_1685599933871"
    },
    "paymentAmount": {
        "currency": "CNY",
        "value": "100"
    },
    "paymentMethod": {
        "paymentMethodType": "ALIPAY_CN"
    },
    "paymentRedirectUrl": "https://www.example.com",
    "paymentRequestId": "REQUEST_ID_1685599933871",
    "productCode": "CASHIER_PAYMENT"
}'
```

处理响应
-----------------

从Antom收到响应后，验证响应的签名。下图展示了如何验证签名：

![](https://idocs-assets.marmot-cloud.com/storage/idocs87c36dc8dac653c1/1664441017739-e31cc973-7ae2-4028-b819-d90c8df65bd8.png)

图2. 验证签名的流程

响应由响应头和响应体组成。例如：

*   响应头的代码示例：

```shell
Client-Id: SANDBOX_5X00000000000000
Response-Time: 2019-05-28T12:12:14+08:00
algorithm=RSA256,keyVersion=1,signature=d1jdwMNkno7eOFqbsmCl2lfnmAUlK40VyHi3%2FlIrto%2FdV%2F1Ds730bfNJc9YrqNzjfb3ly66bhF0vlxgaPPwYqsWmc3FSXqSQGdSZ42VOzoZXBA2sjI0e%2F8e7IIa%2FGlrzbpNwrOiMuJxaUw6lIK7vxxyvr8vxpfQ0Pml0mKnQO2NP4yY%2BvMMJCdvmM3Bl7mNYL%2BVCLDMNespD763EY252vqMU8fbC9CUf2zCckN78TaWOuK%2FOiMlVYN8VUYIKeoyutiNUv%2B0vIiqfq7IcXCS0pom33MltFukhiyHIso3B%2FD1KN9fi0B9eJbXPB5ox%2FLsChGS48rQECRiqo2mC%2FHXzyQ%3D%3D
```

*   响应体的代码示例：

（响应体的示例代码未提供，通常会包含JSON格式的支付结果或其他相关信息）

```markdown
# 处理Antom响应的步骤

### 步骤1：获取Antom公钥

通过[Antom仪表板](https://global.alipay.com/docs/dashboard_en) > **开发者** > **快速入门** > **集成资源和工具** > **集成资源** 获取Antom公钥。

> **注意：** 只有当你在Antom仪表板上上传你的非对称公钥时，你才能获取用于验证Antom相应响应的Antom公钥。

### 步骤2：构造验证内容

`content_to_be_validated` 的构造语法如下：

```

请注意，原始文档中的JSON对象已经转换为中文描述，保留了原始的markdown格式。没有提供具体的`content_to_be_validated`的构造语法，因此这部分留空。如果有具体的JSON数据需要翻译，可以提供详细内容。

`<HTTP方法> <HTTPURI>`
`<客户端ID>.<响应时间>.<响应正文>`

*   `http-method`: [HTTP请求方法](https://global.alipay.com/docs/ac/ams/api_fund#dMgcH)。始终为`POST`。
*   `http-uri`: 包括[资源路径](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL#path_to_resource)和[参数](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL#parameters)（如果有）。例如，如果HTTP URL是[https://open-na-global.alipay.com/ams/api/v1/payments/pay](https://open-na-global.alipay.com/ams/api/v1/payments/pay)，此字段为`/ams/api/v1/payments/pay`。
*   `client-id`: 此参数在[响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)中返回，用于标识客户端。一个示例值是`SANDBOX_5X00000000000000`。

*   `响应时间`: 此参数在[响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)中返回，指明响应返回的时间。该参数的格式遵循[ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)标准。一个示例值是`2019-05-28T12:12:14+08:00`。
*   `响应体`: [HTTP响应体](https://global.alipay.com/docs/ac/ams/api_fund#eNUbf)。

遵循`content_to_be_validated`的语法规则，构建如上所示的响应：

```markdown
POST /ams/api/v1/payments/pay
SANDBOX_5X00000000000000.2019-05-28T12:12:14+08:00.{
 "result": {
    "resultCode":"SUCCESS",
    "resultStatus":"S",
    "resultMessage":"success"
   }
}
```

### 步骤3：从响应头获取签名

目标签名字符串（`target_signature`）可以从响应头的`Signature`字段中提取。有关响应头的详细信息，请参阅[消息结构](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)。

`Signature`的代码示例：`Signature: algorithm=RSA256,keyVersion=1,signature=<target_signature>`

### 步骤4：验证签名

验证签名的语法如下：

```markdown
is_signature_validate=sha256withRSA_verify(base64Decode(urlDecode(<target_signature>), <content_to_be_validated>, <serverPublicKey>)
```

*   `is_signature_validate`：一个布尔值，表示签名是否有效。

*   真: 签名有效。
*   假: 签名无效。可能的原因是私钥和公钥不匹配，或者`content_to_be_validated`构建不正确。

*   `sha256withRSA_verify`: 验证签名的方法。
*   `base64Decode`: 解码数字签名的方法。
*   `urlDecode`: 解码已base64解码的数字签名的方法。
*   `target_signature`: 从[步骤3](https://global.alipay.com/docs/ac/ams/digital_signature#FJhqP)获取的目标签名。
*   `content_to_be_validated`: 需要验证的内容，从[步骤2](https://global.alipay.com/docs/ac/ams/digital_signature#hvhQp)创建。
*   `serverPublicKey`: 从[步骤1](https://global.alipay.com/docs/ac/ams/digital_signature#eK2mk)获取的蚂蚁金服公钥。

以下示例代码展示了如何使用Java进行签名验证：

```java
// 假设已经有了以上方法的实现
public boolean verifySignature(String target_signature, String content_to_be_validated, String serverPublicKey) {
    byte[] decodedSignature = base64Decode(target_signature);
    byte[] decodedContent = urlDecode(content_to_be_validated);
    
    // 使用服务器公钥进行签名验证
    boolean isValid = sha256withRSA_verify(decodedContent, decodedSignature, serverPublicKey);
    
    return isValid;
}
```

请确保导入了正确的库并实现了上述方法。

```java
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

import org.apache.commons.lang3.StringUtils;

public class 签名示例代码 {

    /**
     * 支付宝公钥，用于验证签名
     */
    private static final String SERVER_PUBLIC_KEY = "";

    /**
     * 您的客户端ID
     */
    private static final String CLIENT_ID = "";

    /**
     * @param requestURI      域名部分不包括，示例：/ams/api/v1/payments/pay
     * @param clientId        您的客户端ID，示例：SANDBOX_5X00000000000000
     * @param responseTime    ISO 8601 格式的时间，示例：2019-05-28T12:12:14+08:00
     * @param alipayPublicKey 支付宝公钥
     * @param responseBody    响应正文
     * @param targetSignature 待验证的签名
     * @return
     */
    public static boolean verify(String requestURI, String clientId, String responseTime, String alipayPublicKey, String responseBody, String targetSignature) {

        // 当 AMS 返回 SIGNATURE_INVALID 时，targetSignature 在响应中不会出现
        if (StringUtils.isBlank(targetSignature)) {
            return false;
        }

        // 需要验证的内容
        String contentToBeValidated = String.format("POST %s\n%s.%s.%s", requestURI, clientId, responseTime, responseBody);

        try {
            // 使用 SHA256withRSA 算法
            java.security.Signature signature = java.security.Signature.getInstance("SHA256withRSA");

            // 支付宝公钥
            PublicKey pubKey = KeyFactory.getInstance("RSA").generatePublic(
                    new X509EncodedKeySpec(Base64.getDecoder().decode(alipayPublicKey.getBytes(StandardCharsets.UTF_8))));

            signature.initVerify(pubKey);
            signature.update(contentToBeValidated.getBytes(StandardCharsets.UTF_8));

            // URL解码
            String urlDecodedSignature = URLDecoder.decode(targetSignature, StandardCharsets.UTF_8.displayName());

            // Base64解码
            byte[] signatureToBeVerified = Base64.getDecoder().decode(urlDecodedSignature);

            // 验证签名
            return signature.verify(signatureToBeVerified);

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static void main(String[] args) {
        // ...
    }
}
```

请注意，代码中的 `SERVER_PUBLIC_KEY` 和 `CLIENT_ID` 需要替换为实际的值。

系统.out.println(验证("/ams/api/v1/payments/pay", 客户端ID, "2019-05-28T12:12:14+08:00", 服务器公钥, "{\"result\":{\"resultStatus\":\"S\",\"resultCode\":\"SUCCESS\",\"resultMessage\":\"success.\"}}", "d1jdwMNkno7eOFqbsmCl2lfnmAUlK40VyHi3%2FlIrto%2FdV%2F1Ds730bfNJc9YrqNzjfb3ly66bhF0vlxgaPPwYqsWmc3FSXqSQGdSZ42VOzoZXBA2sjI0e%2F8e7IIa%2FGlrzbpNwrOiMuJxaUw6lIK7vxxyvr8vxpfQ0Pml0mKnQO2NP4yY%2BvMMJCdvmM3Bl7mNYL%2BVCLDMNespD763EY252vqMU8fbC9CUf2zCckN78TaWOuK%2FOiMlVYN8VUYIKeoyutiNUv%2B0vIiqfq7IcXCS0pom33MltFukhiyHIso3B%2FD1KN9fi0B9eJbXPB5ox%2FLsChGS48rQECRiqo2mC%2FHXzyQ%3D%3D"));
    }

接收通知
==========

请注意，这里的代码是一个Java方法，用于验证某个请求。在实际的文档中，这通常会是一个API调用的示例，用于验证支付或其他金融交易的通知。在Markdown格式中，这个代码段被保留原样，不进行翻译，因为它是编程代码，而不是文本内容。

处理请求
------------

在收到蚂蚁金服的通知后，需要验证请求的签名。验证请求签名的过程与[处理响应](#J8HGf)部分介绍的类似。要验证签名，请按照以下步骤操作：

1. 获取用于验证签名的蚂蚁金服公钥。
2. 按照`content_to_be_validated`的语法构建要验证的请求：

    `<http方法> <http-uri>
    <client-id>.<响应时间>.<响应正文>`

3. 从请求头中获取签名。
4. 验证签名。

要查看文档的最新更新，请访问[发行说明](https://global.alipay.com/docs/releasenotes)。

![图片 5](https://ac.alipay.com/storage/2021/5/20/19b2c126-9442-4f16-8f20-e539b1db482a.png) ![图片 6](https://ac.alipay.com/storage/2021/5/20/e9f3f154-dbf0-455f-89f0-b3d4e0c14481.png)

@2024 蚂蚁金服 [法律信息](https://global.alipay.com/docs/ac/platform/membership)

#### 这个页面是否有帮助？

#### 在本页

调用API

先决条件

签名请求

步骤1：构建待签名内容

步骤2：生成签名

步骤3：将生成的签名添加到请求头

发送请求

处理响应

步骤1：获取Antom公钥

步骤2：构建待验证内容

步骤3：从响应头获取签名

步骤4：验证签名

接收通知

处理请求