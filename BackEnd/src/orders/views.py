from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Order 
from django.contrib import messages
from customers.models import Customer
from accounts.models import UserAction 


@login_required(login_url='login') 
def create_order(request):
    customers = Customer.objects.all()  
    customer_info = None  
    if request.method == 'POST':
        selected_customer_id = request.POST.get('customer')

        if selected_customer_id:
            try:
                customer_info = Customer.objects.get(id=selected_customer_id)
            except Customer.DoesNotExist:
                customer_info = None
        name = customer_info.name if customer_info else request.POST.get('name')
        phone_number = customer_info.phone_number if customer_info else request.POST.get('phone_number')
        address = request.POST.get('address', customer_info.address if customer_info else '')
        status = request.POST.get('status')
        order_type = request.POST.get('order_type')
        product_price = request.POST.get('product_price')
        shipping_price = request.POST.get('shipping_price')
        notes = request.POST.get('notes')
        screenshot = None
        if request.FILES:
            screenshot = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(screenshot.name, screenshot)
            uploaded_file_url = fs.url(filename)
            order = Order(
                name=name,
                phone_number=phone_number,
                address=address,
                status=status,
                order_type=order_type,
                product_price=product_price,
                shipping_price=shipping_price,
                screenshot=screenshot,  
                created_by=request.user,
                notes=notes
            )
            Order_code = order.code
            UserAction.objects.create(
                user=request.user,
                action_type='created',
                app_name='Orders',
                code=Order_code, 
                details=f'Order {order.order_type} created.'
            )
            order.save()
            messages.success(request ,'Order created successfully.')
            return redirect('orders')

    return render(request, 'pages/create_order.html', {'customers': customers})


@login_required(login_url='login') 
def orders(request):
    orders_list = Order.objects.all()
    return render(request, 'pages/order.html', {'Order': orders_list})


@login_required(login_url='login')
def delete_orders(request, orders_id):
    try:
        order = Order.objects.get(id=orders_id)
        Order_code = order.code
        UserAction.objects.create(
                user=request.user,
                action_type='delete',
                app_name='Orders',
                code=Order_code, 
                details=f'Order {order.order_type} delete.'
            )
        order.delete()
        messages.success(request ,'Order Delete successfully.')
        return redirect('orders')
    except Order.DoesNotExist:
        return redirect('orders') 


@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'pages/order_detail.html', {'order': order})


@login_required(login_url='login')
def update_order(request, order_id):
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
        Order_code = order.code
        UserAction.objects.create(
                user=request.user,
                action_type='update',
                app_name='Orders',
                code=Order_code, 
                details=f'Order {order.order_type} update.'
            )
        order.save() 
        messages.success(request ,'Order Update successfully.')
        return redirect('orders')  

    return render(request, 'pages/update_order.html', {'order': order})

@login_required(login_url='login')
def search_orders(request):
    # Initialize the orders queryset
    orders = Order.objects.all()

    # Retrieve filter parameters from GET request
    name = request.GET.get('name')
    phone_number = request.GET.get('phone_number')
    date = request.GET.get('date')
    address = request.GET.get('address')
    status = request.GET.get('status')
    order_type = request.GET.get('order_type')
    product_price = request.GET.get('product_price')
    shipping_price = request.GET.get('shipping_price')
    created_by = request.GET.get('created_by')
    code = request.GET.get('code')

    # Apply filters if values are provided
    if name:
        orders = orders.filter(name__icontains=name)
    if phone_number:
        orders = orders.filter(phone_number=phone_number)
    if date:
        orders = orders.filter(created_at__icontains=date)
    if address:
        orders = orders.filter(address__icontains=address)
    if status:
        orders = orders.filter(status=status)
    if order_type:
        orders = orders.filter(order_type=order_type)
    if product_price:
        orders = orders.filter(product_price=product_price)
    if shipping_price:
        orders = orders.filter(shipping_price=shipping_price)
    if created_by:
        orders = orders.filter(created_by__username__icontains=created_by)
    if code:
        orders = orders.filter(code__icontains=code)

    # Log user actions for each filtered order
    for order in orders:
        UserAction.objects.create(
            user=request.user,
            action_type='search',
            app_name='orders',
            code=order.code,  # Use `order.code`, not `Order_code.code`
            details=f'Order {order.order_type} search.'
        )

    # Render the results to the template
    return render(request, 'pages/search_order.html', {'orders': orders})
