*   The [signature](https://global.alipay.com/docs/ac/ams/api_fund) field in a request header 
*   How to [calculate a signature](https://global.alipay.com/docs/ac/ams/digital_signature) 



 |
| KEY\_NOT\_FOUND | F | The private key or public key of Alipay or the merchant is not found. | 

Check whether the private key or public key exists. If not, upload the private key in Antom Dashboard.



 |
| MEDIA\_TYPE\_NOT\_ACCEPTABLE | F | The server does not implement the media type that is acceptable to the client. | Check whether the media type is correct and use a media type that is accepted by Alipay.

 |
| MERCHANT\_NOT\_REGISTERED | F | The merchant is not registered. | Please register the merchant by using the registration interface. Contact Alipay Technical Support if failed to call the registration interface.

 |
| METHOD\_NOT\_SUPPORTED | F | The server does not implement the requested HTTP method. Only the POST method is supported. | Ensure the HTTP method is POST.