from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Value, Count, Q
from django.db.models.functions import Concat
from django.http import HttpResponse

from .models import *
from main.forms import *


class LoginView(View):
    def get(self, request):
        user_form = LoginForm()

        return render(request, 'login.html', {
            'user_form': user_form
        })

    def post(self, request):
        user_form = LoginForm(request.POST)
        if user_form.is_valid():
            user = user_form.cleaned_data['user']
            request.session['user_id'] = user.id
            return redirect('/')
        
        return render(request, 'login.html', {
            'user_form': user_form
        })

    
class RegisterView(View):
    def get(self, request):
        user_form = UserForm()
        academic_form = AcademicInfoForm()

        return render(request, 'register.html', {
            'user_form': user_form,
            'academic_form': academic_form
        })

    def post(self, request):
        user_form = UserForm(request.POST)
        academic_form = AcademicInfoForm(request.POST)
        
        if user_form.is_valid() and academic_form.is_valid():
            user = user_form.save()
            
            academic = academic_form.save(commit=False)
            academic.user = user
            academic.save()
            
            return redirect('/login')
        
        return render(request, 'register.html', {
            'user_form': user_form,
            'academic_form': academic_form
        })


class MainView(View):
    def get(self, request):
        return render(request, 'main.html')
    
    def post(self, request):
        return