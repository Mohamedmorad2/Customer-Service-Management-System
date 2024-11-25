# forms.py
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django import forms
from .models import CustomUser
from django.forms.widgets import PasswordInput , TextInput
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
import os
from django.db import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name' ,'username', 'password1', 'password2'] 


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name']  # أضف المزيد من الحقول حسب الحاجة

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data['profile_picture']:
            profile_picture = self.cleaned_data['profile_picture']
            username = user.username
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')

            # تحديد اسم الملف
            filename = f"{username}_{timestamp}{os.path.splitext(profile_picture.name)[1]}"
            folder_path = os.path.join('Images_profile', username)

            # إنشاء المجلد إذا لم يكن موجودًا
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # تحديد المسار الكامل للملف
            file_path = os.path.join(folder_path, filename)

            # حفظ الصورة
            fs = FileSystemStorage()
            fs.save(file_path, profile_picture)  # حفظ الصورة في المسار المحدد
            user.profile_picture = file_path  # تحديث حقل الصورة الشخصية

        if commit:
            user.save()  # حفظ المستخدم
        return user
