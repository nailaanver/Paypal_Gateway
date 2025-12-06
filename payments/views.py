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
        "redirect_urls":{
            "return_url":"http://localhost:8000/api/payments/execute/",
            "cancel_url": "http://localhost:8000/api/payments/cancel/",
        },
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
    
    payment = paypalrestsdk.Payment.find(payment_id)
    
    if payment.execute({"prayer_id":payer_id}):
        order = Order.objects.get(paypal_order_id=payment_id)
        order.status = "PAID"
        order.save()
        
        return Response({"message":"Payment successful!"})
    return Response({"error":payment.error},status=400)

# cancel payment

@api_view(['GET'])
def cancel_payment(request):
    return Response({"message":"Payment cancelled"})
