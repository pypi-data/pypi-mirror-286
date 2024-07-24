接受争议
==================  
2024-02-23 07:18  
POST /v1/payments/acceptDispute  
使用**acceptDispute** API 接受特定的争议。

结构
==========

消息由头和正文组成。以下部分专注于正文结构。头结构请参考：
*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着必须使用双引号（" "）包围字段值。例如：
*   如果字段的数据类型为Integer，其值为20，应设置为"20"。
*   如果字段的数据类型为Boolean，其值为true，应设置为"true"。
### 请求参数  
#### 争议ID (disputeId) - 字符串 - 必填  
支付宝为识别一个争议分配的唯一标识。  
关于此字段的更多信息：  
*   最大长度：64 个字符
### 响应参数  
显示全部  
#### result 结果对象 object 必填  
API调用的结果。  
显示子参数  
#### disputeId 争议ID 字符串  
支付宝为识别一次争议分配的唯一ID。  
当resultCode的值为`SUCCESS`时，此参数返回。  
关于此字段的更多信息  
*   最大长度：64个字符  
#### disputeResolutionTime 解决争议时间 字符串  
您接受争议的时间。  
当resultCode的值为`SUCCESS`时，此参数返回。  
关于此字段的更多信息  
*   最大长度：64个字符  
API探索器  
示例代码 在沙箱中运行
### 请求  
URL  
北美地区  
https://open-na-global.alipay.com/ams/api/v1/payments/acceptDispute  

请求体  
```json
{
  "disputeId": "202401012501310115730104****"
}
```

### 响应  
响应体  
```json
{
  "result": {
    "resultCode": "SUCCESS",
    "resultStatus": "S",
    "resultMessage": "success"
  },
  "disputeId": "2024010121013101637705928564",
  "disputeResolutionTime": "2024-01-01T18:25:00+00:00"
}
```

### 结果/错误代码  
| 代码 | 值 | 消息 | 进一步操作 |
| --- | --- | --- | --- |
| SUCCESS | S | 成功。 |  |
| PARAM\_ILLEGAL | F | 参数非法。例如，非数字输入，无效日期。 | 检查并验证当前API所需的请求字段（包括头部字段和正文字段）是否正确传递并有效。 |
| REPEAT\_REQUEST | F | 重复请求。 | 联系支付宝技术支持以检查争议状态。 |
| TIME\_EXCEEDS\_LIMIT | F | 您的防御已过期，无法接受或辩护争议。 |  |
| UNKNOWN\_EXCEPTION | U | 由于未知原因，API调用失败。 | 再次调用接口以解决问题。如果未解决，联系支付宝技术支持。 |

要查看文档的最新更新，请访问 [发行说明](https://global.alipay.com/docs/releasenotes)。  
