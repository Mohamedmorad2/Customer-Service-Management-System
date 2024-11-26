from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from orders.models import Order
from customers.models import Customer
from finances.models import Expense
from django.db import models
# Create your views here.


@login_required(login_url='login')
def dashboard(request):
    total_expenses = Expense.objects.aggregate(total=Sum(Cast('product_price', FloatField())))['total'] or 0
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()

    context = {
        'total_expenses': total_expenses,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'messages': messages.get_messages(request),
    }
    return render(request, 'pages/dashboard.html', context)
