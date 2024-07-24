|
| PARAM\_ILLEGAL | F | The required parameters are not passed, or illegal parameters exist. For example, a non-numeric input, an invalid date, or the length and type of the parameter are wrong. | Check and verify whether the required request fields (including the header fields and body fields) of the current API are correctly passed and valid.

 |
| PROCESS\_FAIL | F | A general business failure occurred. | Do not retry. Human intervention is usually needed. It is recommended that you contact Alipay Technical Support to troubleshoot the issue.

 |
| REPEAT\_REQ\_INCONSISTENT | F | The amount or currency is different from the previous request. | Use a unique _declarationRequestId_ value to initiate the customs declaration again. In retransmission scenarios, make sure to meet all the conditions in the retransmission conditions section and retransmission.