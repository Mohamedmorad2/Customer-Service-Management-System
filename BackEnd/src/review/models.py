from django.db import models
import os
import random
from django.utils import timezone
from django.contrib.auth.models import User
from orders.models import Order

def get_customer_image_upload_to(instance, filename):
    # Create folder with customer name and current date
    order_type = instance.order_type
    current_date = timezone.localtime(timezone.now()).strftime("Date_%Y-%m-%d_Time_%H-%M-%S")
    folder_name = f'{order_type}_{current_date}'
    
    # Determine sub-folder based on field
    if hasattr(instance, 'screenshot') and instance.screenshot == filename:
        subfolder = 'screenshots'
    else:
        subfolder = 'other'
    
    return os.path.join(f'Review_Images/{folder_name}/{subfolder}', filename)



class Review(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    name_customer = models.CharField(max_length=255, null=True, blank=True)
    order_type = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=10, decimal_places=2)
    evaluation_authority = models.CharField(
        max_length=50,
        choices=[
            ('Phone', 'Phone'),
            ('WhatsApp', 'WhatsApp'),
            ('Facebook', 'Facebook'),
            ('Instagram', 'Instagram'),
            ('Other', 'Other'),
        ]
    )
    review_text = models.TextField(null=True, blank=True)
    screenshot = models.ImageField(upload_to='reviews/screenshots/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

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
