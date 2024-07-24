|
| RISK\_REJECT | F | The request is rejected because of the risk control. | Prompt the user that the request is rejected because the risk control failed.

 |
| SYSTEM\_ERROR | F | A system error occurred. | Do not retry, and contact Alipay Technical Support for more details.

 |
| TOTAL\_DECLARATION\_AMOUNT\_EXCEED | F | The total declared amount exceeds the payment amount. | Confirm whether the total declared amount exceeds the payment amount. Create a new declaration by using an amount less than or equal to the payment amount, or contact Alipay Technical Support.

 |
| USER\_STATUS\_ABNORMAL | F | The user status is abnormal on the wallet side. | Contact Alipay Technical Support to know the specific reasons.

 |
| REQUEST\_TRAFFIC\_EXCEED\_LIMIT | U | The request traffic exceeds the limit. | Call the interface again to resolve the issue. If not resolved, contact Alipay Technical Support.