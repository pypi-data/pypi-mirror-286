一条消息由头和正文组成。以下部分专注于正文结构。关于头部结构，请参阅：

*   [请求头](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [响应头](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**注意**：除数组外，每个字段的数据类型应设置为字符串。这意味着必须使用双引号（" "）包围字段值。例如：

*   如果字段的数据类型为Integer，其值为20，则设置为"20"。
*   如果字段的数据类型为Boolean，其值为true，则设置为"true"。

### 请求参数

显示全部

#### declarationRequestId 字符串  必需

商家为标识申报请求分配的唯一ID。每个申报请求号的长度范围为1到32位。

关于此字段的更多信息：

*   此字段是API幂等性字段。
*   最大长度：32个字符

#### paymentId 字符串  必需