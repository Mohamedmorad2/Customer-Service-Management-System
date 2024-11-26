from django.contrib import admin
from .models import Review




class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id','order_type','product_price' ,'shipping_price' , 'evaluation_authority','code', 'created_at','created_by']

    # Register your models here.
admin.site.register( Review,ReviewsAdmin)