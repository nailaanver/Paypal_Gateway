from django.shortcuts import render
import paypalrestsdk
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializer import OrderSerializer


@api_view(['POST'])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(status='PENDING')
        return Response(serializer.data,status=201)
    return Response(serializer.errors,status=400)

@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_order(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"},status=404)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)

@api_view(['PUT','PATCH'])
def update_order(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"},status=404)
    
    serializer = OrderSerializer(order,data=request.data,partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors,status=400)

@api_view(['DELETE'])
def delete_order(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
    
    order.delete()
    return Response({"message":"Order deleted"},status=status.HTTP_204_NO_CONTENT)

# create paypal payment

@api_view(['POST'])
def create_paypal_payment(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error":"Order not found"},status=404)
    
    payment =paypalrestsdk.Payment({
        "intent":"sale",
        "payer":{"payment_method":"paypal"},
<<<<<<< HEAD
        "redirect_urls": {
    "return_url": "http://localhost:8000/execute/",
    "cancel_url": "http://localhost:8000/cancel/",
},

=======
        "redirect_urls":{
            "return_url":"http://localhost:8000/api/payments/execute/",
            "cancel_url": "http://localhost:8000/api/payments/cancel/",
        },
>>>>>>> af632ef10292e9b381cba117a4dc62c6f8d92b1e
        "transactions":[{
            "amount":{
                "total":str(order.amount),
                "currency":"USD",
            },
            "description":f"Payment for order {order.id}"
        }]
    })
    
    if payment.create():
        order.paypal_order_id = payment.id
        order.status = "CREATED"
        order.save()
        
        approval_url = [
            link.href for link in payment.links if link.rel == "approval_url"
        ][0]
        
        return Response({
            "paypal_order_id":payment.id,
            "approval_url":approval_url
        })
    return Response({"error":payment.error},status=400)

# execute payment

@api_view(['GET'])
def execute_payment(request):
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")
<<<<<<< HEAD

    # 1. Check if paymentId and PayerID exist
    if not payment_id or not payer_id:
        return Response(
            {"error": "Missing paymentId or PayerID"},
            status=400
        )

    # 2. Find PayPal payment
    try:
        payment = paypalrestsdk.Payment.find(payment_id)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

    # 3. Execute payment (correct key = payer_id)
    if payment.execute({"payer_id": payer_id}):
        
        # 4. Update your order status
        try:
            order = Order.objects.get(paypal_order_id=payment_id)
            order.status = "PAID"
            order.save()
        except Order.DoesNotExist:
            return Response(
                {"warning": "Payment executed but order not found"},
                status=200
            )

        return Response({"message": "Payment successful!"})

    # 5. If PayPal returns error
    return Response({"error": payment.error}, status=400)

=======
    
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"prayer_id":payer_id}):
        order = Order.objects.get(paypal_order_id=payment_id)
        order.status = "PAID"
        order.save()
        
        return Response({"message":"Payment successful!"})
    return Response({"error":payment.error},status=400)
>>>>>>> af632ef10292e9b381cba117a4dc62c6f8d92b1e

# cancel payment

@api_view(['GET'])
def cancel_payment(request):
    return Response({"message":"Payment cancelled"})
