from django.db import models
from django.utils import timezone
import os
from django.utils import timezone
import random
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator 


def get_customer_image_upload_to(instance, filename):
    # Create folder with customer name and current date
    customer_name = instance.name
    current_date = timezone.localtime(timezone.now()).strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
    folder_name = f'{customer_name}_{current_date}'
    
    # Determine sub-folder based on field
    if hasattr(instance, 'screenshot') and instance.screenshot == filename:
        subfolder = 'screenshots'
    else:
        subfolder = 'other'
    
    return os.path.join(f'Orders_Images/{folder_name}/{subfolder}', filename)



class Order(models.Model):
    STATUS_CHOICES = [
        ('request', 'Request'),
        ('pending', 'Pending'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
    ]

    ORDER_CHOICES = [
        ('Mug', 'Mug'),
        ('Magic Mug', 'Magic Mug'),
        ('T-shirt printing', 'T-shirt printing'),
        ('Tableau', 'Tableau'),
        ('Sticker', 'Sticker'),
    ]

    name = models.CharField(max_length=255 , null=False)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    order_type = models.CharField(max_length=50, choices=ORDER_CHOICES)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    screenshot = models.ImageField(upload_to=get_customer_image_upload_to) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.TextField(max_length=6, unique=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering =['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.code:  
            self.code = generate_unique_code()
        super().save(*args, **kwargs)

def generate_unique_code():
    while True:
        code = ''.join(random.choices('0123456789', k=6))  
        if not Order.objects.filter(code=code).exists():  
            print(f"Generated unique code: {code}") 
            return code
        else:
            print(f"Duplicate code generated: {code}") 
