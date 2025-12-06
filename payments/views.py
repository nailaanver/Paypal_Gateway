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
