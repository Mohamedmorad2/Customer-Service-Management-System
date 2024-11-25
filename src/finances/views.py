from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Expense
from orders.views import orders
from orders.models import Order 
from accounts.models import UserAction 


@login_required(login_url='login') 
def create_expense(request):
    if request.method == 'POST':
        product = request.POST['Product']
        quantity = request.POST['Quantity']
        product_price = request.POST['product_price']
        purchase_date = request.POST['purchase_date']
        total_price = request.POST['Total_Price']
        status = request.POST['Status']
        notes = request.POST.get('notes', '')

        screenshot = None
        if request.FILES:
            screenshot = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(screenshot.name, screenshot)
            uploaded_file_url = fs.url(filename)
        expense = Expense(
            product=product,
            quantity=quantity,
            product_price=product_price,
            purchase_date=purchase_date,
            total_price=total_price,
            status=status,
            notes=notes,  
            created_by=request.user,
            screenshot=screenshot
        )
        finances_code = expense.code
        UserAction.objects.create(
                user=request.user,
                action_type='created',
                app_name='Finances',
                code=finances_code, 
                details=f'finances {expense.product} created.'
            )
        expense.save()
        messages.success(request, 'Expense created successfully!')
        return redirect('expenses') 

    return render(request, 'pages/create_expense.html') 


@login_required(login_url='login') 
def expenses(request):
    expense_list = Expense.objects.all()
    return render(request, 'pages/total_expenses.html', {'Expense': expense_list})

@login_required(login_url='login')
def total_sales(request):
    approved_orders = Order.objects.filter(status='Approve').order_by('-created_at')
    return render(request , 'pages/total_sales.html' ,{'Order': approved_orders})


@login_required(login_url='login')
def delete_expenses(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id)
        finances_code = expense.code
        UserAction.objects.create(
                user=request.user,
                action_type='delete',
                app_name='Finances',
                code=finances_code, 
                details=f'finances {expense.product} delete.'
            )
        expense.delete()
        messages.success(request, 'Expense Delete successfully!')
        return redirect('expenses')
    except Expense.DoesNotExist:
        return redirect('expenses') 

@login_required(login_url='login')
def expense_detail(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    return render(request, 'pages/expense_detail.html', {'expense': expense})


@login_required(login_url='login')
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        product = request.POST.get('Product')
        quantity = request.POST.get('Quantity')
        product_price = request.POST.get('product_price')
        purchase_date = request.POST.get('purchase_date')
        total_price = request.POST.get('Total_Price')
        status = request.POST.get('Status')
        notes = request.POST.get('notes')
        expense.product = product
        expense.quantity = quantity
        expense.product_price = product_price
        expense.purchase_date = purchase_date
        expense.total_price = total_price
        expense.status = status
        expense.notes = notes
        if request.FILES.get('image'):
            expense.invoice_image = request.FILES['image'] 
        finances_code = expense.code
        UserAction.objects.create(
                user=request.user,
                action_type='update',
                app_name='Finances',
                code=finances_code, 
                details=f'finances {expense.product} update.'
            )
        expense.save() 
        messages.success(request, 'Expense Updated successfully.') 
        return redirect('expenses')


    return render(request, 'pages/update_expense.html', {'expense': expense})


@login_required(login_url='login')
def update_order_finances(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        order.name = request.POST.get('name')
        order.phone_number = phone_number
        order.address = request.POST.get('address')
        order.status = request.POST.get('status')
        order.order_type = request.POST.get('order_type')
        order.product_price = request.POST.get('product_price')
        order.shipping_price = request.POST.get('shipping_price')
        order.notes = request.POST.get('notes')
        if request.FILES.get('image'):
            order.screenshot = request.FILES['image']
        finances_code = Expense.code
        UserAction.objects.create(
                user=request.user,
                action_type='update_order_finances',
                app_name='Finances',
                code=finances_code, 
                details=f'finances {Expense.product} update.'
            )
        order.save() 
        messages.success(request ,'Order Update successfully.')
        return redirect('total_sales')  

    return render(request, 'pages/update_order.html', {'order': order})


@login_required(login_url='login')
def search_expenses(request):
    # Initialize the expenses queryset
    expenses = Expense.objects.all()

    # Retrieve filter parameters from GET request
    product = request.GET.get('product')
    quantity = request.GET.get('quantity')
    product_price = request.GET.get('product_price')
    purchase_date = request.GET.get('purchase_date')
    total_price = request.GET.get('total_price')
    status = request.GET.get('status')
    created_by = request.GET.get('created_by')
    code = request.GET.get('code')

    # Apply filters if values are provided
    if product:
        expenses = expenses.filter(product=product)
    if quantity:
        expenses = expenses.filter(quantity=quantity)
    if product_price:
        expenses = expenses.filter(product_price=product_price)
    if purchase_date:
        expenses = expenses.filter(purchase_date=purchase_date)
    if total_price:
        expenses = expenses.filter(total_price=total_price)
    if status:
        expenses = expenses.filter(status=status)
    if created_by:
        expenses = expenses.filter(created_by__username__icontains=created_by)
    if code:
        expenses = expenses.filter(code__icontains=code)

    # Log user actions for each filtered order
    for expense in expenses:
        UserAction.objects.create(
            user=request.user,
            action_type='search',
            app_name='finances',
            code=expense.code, 
            details=f'Expense search for {expense.product}.'
        )

    # Render the results to the template
    return render(request, 'pages/search_expenses.html', {'expenses': expenses})
