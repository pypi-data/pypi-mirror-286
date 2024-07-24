*   _declarationRequestId_ must be the same as the original request, otherwise, it will be considered as a new request.
*   Only _merchantCustomsCode_, _merchantCustomsName_, _customsPlace,_ _declarationAmount, suborderId, and buyer_ can be modified in the retransmission. The retransmission's _declarationAmount_ is not included in the total amount of the customs declaration.

**Retransmission conditions**

Before re-triggering the interface, make sure that the following conditions are met:

*   The declaration with the same _declarationRequestId_ exists in the Alipay system.
*   More than 5 minutes have passed since the last call. (Alipay might adjust this time value according to the actual situation.)
*   Keep all information the same except the values of the following fields:

*   _merchantCustomsCode_
*   _merchantCustomsName_
*   _customs__Code_ 
*   _declarationAmount_
*   _suborderId_
*   _buyerCertificate.holderName.__fullName_ 
*   _buyerCertificate.certificateNo_