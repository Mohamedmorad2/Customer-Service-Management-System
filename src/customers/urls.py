# urls.py
from django.urls import path
from . import views


urlpatterns = [
        path('create_customer/', views.create_customer, name='create_customer'),
        path('customers-list/', views.customers, name='customers'),
        path('search_customers/', views.search_customers, name='search_customers'),
        path('delete/<int:customer_id>/', views.delete_customer, name='delete_customer'),
        path('update/<int:customer_id>/', views.update_customer, name='update_customer'),
        path('customer/<int:customer_id>/detail/', views.customer_detail, name='customer_detail'),

]
