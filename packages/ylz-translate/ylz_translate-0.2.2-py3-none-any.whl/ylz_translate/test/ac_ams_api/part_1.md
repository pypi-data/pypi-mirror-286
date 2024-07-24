A message consists of a header and body. The following sections are focused on the body structure. For the header structure, see：

*   [Request header](https://global.alipay.com/docs/ac/ams/api_fund#ML5ur)
*   [Response header](https://global.alipay.com/docs/ac/ams/api_fund#WWH90)

**Note**: Set the data type of each field (except array) as String. This means that you must use double quotation marks (" ") to enclose the field value. Examples:

*   If the data type of a field is Integer and its value is 20, set it as "20".
*   If the data type of a field is Boolean and its value is true, set it as "true".  

### Request parameters

Show all

#### declarationRequestId String  REQUIRED

The unique ID that is assigned by the merchant to identify a declaration request. The length of each declaration request number ranges from 1 to 32 bits.

More information about this field

*   This field is an API idempotency field.
*   Maximum length: 32 characters

#### paymentId String  REQUIRED