Note: This field is returned when these two conditions are met:

*   _resultCode_ is `S`. 
*   The customs receipt is returned.  

More information about this field

*   Maximum length: 32 characters

API Explorer

Sample CodesRun in Sandbox

### Request

URL

North America

https://open-na-global.alipay.com/ams/api/v1/customs/declare

Request Body

Copy

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

{

"declarationAmount": {

"currency": "CNY",

"value": "100"

},

"merchantCustomsInfo": {

"merchantCustomsName": "amsdemo",

"merchantCustomsCode": "amsdemoskr"

},

"paymentId": "20211117194010800100188180203227785",

"splitOrder": false,

"customs": {

"region": "CN",

"customsCode": "ZONGSHU"

},

"declarationRequestId": "req123",

"buyerCertificate": {

"holderName": {

"firstName": "f",

"lastName": "l",

"fullName": "cangxi.lj",

"middleName": "m"

},

"certificateNo": "510502199504139527",

"certificateType": "ID\_CARD"

}

}