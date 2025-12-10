from django.urls import path
from . import views
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response


urlpatterns = [
    path('orders/create/',views.create_order,name='create-order'),
    path('orders/list/',views.list_orders,name='list_order'),
    path('orders/<int:pk>/',views.get_order,name='get-order'),
    path('orders/update/<int:pk>/',views.update_order,name='update-order'),
    path('orders/delete/<int:pk>/',views.delete_order,name='delete_order'),
    
    
    path("orders/<int:pk>/create-payment/", views.create_paypal_payment),
    path('payments/execute/', views.execute_payment, name='execute-payment'),
    path('payments/cancel/', views.cancel_payment, name='cancel-payment'),
    
    path('register/',views.register_user,name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    

]