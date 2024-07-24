查询存档
=============== 

2023-12-26 08:34

POST /v1/vaults/inquireVaulting  

使用**查询存档** API 来查询支付方式的存档状态。  

结构
=========  
消息由头部和主体组成。以下部分专注于主体结构。头部结构请参阅：
*   [请求头部](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头部](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)  

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着必须使用双引号（" "）包围字段值。示例：
*   如果字段的数据类型为整数，值为20，设置为"20"。
*   如果字段的数据类型为布尔值，值为`true`，设置为"true"。
### 请求参数  
#### vaultingRequestId 字符串  必需  
由商家分配的唯一ID，用于标识一次卡存储请求。  
关于此字段的更多信息：  
*   此字段是一个API幂等性字段。对于使用相同`vaultingRequestId`值发起并达到最终状态`S`或`F`的卡存储请求，应返回相同的结果。  
关于此字段的更多信息：  
*   最大长度：64个字符
### 响应参数  
显示全部  
#### result 结果对象 **必需**  
请求调用结果的信息。  
此字段不表示存卡结果，仅表示接口调用是否成功。  
显示子参数  
#### vaultingRequestId 字符串 **必需**  
商家为识别一个卡存档请求而分配的唯一ID。  
关于此字段的更多信息：  
*   最大长度：64 个字符  
#### normalUrl URL  
在默认浏览器或嵌入式WebView中重定向用户到WAP或WEB页面的URL。  
当 *result.resultStatus* 的值为 `S` 且 *vaultingStatus* 的值为 `PROCESSING` 时，可能会返回以下一个或多个URL：*schemeUrl*、*applinkUrl* 和 *normalUrl*。  
当 *paymentMethodType* 的值为 `CARD` 时，用户需要通过此URL访问的页面完成3DS验证。  
关于此字段的更多信息：  
*   最大长度：2048 个字符  
#### schemeUrl URL  
在Android或iOS系统中重定向用户打开已安装目标应用的URL方案。  
当 *result.resultStatus* 的值为 `S` 且 *vaultingStatus* 的值为 `PROCESSING` 时，可能会返回以下一个或多个URL：*schemeUrl*、*applinkUrl* 和 *normalUrl*。  
关于此字段的更多信息：  
*   最大长度：2048 个字符  
#### applinkUrl URL  
当目标应用已安装时重定向用户打开应用，或者当目标应用未安装时打开WAP页面的URL。对于Android，URL是原生应用链接。对于iOS，URL是通用链接。  
当 *result.resultStatus* 的值为 `S` 且 *vaultingStatus* 的值为 `PROCESSING` 时，可能会返回以下一个或多个URL：*schemeUrl*、*applinkUrl* 和 *normalUrl*。  
关于此字段的更多信息：  
*   最大长度：2048 个字符  
#### paymentMethodDetail 支付方式详情对象
关于需要存储的支付方式的详细信息。  
当*vaultingStatus*的值为`SUCCESS`时，此参数会被返回。  
显示子参数  
#### vaultingStatus 字符串  
表示支付方式的存储状态。有效值包括：  
*   `SUCCESS`：表示存储成功。
*   `FAIL`：表示存储失败。
*   `PROCESSING`：表示存储处理中。  
当*result.resultStatus*的值为`S`时，此参数会被返回。  
关于此字段的更多信息  
*   最大长度：10个字符 

API 探索器  
示例代码在沙箱中运行
### 请求  
URL  
北美地区  
https://open-na-global.alipay.com/ams/api/v1/vaults/inquireVaulting  
请求体  
```json
{
  "vaultingRequestId": "123456789206"
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
  "vaultingStatus": "SUCCESS",
  "result": {
    "resultCode": "SUCCESS",
    "resultMessage": "success.",
    "resultStatus": "S"
  }
}
```
结果处理逻辑 
---------------------

对于不同的请求结果，需要采取不同的行动。*result.resultStatus* 的可能响应包括：  
* `S`：表示 API 调用成功。您可以从 API 响应中的 *vaultingStatus* 获取存储卡信息的结果。
* `F`：表示 API 调用失败。有关失败原因的更多信息，请参阅 *result.resultCode*。
* `U`: 表示API调用由于未知原因失败。请使用相同的请求ID重试。
### 结果/错误代码  
| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功 |  |
| VAULTING\_NOT\_EXIST | F | 保险箱请求ID不存在。 | 检查*vaultingRequestId*的值是否正确。如果正确，请联系支付宝技术支持以获取具体原因。 |
| UNKNOWN\_EXCEPTION | U | 由于未知原因，API调用失败。 | 重新调用接口以解决问题。如果问题未解决，请联系支付宝技术支持。  

