存储支付方式
==================  
2024年3月14日 08:39  
POST /v1/vaults/vaultPaymentMethod  

使用**vaultPaymentMethod** API在发起支付之前存储支付方式。从API响应中，您可以获取到*cardToken*或一个或多个*normalUrl*, *schemeUrl*, 或 *applinkUrl*。*cardToken*用于使用[**pay**](https://global.alipay.com/docs/ac/ams/payment_cashier) API发起支付，而URLs可用于重定向用户完成存储过程。

结构
=========

消息由头部和主体组成。以下部分专注于主体结构。头部结构请参考：
*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着字段值必须用双引号（" "）包围。例如：
*   如果字段的数据类型为Integer，值为20，则设置为"20"。
* 如果字段的数据类型为布尔值，并且其值为 `true`，则设置为 "真"。
### 请求参数  
#### vaultingRequestId 字符串  必需  
商家为识别卡存储请求分配的唯一ID。  
关于此字段的更多信息：  
*   此字段是API幂等字段。对于具有相同`vaultingRequestId`且最终状态为S或F的存储请求，应返回相同的结果。
*   最大长度：64个字符  
#### vaultingNotificationUrl 字符串  必需  
用于接收存储结果通知的URL。  
关于此字段的更多信息：  
*   最大长度：2048个字符  
#### redirectUrl 字符串  必需  
存储过程完成后，买家被重定向到的商家页面URL。  
关于此字段的更多信息：  
*   最大长度：2048个字符  
#### merchantRegion 字符串  
商家运营业务的国家或地区。此参数的值基于[ISO 3166国家代码](https://www.iso.org/obp/ui/#search)标准的2字母国家或地区代码。  
可能的值包括 `US`, `SG`, `HK`, `PK`, `JP`, `CN`, `BR`, `AU`, 和 `MY`。  
当使用全球收单网关（GAGW）产品时，需要指定此参数。  
关于此字段的更多信息：  
*   最大长度：2个字符  
#### paymentMethodDetail PaymentMethodDetail对象  必需  
需要存储的支付方式的详细信息。  
#### env Env对象  必需  
关于订单放置环境的信息，如设备信息。  
### 响应参数  
#### result 结果对象 **必需**  
API调用的结果。  
#### vaultingRequestId 字符串 **必需**  
商家为标识卡存储请求分配的唯一ID。  
关于此字段的更多信息  
*   最大长度：64个字符  
#### paymentMethodDetail 支付方式详情对象  
需要存储的支付方式的详细信息。  
当*result.resultStatus*的值为`S`时，此参数返回。  
#### normalUrl 字符串  
将用户重定向到默认浏览器或嵌入式WebView中的WAP或WEB页面的URL。  
当*result.resultCode*的值为`VERIFICATION_IN_PROCESS`时，可能会返回以下一个或多个URL：*schemeUrl*、*appLinkUrl*和*normalUrl*。  
当*paymentMethodType*的值为`CARD`时，用户需要通过此URL访问的页面完成3DS验证。  
关于此字段的更多信息  
*   最大长度：2048个字符  
#### schemeUrl 字符串  
当目标应用已安装时，将用户重定向到Android或iOS系统中打开应用的URL方案。  
关于此字段的更多信息  
*   最大长度：2048个字符  
#### applinkUrl 字符串  
当目标应用已安装时，将用户重定向到打开应用的URL，或者当目标应用未安装时，打开WAP页面。  
关于此字段的更多信息  
*   最大长度：2048个字符  
API探索器  
示例代码在沙箱中运行
### 请求  
URL  
北美地区  
https://open-na-global.alipay.com/ams/api/v1/vaults/vaultPaymentMethod  

请求体  
```json
{
  "vaultingRequestId": "123456789206",
  "vaultingNotificationUrl": "www.test.com",
  "redirectUrl": "www.test.com",
  "paymentMethodDetail": {
    "paymentMethodType": "CARD",
    "card": {
      "cardNo": "4112273146798764",
      "brand": "VISA",
      "cardholderName": {
        "firstName": "xu",
        "middleName": "fang",
        "lastName": "jie",
        "fullName": "xufangjie"
      },
      "billingAddress": {
        "region": "CN",
        "address1": "gongzhuan Road",
        "city": "hangzhou",
        "state": "zhejiang",
        "zipCode": "310000"
      },
      "cvv": "123",
      "expiryYear": "26",
      "expiryMonth": "08",
      "businessRegistrationNo": "96"
    }
  },
  "env": {
    "terminalType": "app"
  }
}
```
### 响应  
响应体  
```json
{
  "paymentMethodDetail": {
    "card": {
      "brand": "VISA",
      "cardToken": "ALIPAY9CGwsAeMBug+G2dSKDV6AIsNKTxAFNkOMoj8Gxvt8h0eDUbd6nO5CwMFIjEFERWxCAo/b1OjVTvtl1zspyMGcg==",
      "maskedCardNo": "************8764"
    },
    "paymentMethodType": "CARD"
  },
  "vaultingRequestId": "123487889889",
  "result": {
    "resultCode": "SUCCESS",
    "resultMessage": "success.",
    "resultStatus": "S"
  }
}
```

结果处理逻辑
--------------------
对于不同的请求结果，需要执行不同的操作。可能的*result.resultStatus*响应值如下：

*   `S`: 表示API调用成功。从该API的响应中获取*cardToken*。然后在启动支付时，在支付API中使用*cardToken*的值
*   `F`: 表示API调用失败。要了解失败的具体原因，请查看*result.resultCode*。
*   `U`: 当返回此值时，根据*resultCode*的值是否为`VERIFICATION_IN_PROCESS`采取相应行动：
    *   结果代码不是`VERIFICATION_IN_PROCESS`：API调用失败。使用新的*vaultingRequestId*值再次调用此API。
    *   结果代码是`VERIFICATION_IN_PROCESS`：检查是否返回了三个URL（*appLinkUrl*，*normalUrl*，*schemeUrl*）中的一个或多个：
        *   返回了一个或多个URL：保管箱创建成功。将用户重定向到提供的特定URL以完成保管箱设置。
        *   没有返回URL：保管箱创建失败。使用新的_vaultingRequestId_值再次调用此API。如果问题持续存在，请联系支付宝技术支持。
### 结果/错误代码  
| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 | 保险箱会话创建成功。无需进一步操作。 |
| PARAM\_ILLEGAL | F | 必需参数未传递，或存在非法参数。例如，非数字输入，无效日期，或参数长度和类型错误。 | 检查并确认当前API的必需请求字段（包括头部字段和正文字段）是否正确传递并有效。 |
| PROCESS\_FAIL | F | 发生了一般业务失败。 | 不要重试。通常需要人工干预。建议联系支付宝技术支持解决问题。 |
| UNKNOWN\_EXCEPTION | U | 由于未知原因，API调用失败。 | 重新调用接口以解决问题。如果未解决，联系支付宝技术支持。 |
| VERIFICATION\_IN\_PROCESS | U | 支付方式信息的验证正在进行中。 | 获取任何URL（*appLinkUrl*, *normalUrl*, *schemeUrl*）并打开URL。如果没有返回URL，使用新的请求ID再次调用此API。如果问题持续，联系支付宝技术支持。 |
| VERIFICATION\_FAIL | F | 支付方式信息验证失败。 | 使用新的请求ID再次调用此API。 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。  
