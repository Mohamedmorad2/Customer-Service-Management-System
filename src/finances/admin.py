from django.contrib import admin
from .models import Expense



class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','product_price' ,'purchase_date' ,'total_price', 'code', 'created_at','created_by']

    # Register your models here.
admin.site.register( Expense,ExpenseAdmin)