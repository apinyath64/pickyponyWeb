from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from .models import Customer


class RegistrationForm(UserCreationForm):
    
    username = forms.CharField(label="ชื่อผู้ใช้", widget=forms.TextInput(attrs={"class": "w-full bg-gray-100 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block appearance-none"}))
    email = forms.EmailField(label="อีเมล", widget=forms.EmailInput(attrs={"class": "w-full bg-gray-100 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block appearance-none"}))
    password1 = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput(attrs={"class": "w-full bg-gray-100 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block appearance-none"}))
    password2 = forms.CharField(label="ยืนยันรหัสผ่าน", widget=forms.PasswordInput(attrs={"class": "w-full bg-gray-100 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block appearance-none"}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    username = UsernameField(label="ชื่อผู้ใช้", widget=forms.TextInput(attrs={"autofocus": "True", "class": "w-full bg-gray-100 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block appearance-none"}))
    password = forms.CharField(label="รหัสผ่าน", widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "class": "w-full bg-gray-100 text-gray-700 focus:outline-none focus:shadow-outline border border-gray-300 rounded py-2 px-4 block appearance-none"}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='รหัสผ่านเดิม', widget=forms.PasswordInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"}))
    new_password1 = forms.CharField(label='รหัสผ่านใหม่', widget=forms.PasswordInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"}))
    new_password2 = forms.CharField(label='ยืนยันรหัสผ่าน', widget=forms.PasswordInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5"}))


class MyPasswordResetForm(PasswordResetForm):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "py-3 px-4 block w-full border-2 border-gray-200 rounded-md text-sm focus:border-gray-300 focus:ring-gray-400 shadow-sm"}))


class MyPasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(label="รหัสผ่านใหม่", widget=forms.PasswordInput(attrs={"auto-complete": "current-password", "class": "py-3 px-4 block w-full border-2 border-gray-200 rounded-md text-sm focus:border-gray-300 focus:ring-gray-400 shadow-sm"}))
    new_password2 = forms.CharField(label="ยืนยันรหัสผ่าน", widget=forms.PasswordInput(attrs={"auto-complete": "current-password", "class": "py-3 px-4 block w-full border-2 border-gray-200 rounded-md text-sm focus:border-gray-300 focus:ring-gray-400 shadow-sm"}))


class ProfileSettingForm(forms.ModelForm): 
    class Meta:
        model = Customer
        fields = ["name", "locality", "city", "mobile", "zipcode"]
        labels = {
            "name": "ชื่อ",
            "locality": "ที่อยู่",
            "city": "เมือง",
            "mobile": "เบอร์โทรศัพท์",
            "zipcode": "รหัสไปรษณีย์"
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"}),
            "locality": forms.TextInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"}),
            "city": forms.Select(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"}),
            "mobile": forms.NumberInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"}),
            "zipcode": forms.NumberInput(attrs={"class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"})
        }