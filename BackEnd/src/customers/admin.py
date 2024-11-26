from django.contrib import admin
from .models import Customer




class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number','age' ,'address' ,'interest' ,'how_did_we_know' ,'notes' , 'code', 'created_at','created_by']

    # Register your models here.
admin.site.register( Customer,CustomerAdmin)