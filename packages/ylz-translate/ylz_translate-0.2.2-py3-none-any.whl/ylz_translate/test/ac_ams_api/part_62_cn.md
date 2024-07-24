2019年10月24日
===============

在线支付与店内支付
-------------------

*   对**pay**接口的请求进行了以下修改：

    *   移除了 _payToAmount_
    *   移除了 _paymentQuote_
    *   更新了 _paymentAmount_ 的描述，并将其设为必填字段
    *   更新了 _paymentFactor_ 的子字段

*   对**pay**接口的响应进行了以下修改：

    *   移除了 _payToAmount_
    *   更新了 _paymentQuote_ 的描述
    *   更新了 _paymentAmount_ 的描述，并将其设为必填字段
    *   添加了 _actualPaymentAmount_
    *   移除了 _nonGuaranteeCouponValue_

*   对**notifyPayment**接口的请求进行了以下更新：

    *   移除了 _payToAmount_
    *   更新了 _paymentQuote_ 的描述
    *   更新了 _paymentAmount_ 的描述，并将其设为必填字段
    *   添加了 _actualPaymentAmount_
    *   移除了 _nonGuaranteeCouponValue_