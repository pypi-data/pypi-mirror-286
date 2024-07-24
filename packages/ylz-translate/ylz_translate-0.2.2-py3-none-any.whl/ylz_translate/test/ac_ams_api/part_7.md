*   `CUP`: indicates that the clearing channel is Unionpay. For example, when the user uses the bank card to pay, this value might be returned.
*   `NUCC`: indicates that the clearing channel is NetsUnion. For example, when the user uses the bank card to pay, this value might be returned.
*   `OTHER`: indicates that the clearing channel is others. For example, when the user uses credit products such as Huabei, this value is returned.

Note: This field is returned when these two conditions are met:

*   _resultCode_ is `S`. 
*   The customs receipt is returned. 

#### clearingTransactionId String  

The clearing organization's serial number.

Note: This field is returned when these two conditions are met:

*   _resultCode_ is `S`.
*   The customs receipt is returned. 

More information about this field

*   Maximum length: 64 characters

#### customsProviderRegistrationId String  

The registration ID in the customs system.