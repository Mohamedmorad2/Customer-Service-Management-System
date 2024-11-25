from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Order
from .models import Review 
from django.contrib import messages
from accounts.models import UserAction 



@login_required(login_url='login')
def create_review(request):
    if request.method == 'POST':
        selected_order_id = request.POST.get('order')
        if selected_order_id:
            try:
                order_info = Order.objects.get(id=selected_order_id)
            except Order.DoesNotExist:
                order_info = None
            if Review.objects.filter(order=order_info).exists():
                messages.error(request, "This order has already been reviewed.")
                return redirect('create_review')

        name_customer = order_info.name if order_info else request.POST.get('name')
        order_type = order_info.order_type if order_info else request.POST.get('order_type')
        product_price = order_info.product_price if order_info else request.POST.get('product_price')
        shipping_price = order_info.shipping_price if order_info else request.POST.get('shipping_price')
        evaluation_authority = request.POST.get('evaluation_authority')
        review_text = request.POST.get('review')
        screenshot = request.FILES.get('image')

        review = Review(
            order=order_info, 
            name_customer=name_customer, 
            order_type=order_type,
            product_price=product_price,
            shipping_price=shipping_price,
            evaluation_authority=evaluation_authority,
            review_text=review_text,
            created_by=request.user,
            screenshot=screenshot
        )
        review.save()
        Review_code = review.code
        UserAction.objects.create(
            user=request.user,
            action_type='created',
            app_name='Review',
            code=Review_code, 
            details=f'Review ID - {review.id} || Order Type - {review.order_type} created.'
            )
        messages.success(request, "Review created successfully!")
        return redirect('reviews') 
    orders = Order.objects.filter(status='Approve')

    return render(request, 'pages/create_review.html', {'orders': orders})

@login_required(login_url='login')
def create_review_orders(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status != 'Approve':
        messages.error(request, "You cannot create a review for this order because its status is not 'Approve'.")
        return redirect('orders') 

    existing_review = Review.objects.filter(order=order).exists() 
    if existing_review:
        messages.error(request, "This order has already been reviewed.")  
        return redirect('orders')

    if request.method == 'POST':
        order_info = order
        name_customer = order_info.name 
        order_type = order_info.order_type 
        product_price = order_info.product_price  
        shipping_price = order_info.shipping_price  
        evaluation_authority = request.POST.get('evaluation_authority')
        review_text = request.POST.get('review')
        screenshot = request.FILES.get('image')

        review = Review(
            order=order_info,
            name_customer=name_customer, 
            order_type=order_type,
            product_price=product_price,
            shipping_price=shipping_price,
            evaluation_authority=evaluation_authority,
            review_text=review_text,
            created_by=request.user,
            screenshot=screenshot
        )
        review.save()

        Review_code = review.code
        UserAction.objects.create(
            user=request.user,
            action_type='created',
            app_name='Review',
            code=Review_code, 
            details=f'Review FOR Order ID - {review.id} || Order Type - {review.order_type} created.'
        )

        messages.success(request, "Review created successfully!")
        return redirect('reviews')  

    orders = Order.objects.filter(status='Approve') 

    return render(request, 'pages/create_review_order.html', {'order': order, 'orders': orders})


@login_required(login_url='login')
def reviews(request):
    reviews = Review.objects.all()
    
    return render(request, 'pages/review.html' , {'review': reviews})

@login_required(login_url='login')
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'pages/review_detail.html', {'review': review})


@login_required(login_url='login')
def delete_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
        Review_code = review.code
        UserAction.objects.create(
            user=request.user,
            action_type='Delete',
            app_name='Review',
            code=Review_code, 
            details=f'Review ID - {review.id} || Order Type - {review.order_type} Delete.'
        )
        review.delete()
        messages.success(request ,'Review Delete successfully.')
        return redirect('reviews')
    except Review.DoesNotExist:
        return redirect('reviews') 


@login_required(login_url='login')
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.method == 'POST':
        review.review_text = request.POST.get('review_text', review.review_text)
        review.evaluation_authority = request.POST.get('evaluation_authority', review.evaluation_authority)

        if 'screenshot' in request.FILES:
            review.screenshot = request.FILES['screenshot']
        Review_code = review.code
        UserAction.objects.create(
            user=request.user,
            action_type='update',
            app_name='Review',
            code=Review_code, 
            details=f'Review ID - {review.id} || Order Type - {review.order_type} Update.'
        )
        review.save()  

        messages.success(request, "Review updated successfully!")
        return redirect('reviews') 

    return render(request, 'pages/update_review.html', {'review': review})


@login_required(login_url='login')
def search_review(request):
    order_type = request.GET.get('order_type', '')
    product_price = request.GET.get('product_price', '')
    shipping_price = request.GET.get('shipping_price', '')
    date = request.GET.get('date', '')
    evaluation_authority = request.GET.get('evaluation_authority', '')
    created_by = request.GET.get('created_by', '')
    code = request.GET.get('code', '')

    reviews = Review.objects.all()

    if order_type:
        reviews = reviews.filter(order_type__icontains=order_type)
    if product_price:
        reviews = reviews.filter(product_price=product_price)
    if shipping_price:
        reviews = reviews.filter(shipping_price=shipping_price)
    if date:
        reviews = reviews.filter(created_at__date=date)
    if evaluation_authority:
        reviews = reviews.filter(evaluation_authority__icontains=evaluation_authority)
    if created_by:
        reviews = reviews.filter(created_by__username__icontains=created_by)
    if code:
        reviews = reviews.filter(code__icontains=code)

    for review in reviews:
        Review_code = review.code
        UserAction.objects.create(
            user=request.user,
            action_type='search',
            app_name='Review',
            code=Review_code,
            details=f'Review ID - {review.id} || Order Type - {review.order_type} search.'
        )

    return render(request, 'pages/search_review.html', {'reviews': reviews})