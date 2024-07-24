The merchant can decide whether the order is split for declaration. If the value of this field is `true`, order splitting is allowed. If the value of this field is `false`, no order splitting is allowed.

#### suborderId String  

The suborder ID that is assigned by the merchant.

Notes:

*   Specify this field when _splitOrder_ is `true`. The suborder ID is transmitted to the customs as the order ID in the payment information when the following business scenarios occur:

*   A payment contains multiple commodities and needs to be submitted to different customs, or the customs require separate submission according to the commodities.
*   In a combined payment, a customs declaration is required for some commodities. 
*   Other situations where customs declaration needs to be split.