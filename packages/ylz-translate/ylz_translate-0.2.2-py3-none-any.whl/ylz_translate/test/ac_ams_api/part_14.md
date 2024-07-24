*   If _declarationAmount_ has changed, the new declaration amount cannot exceed the original total transaction amount.

**Retransmission Response**

The following list describes the responses under different situations:

*   If retransmission conditions are not met and none of the parameter values have changed, return idempotent success.
*   If retransmission conditions are not met but one or more parameter values have changed, the error code `CONTEXT_INCONSISTENT` or other error codes will be returned.
*   If retransmission conditions are met and retransmission is successful, the return value will be the same as that which was returned during the first successful transmission. 

### Result/Error codes

| Code | Value | Message | Further action |
| --- | --- | --- | --- |
| SUCCESS | S | Success | The customs declaration is successful. Call the **inquiryDeclarationRequests** interface to query the customs declaration result.
 |
| ACCESS\_DENIED | F | Access is denied. | Contact Alipay Technical Support for detailed reasons.

 |
| INVALID\_API | F | The called API is invalid or not active. | Contact Alipay Technical Support to resolve the issue.