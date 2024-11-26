from django.urls import path
from . import views


urlpatterns = [
        path('', views.system_info, name='system_info'),
        path('login/', views.login, name='login'),
        path('login-emails/', views.login_emails, name='login_emails'),
        path('logout/', views.logout, name='logout'),
        path('home/', views.home, name='home'),
        # path('manage_permissions/', views.manage_permissions, name='manage_permissions'),
        path('create_user/', views.create_user, name='create_user'),
        path('users/', views.users, name='users'),
        path('logs/', views.logs_view, name='logs'),
        path('admin_logs/', views.admin_logs, name='admin_logs'),
        path('delete/<int:record_id>/', views.delete_user, name='delete_user'),
        path('update/<int:record_id>/', views.update_user, name='update_user'),
        path('profile/', views.profile_view, name='profile_view'),
        path('operations_list/', views.operations_list, name='operations_list'),
        path('contact_submit/', views.contact_submit, name='contact_submit'),
        path('email-submit/', views.email_submit, name='email_submit'),
        path('private/emails/', views.emails, name='emails'),
]
