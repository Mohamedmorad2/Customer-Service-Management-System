import random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Customer

def generate_unique_code():
    while True:
        code = ''.join(random.choices('0123456789', k=6))  
        if not Customer.objects.filter(code=code).exists():  
            return code

@receiver(pre_save, sender=Customer)
def assign_unique_code(sender, instance, **kwargs):
    if not instance.code:  
        instance.code = generate_unique_code()
