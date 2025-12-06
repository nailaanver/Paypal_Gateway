from django.urls import path
from . import views

urlpatterns = [
    path('orders/create/',views.create_order,name='create-order'),
    path('orders/list/',views.list_orders,name='list_order'),
    path('orders/<int:pk>/',views.get_order,name='get-order'),
    path('orders/update/<int:pk>/',views.update_order,name='update-order'),
    path('orders/delete/<int:pk>/',views.delete_order,name='delete_order'),
]