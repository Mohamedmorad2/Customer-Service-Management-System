from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from accounts.models import UserAction 
# Create your views here.


@login_required(login_url='login')  
def create_customer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')
        address = request.POST.get('address')
        interest = request.POST.get('Interest')
        how_did_we_know = request.POST.get('howDidWeKnow')
        notes = request.POST.get('notes')

        if Customer.objects.filter(phone_number=phone_number).exists():
            messages.error(request, 'The phone number already exists.')  
        else:
            screenshot = None
            if request.FILES:
                screenshot = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(screenshot.name, screenshot)
                uploaded_file_url = fs.url(filename)
            customer = Customer.objects.create(
                name=name,
                phone_number=phone_number,
                age=age,
                address=address,
                interest=interest,
                how_did_we_know=how_did_we_know,
                screenshot=screenshot,
                notes=notes,
                created_by=request.user  
            )

            customer_code = customer.code
            UserAction.objects.create(
                user=request.user,
                action_type='created',
                app_name='customers',
                code=customer_code, 
                details=f'Customer {customer.name} created.'
            )

            messages.success(request, 'Customer created successfully.')  
            return redirect('customers') 

    return render(request, 'pages/create_customer.html')


@login_required(login_url='login')
def customers(request):
    customer_list = Customer.objects.all()
    return render(request, 'pages/customers.html', {'customers': customer_list})



@login_required(login_url='login')
def search_customers(request):
    name = request.GET.get('name', '')
    phone_number = request.GET.get('phone_number', '')
    age = request.GET.get('age', '')
    date = request.GET.get('date', '')
    address = request.GET.get('address', '')
    interest = request.GET.get('interest', '')
    how_did_we_know = request.GET.get('howDidWeKnow', '')
    created_by = request.GET.get('created_by', '')
    code = request.GET.get('code', '')

    customers = Customer.objects.all()

    if name:
        customers = customers.filter(name__icontains=name)
    if phone_number:
        customers = customers.filter(phone_number__icontains=phone_number)
    if age:
        customers = customers.filter(age=age)
    if date:
        customers = customers.filter(created_at__icontains=date)
    if address:
        customers = customers.filter(address__icontains=address)
    if interest:
        customers = customers.filter(interest__icontains=interest)
    if how_did_we_know:
        customers = customers.filter(how_did_we_know__icontains=how_did_we_know) 
    if created_by:
        customers = customers.filter(created_by__username__icontains=created_by)
    if code:
        customers = customers.filter(code__icontains=code)

    for customer in customers:
        UserAction.objects.create(
            user=request.user,
            action_type='search',
            app_name='customers',
            code=customer.code, 
            details=f'Customer {customer.name} search.'
        )

    return render(request, 'pages/search_customers.html', {'customers': customers})


@login_required(login_url='login')
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer_code = customer.code
        UserAction.objects.create(
        user=request.user,
        action_type='delete',
        app_name='customers',
        code=customer_code, 
        details=f'Customer {customer.name} deleted.'
        )
        customer.delete()
        return redirect('customers')
    except Customer.DoesNotExist:
        return redirect('customers') 


@login_required(login_url='login')
def update_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)

    old_data = {
        'name': customer.name,
        'phone_number': customer.phone_number,
        'age': customer.age,
        'address': customer.address,
        'interest': customer.interest,
        'how_did_we_know': customer.how_did_we_know,
        'notes': customer.notes,
        'screenshot': customer.screenshot.url if customer.screenshot else None
    }

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        if Customer.objects.exclude(id=customer.id).filter(phone_number=phone_number).exists():
            messages.error(request, 'The phone number already exists.')  
        else:
            customer.name = request.POST.get('name', customer.name)
            customer.phone_number = phone_number
            customer.age = request.POST.get('age', customer.age)
            customer.address = request.POST.get('address', customer.address)
            customer.interest = request.POST.get('Interest', customer.interest)
            customer.how_did_we_know = request.POST.get('howDidWeKnow', customer.how_did_we_know)
            customer.notes = request.POST.get('notes', customer.notes)
            if request.FILES.get('image'):
                customer.screenshot = request.FILES['image']
            new_data = {
                'name': customer.name,
                'phone_number': customer.phone_number,
                'age': customer.age,
                'address': customer.address,
                'interest': customer.interest,
                'how_did_we_know': customer.how_did_we_know,
                'notes': customer.notes,
                'screenshot': customer.screenshot.url if customer.screenshot else None
            }


            changes = []
            for field in old_data:
                if old_data[field] != new_data[field]:
                    changes.append(f'{field}: "{old_data[field]}" -> "{new_data[field]}"')

            changes_text = "; ".join(changes)
            customer_code = customer.code
            UserAction.objects.create(
                user=request.user,
                action_type='update',
                app_name='customers',
                code=customer_code, 
                details=f'Customer {customer.name} updated. Changes: {changes_text}'
            )

            customer.save()  
            messages.success(request, 'Customer updated successfully.') 
            return redirect('customers')  

    return render(request, 'pages/update_customer.html', {'customer': customer})


@login_required(login_url='login')
def customer_detail(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        # Handle the case where the customer does not exist
        return redirect('customers')

    return render(request, 'pages/customer_detail.html', {'customer': customer})

