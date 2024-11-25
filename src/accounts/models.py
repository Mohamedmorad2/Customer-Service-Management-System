# models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change the related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change the related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    class Meta:
        ordering =['-date_joined']



class UserPermission(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_view = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Permissions"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='Images_profile/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    first_name = models.CharField(max_length=150) 
    action = models.CharField(max_length=50)  
    timestamp = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"


# class Operation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 
#     operation_type = models.CharField(max_length=50) 
#     order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True) 
#     created_at = models.DateTimeField(auto_now_add=True) 

#     def __str__(self):
#         return f"{self.user.username} - {self.operation_type} - {self.created_at}"



class UserAction(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    APP_CHOICES = [
        ('accounts', 'accounts'),
        ('customers', 'customers'),
        ('finances', 'finances'),
        ('orders', 'orders'),
        ('review', 'review'),
    ]
    


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=10, choices=ACTION_CHOICES)
    app_name = models.CharField(max_length=10, choices=APP_CHOICES)
    action_time = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=6)
    details = models.TextField(null=True, blank=True)  



class ContactMessage(models.Model):
    CATEGORY_CHOICES = [
        ('company', 'Company/Brand'),
        ('personal', 'Personal'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    message = models.TextField()
    company_name = models.CharField(max_length=255, null=True, blank=True)  # إضافة حقل الشركة/البراند
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
