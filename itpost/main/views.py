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
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        posts = Post.objects.prefetch_related('files').all().order_by('-created_at')
        return render(request, 'all_post.html', {
            'user': user,
            'posts': posts
        })
    
    def post(self, request):
        return
    

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect('/login')
    

class CreateView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)

        create_form = CreatePostForm(user=user)

        return render(request, 'create_post.html', {
            'user': user,
            'create_form': create_form
        })
    
    def post(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)

        create_form = CreatePostForm(request.POST, request.FILES, user=user)

        if create_form.is_valid():
            post = create_form.save(commit=False)
            post.created_by = user
            post.save()
            create_form.save_m2m()

            print("FILES:", request.FILES.getlist('files'))
            for f in request.FILES.getlist('files'):
                PostFile.objects.create(post=post, file=f)

            return redirect('/')
        else:
            print("Form errors:", create_form.errors)
            return render(request, 'create_post.html', {
                'user': user,
                'create_form': create_form
            })
        
class ProfileView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        academic_info = AcademicInfo.objects.get(user=user)
        user_posts = Post.objects.filter(created_by=user).prefetch_related('files').order_by('-created_at')
        can_edit = False
        if user.id == request.session.get('user_id'):
            can_edit = True

        return render(request, 'profile.html', {
            'user': user,
            'academic_info': academic_info,
            'user_posts': user_posts,
            'can_edit': can_edit
        })

# class TestView(View):
#     def get(self, request):
#         user_id = request.session.get('user_id')
#         user = User.objects.get(pk=user_id)
#         posts = Post.objects.prefetch_related('files').all().order_by('-created_at')
#         return render(request, 'main.html', {
#             'user': user,
#             'posts': posts
#         })