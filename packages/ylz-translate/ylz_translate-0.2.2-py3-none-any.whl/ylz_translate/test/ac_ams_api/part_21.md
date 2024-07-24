*   `S`: When this value is returned, the API call succeeds.
*   `F`: When this value is returned, the API call fails. Take actions according to the corresponding result message or call the API again with a new _paymentRequestId_ value. If the issue persists, contact Alipay Technical Support.
*   `U`: When this value is returned, check the result code:

*   Result code is not `PAYMENT_IN_PROCESS`: The API call fails. Call this API again with a new _paymentRequestId value_.
*   Result code is `PAYMENT_IN_PROCESS`: Check whether one or more of the three URLs (appLinkUrl, normalUrl, schemeUrl) are returned:

*   one or more of the URLs returned: The transaction is created successfully. Redirect your user to the address specified by the URL to complete the payment.
*   no URLs returned: The transaction creation fails. Call the **pay** API again with a new _paymentRequestId_ value. If the issue persists, contact Alipay Technical Support.

### Result/Error codes