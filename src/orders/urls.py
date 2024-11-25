# urls.py
from django.urls import path
from . import views


urlpatterns = [
        path('create_order/', views.create_order, name='create_order'),
        path('orders-list/', views.orders, name='orders'),
        path('search-orders/', views.search_orders, name='search_orders'),
        path('delete/<int:orders_id>/', views.delete_orders, name='delete_orders'),
        path('update/<int:order_id>/', views.update_order, name='update_order'),
        path('order/<int:order_id>/detail/', views.order_detail, name='order_detail'),

]
