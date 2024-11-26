# models.py
from django.db import models
from django.utils import timezone
import os
from django.utils import timezone
import random
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator 


def get_customer_image_upload_to(instance, filename):
    # Create folder with customer name and current date
    customer_name = instance.product
    current_date = timezone.localtime(timezone.now()).strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
    folder_name = f'{customer_name}_{current_date}'
    
    # Determine sub-folder based on field
    if hasattr(instance, 'screenshot') and instance.screenshot == filename:
        subfolder = 'screenshots'
    else:
        subfolder = 'other'
    
    return os.path.join(f'Expense_Images/{folder_name}/{subfolder}', filename)



class Expense(models.Model):
    PRODUCT_CHOICES = [
        ('Mug', 'Mug'),
        ('Magic Mug', 'Magic Mug'),
        ('T-shirt printing', 'T-shirt printing'),
        ('Tableau', 'Tableau'),
        ('Sticker', 'Sticker'),
    ]
    
    STATUS_CHOICES = [
        ('request', 'Request'),
        ('pending', 'Pending'),
        ('approve', 'Approve'),
        ('cancel', 'Cancel'),
    ]
    
    product = models.CharField(max_length=100, choices=PRODUCT_CHOICES)
    quantity = models.PositiveIntegerField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    screenshot = models.ImageField(upload_to=get_customer_image_upload_to) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=6, unique=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering =['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.code:  
            self.code = generate_unique_code()
        super().save(*args, **kwargs)

def generate_unique_code():
    while True:
        code = ''.join(random.choices('0123456789', k=6))  
        if not Expense.objects.filter(code=code).exists():  
            print(f"Generated unique code: {code}") 
            return code
        else:
            print(f"Duplicate code generated: {code}") 
