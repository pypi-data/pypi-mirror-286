*   Specify this field when the buyer information needs to be verified. Actually, it is recommended to provide the buyer information in this API to meet the customs declaration policy requirements and facilitate Alipay to check the buyer information. Although this field is optional, it is suggested to specify this field because customs will check buyer information at random. 
*   If this field is not specified, the merchant needs to ensure that the buyer and payer information is consistent. Any inconsistency detected by customs will result in a rejected declaration. Specifying this field will reduce the risk of the order being returned. 

Show child parameters

### Response parameters

Show all

#### result Result object REQUIRED

The request result, which contains information such as status and error codes.

Note: This field does not indicate the declaration result. This field only indicates whether the **declare** API is called successfully.

Show child parameters