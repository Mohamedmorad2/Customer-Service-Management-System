from django.shortcuts import render, redirect ,get_object_or_404
from .forms import CustomUserCreationForm , LoginForm
from .models import CustomUser ,UserAction ,ContactMessage
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserPermission
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from .forms import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import os
from .models import Log
from django.http import HttpResponse
from django.core.mail import send_mail 
from django.conf import settings
from django.db import connection


@login_required(login_url='login')
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully!')
            return redirect('users')  
    else:
        form = CustomUserCreationForm()

    return render(request, 'pages/create_user.html', {'form': form})


@login_required(login_url='login')
def users(request):
    users = User.objects.all()
    return render(request, 'pages/users.html' , {'users': users})


@login_required(login_url='login')
def logs_view(request):
    logs = Log.objects.all()
    return render(request, 'pages/logs.html', {'logs': logs})


@login_required(login_url='login')
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Update successfully!')
            return redirect('users')
    else:

        form = CustomUserCreationForm(instance=user)
    
    return render(request, 'pages/update_user.html', {'form': form})


@login_required(login_url='login')
def delete_user(request, record_id):
    users = get_object_or_404(CustomUser, id=record_id)
    users.delete()
    messages.success(request, 'User Delete successfully!')
    return redirect('users')  


@login_required(login_url='login')
def search_users(request):
    # Get the search query parameters
    name = request.GET.get('name', '')  
    username = request.GET.get('username', '') 
    users = CustomUser.objects.all()
    if name:
        users = users.filter(first_name__icontains=name) 
    if username:
        users = users.filter(username__icontains=username)  
    
    return render(request, 'pages/search_users.html', {'users': users})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)  
                Log.objects.create(
                    user=user,
                    first_name=user.first_name,
                    action="login"
                )
                messages.success(request ,'Login is successful.')
                return redirect('home')
    
    context = {'form': form}
    return render(request, 'pages/login.html', context)

def logout(request):
    user = request.user
    if user.is_authenticated:
        Log.objects.create(
            user=user,
            first_name=user.first_name,
            action="logout"
        )
        auth_logout(request) 
        messages.success(request ,'logout is successful.')
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'pages/home.html')


@login_required(login_url='login')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                username = user.username
                timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{username}_{timestamp}{os.path.splitext(profile_picture.name)[1]}"
                file_path = os.path.join('Images_profile', filename)

                fs = FileSystemStorage()
                fs.save(file_path, profile_picture)
                user.profile_picture = file_path  

            user.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_view')

    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'pages/profile.html', {'form': form, 'user': user})


@login_required(login_url='login')
def operations_list(request):
    useractions = UserAction.objects.all()  
    return render(request, 'pages/operations_list.html', {'useractions': useractions})

@login_required(login_url='login')
def admin_logs(request):
    logs = LogEntry.objects.select_related('user').all()
    return render(request, 'pages/admin_logs.html' , {'django_auth_log': logs})

def system_info(request):
    return render(request, 'pages/system_info.html' )


def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        category = request.POST.get('category')
        message = request.POST.get('message')
        company_name = request.POST.get('company_name') if category == 'company' else None

        if len(phone) != 12 or not phone.isdigit():
            return HttpResponse("Phone number must be exactly 12 digits.", status=400)
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            category=category,
            message=message,
            company_name=company_name  
        )

        send_mail(
            subject=f"New Contact Form Submission ({category.capitalize()})|| Email From System Customer Service System (CSS) ",
            message=f"Name: {name}\nEmail:\n Phone: {phone}\n {email}\nCategory: {category.capitalize()}\n\nMessage:\n{message}\n\nCompany/Brand Name: {company_name}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],  
        )

        return redirect('email_submit')
    return HttpResponse("Invalid request method.", status=400)

def email_submit(request):
    return render(request, 'pages/email_submit.html') 

@login_required(login_url='login')
def emails(request):
    emails = ContactMessage.objects.all()
    return render(request, 'pages/tables_email.html' , {'emails': emails}) 

def login_emails(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)  
                Log.objects.create(
                    user=user,
                    first_name=user.first_name,
                    action="login Emails App"
                )
                messages.success(request ,'Login is successful.')
                return redirect('emails')
    
    context = {'form': form}
    return render(request, 'pages/login_email.html', context)

