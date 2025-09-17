from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Value, Count, Q
from django.db.models.functions import Concat
from django.http import HttpResponse

from .models import *
from main.forms import *
from django.forms import modelformset_factory

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

def landing_page(request):
    return render(request, "main_page.html")

class LoginView(View):
    def get(self, request):
        return

    def post(self, request):
        return
    
class RegisterView(View):
    def get(self, request):
        return


    def post(self, request):
        return

