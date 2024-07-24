注意: 当满足以下两个条件时，此字段会被返回:

1.  _resultCode_ 为 `S`。
2. 收到海关收据。

关于此字段的更多信息:

* 最大长度: 32 个字符

API 探索器

示例代码（在沙箱中运行）

### 请求

URL

北美地区

```text
https://open-na-global.alipay.com/ams/api/v1/customs/declare
```

请求体

```json
{
  "declarationAmount": {
    "currency": "CNY",
    "value": "100"
  },
  "merchantCustomsInfo": {
    "merchantCustomsName": "amsdemo",
    "merchantCustomsCode": "amsdemoskr"
  },
  "paymentId": "20211117194010800100188180203227785",
  "splitOrder": false,
  "customs": {
    "region": "CN",
    "customsCode": "ZONGSHU"
  },
  "declarationRequestId": "req123",
  "buyerCertificate": {
    "holderName": {
      "firstName": "f",
      "lastName": "l",
      "fullName": "cangxi.lj",
      "middleName": "m"
    },
    "certificateNo": "510502199504139527",
    "certificateType": "ID_CARD"
  }
}
```

请确保翻译后的文本通顺且保留了原始markdown格式。