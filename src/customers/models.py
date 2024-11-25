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
    
    return os.path.join(f'Customer_Images/{folder_name}/{subfolder}', filename)

class Customer(models.Model):
    INTEREST_CHOICES = [
        ('Programming', 'Programming'),
        ('Design', 'Design'),
        ('Marketing', 'Marketing'),
        ('Business', 'Business'),
        ('Other', 'Other'),
    ]

    KNOW_SOURCE_CHOICES = [
        ('Facebook', 'Facebook'),
        ('Instagram', 'Instagram'),
        ('TikTok', 'TikTok'),
        ('Friend', 'Friend'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(
        max_length=12,
        validators=[MinLengthValidator(11)],  
        blank=False  
    )
    age = models.PositiveIntegerField()
    address = models.CharField(max_length=255)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES)
    how_did_we_know = models.CharField(max_length=20, choices=KNOW_SOURCE_CHOICES)
    screenshot = models.ImageField(upload_to=get_customer_image_upload_to)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering =['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.code:  
            self.code = generate_unique_code()
        super().save(*args, **kwargs)


def generate_unique_code():
    while True:
        code = ''.join(random.choices('0123456789', k=6))  
        if not Customer.objects.filter(code=code).exists():  
            print(f"Generated unique code: {code}") 
            return code
        else:
            print(f"Duplicate code generated: {code}")  #