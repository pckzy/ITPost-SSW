from django import forms
from .models import *
from django.core.exceptions import ValidationError
import re

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'password'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'email': forms.EmailInput(attrs={'placeholder': 'e.g. 6607xxx@kmitl.ac.th', 'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and not email.endswith('@kmitl.ac.th'):
            raise forms.ValidationError("อีเมลต้องลงท้ายด้วย @kmitl.ac.th")

        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        pattern = r'^[0-9]{2}07[0-9]{4}$'

        if not re.match(pattern, username):
            raise forms.ValidationError('ต้องเป็นรหัสนักศึกษาเท่านั้น')

        return username


class AcademicInfoForm(forms.ModelForm):
    class Meta:
        model = AcademicInfo
        fields = [
            'major', 'specialization', 'year'
        ]
        widgets = {
            'year': forms.Select(attrs={'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'major': forms.Select(attrs={'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'}),
            'specialization': forms.Select(attrs={'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['major'].empty_label = "-- เลือกสาขา --"
        self.fields['specialization'].empty_label = "-- เลือกแขนง --"


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the username',
            'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter the password',
            'class': 'border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username, password=password)
                cleaned_data["user"] = user
            except User.DoesNotExist:
                raise ValidationError("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง โปรดลองอีกครั้ง")

        return cleaned_data
    

class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['post_type'].empty_label = None

        if user and user.role.id == 3:
            self.fields['post_type'].queryset = PostType.objects.filter(id__gt=1).order_by('-id')

    class Meta:
        model = Post
        fields = ['post_type', 'years', 'majors', 'specializations', 'title', 'content']
        widgets = {
            'post_type': forms.Select(),
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-[#e5e7eb] rounded text-xl leading-5 bg-white p-2'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full border border-[#e5e7eb] rounded text-md leading-5 bg-white p-2',
                'rows': 6,
            })
        }
    
