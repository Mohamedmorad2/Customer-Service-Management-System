from django.contrib import admin
from .models import Order




class OrdersAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number','address' ,'notes' , 'code', 'created_at','created_by']

    # Register your models here.
admin.site.register( Order,OrdersAdmin)