from django.db import models

# Create your models here.
class Payment(models.Model):
    order_id = models.CharField(max_length=200)
    payment_id = models.CharField(max_length=50,blank=True,null=True)
    status = models.CharField(max_length=50,default="CREATED")
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.order_id
    
    
class Order(models.Model):
    product_name = models.CharField(max_length=255)
    amount = models.FloatField()
    status = models.CharField(max_length=50, default="PENDING") 
    paypal_order_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"
    
