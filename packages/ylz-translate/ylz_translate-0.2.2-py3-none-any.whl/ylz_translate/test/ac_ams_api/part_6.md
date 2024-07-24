#### customsPaymentId String  

The payment ID provided to the customs by the declaration service provider.

Note: This field is returned when _result.resultCode_ is `S`.

More information about this field

*   Maximum length: 64 characters

#### customsOrderId String  

The order ID provided to the customs by the declaration service provider.

Note: This field is returned when _result.resultCode_ is `S`.

More information about this field

*   Maximum length: 64 characters

#### identityCheckResult String  

The identity check result. Valid values are:

*   `CHECK_PASSED`: indicates that the buyer is also the payer.
*   `CHECK_NOT_PASSED`: indicates that the buyer is not the payer.

Note: This field is returned when _result.resultCode_ is `S`. If this field is not returned, it indicates that the buyer's identity is not checked.

#### clearingChannel String  

The clearing organization. Valid values are: