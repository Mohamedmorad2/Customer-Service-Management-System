# urls.py
from django.urls import path
from . import views



urlpatterns = [
        path('create_expense/', views.create_expense, name='create_expense'),
        path('expenses-list/', views.expenses, name='expenses'),
        path('total_sales/', views.total_sales, name='total_sales'),
        path('search-expenses/', views.search_expenses, name='search_expenses'),
        path('delete/<int:expense_id>/', views.delete_expenses, name='delete_expenses'),
        path('update/<int:expense_id>/', views.update_expense, name='update_expense'),
        path('update_order_finances/<int:order_id>/', views.update_order_finances, name='update_order_finances'),
        path('expenses/<int:expense_id>/detail/', views.expense_detail, name='expense_detail'),
]
