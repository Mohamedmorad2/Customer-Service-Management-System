from django.contrib import admin
from .models import CustomUser
from .models import Log
from .models import UserAction
from unfold.admin import ModelAdmin



class LogsAdmin(ModelAdmin):
    list_display = ['id' ,'user_id','user','first_name' ,'action' ,'timestamp']
class UserActionAdmin(ModelAdmin):
    list_display = ['id' ,'user_id','user','action_type' ,'action_time' ,'code' ,'app_name','details']

    # Register your models here.
admin.site.register( Log , LogsAdmin)
admin.site.register( UserAction , UserActionAdmin)