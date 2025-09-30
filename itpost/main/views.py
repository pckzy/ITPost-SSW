from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Value, Count, Q
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from main.forms import *
from .serializers import *


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
        user_logged = User.objects.get(pk=user_id)
        user = User.objects.get(pk=user_id)
        posts_list = Post.objects.prefetch_related('files').filter(status='approved').order_by('-created_at')

        search = request.GET.get('search', '')
        year_query = request.GET.getlist('year')
        major_query = request.GET.getlist('major')
        specialization_query = request.GET.getlist('specialization')

        if search:
            posts_list = posts_list.annotate(full_name=Concat('created_by__first_name', Value(' '), 'created_by__last_name')).filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(created_by__username__icontains=search, annonymous=False) |
                Q(full_name__icontains=search, annonymous=False)
            ).distinct()

        if year_query or major_query or specialization_query:
            if year_query:
                posts_list = posts_list.filter(years__in=year_query).distinct()
            if major_query:
                posts_list = posts_list.filter(majors__in=major_query).distinct()
            if specialization_query:
                posts_list = posts_list.filter(specializations__in=specialization_query).distinct()

        paginator = Paginator(posts_list, 5)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        majors = Major.objects.all()
        specializations = Specialization.objects.all()

        return render(request, 'all_post.html', {
            'user': user,
            'user_logged': user_logged,
            'posts': posts,
            'years': range(1, 5),
            'majors': majors,
            'specializations': specializations,
            'year_query': year_query,
            'major_query': major_query,
            'specialization_query': specialization_query
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
        user_logged = User.objects.get(pk=user_id)
        user = User.objects.get(pk=user_id)

        create_form = CreatePostForm(user=user)
        return render(request, 'create_post.html', {
            'user': user,
            'user_logged': user_logged,
            'create_form': create_form
        })
    
    def post(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)

        create_form = CreatePostForm(request.POST, request.FILES, user=user)

        if create_form.is_valid():
            post = create_form.save(commit=False)
            post.created_by = user

            if user.role.id != 3:  # Student
                post.status = 'approved'

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
        user_id = request.session.get('user_id')
        user_logged = User.objects.get(pk=user_id)
        user = User.objects.get(username=username)
        print("User Role:", user.role)
        if user.role.name == 'Student':
            academic_info = AcademicInfo.objects.get(user=user)

        if user == user_logged or user_logged.role.id == 1:
            user_posts = Post.objects.filter(created_by=user).prefetch_related('files').order_by('-created_at')
        else:
            user_posts = Post.objects.filter(created_by=user, annonymous=False).prefetch_related('files').order_by('-created_at')

        
        can_edit = False
        if user.id == request.session.get('user_id'):
            can_edit = True

        stats = {
            'total': user_posts.count(),
            'pending': user_posts.filter(status='pending').count(),
            'approved': user_posts.filter(status='approved').count(),
            'rejected': user_posts.filter(status='rejected').count()
        }

        context = {
            'user_logged': user_logged,
            'user': user,
            'posts': user_posts,
            'can_edit': can_edit,
            'stats': stats
        }

        if user.role.name == 'Student':
            context['academic_info'] = academic_info
        return render(request, 'profile.html', context)

class TestView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        posts = Post.objects.prefetch_related('files').all().order_by('-created_at')
        return render(request, 'test.html', {
            'user': user,
            'posts': posts
        })
    

class PostCommentView(APIView):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)

        comments = Comment.objects.filter(post=post).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response({
            "success": True,
            "post_title": post.title,
            "comments": serializer.data
        })
    
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)

        user_id = request.session.get("user_id")
        user = User.objects.get(pk=user_id)

        comment = Comment.objects.create(
            post=post,
            user=user,
            content=request.data.get("content", "")
        )

        serializer = CommentSerializer(comment)
        return Response({"success": True, "comment": serializer.data}, status=201)


class ToggleLikeView(APIView):
    def post(self, request, post_id):
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)

        if user in post.liked_by.all():
            post.liked_by.remove(user)
            liked = False
        else:
            post.liked_by.add(user)
            liked = True

        return Response({'success': True, 'liked': liked, 'count': post.liked_by.count()})


class DeletePostView(APIView):
    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        post.delete()
        
        return Response({'success': True})
    

class EditProfileView(View):
    def get(self, request, username):
        user_id = request.session.get('user_id')
        user_logged = User.objects.get(username=username)

        user_form = UserForm(instance=user_logged)
        academic_form = AcademicInfoForm(instance=user_logged.academic_info)

        context = {
            'user_logged': user_logged,
            'user_form': user_form,
            'academic_form': academic_form
        }
        return render(request, 'edit_profile.html', context)
    
    def post(self, request, username):
        user_id = request.session.get('user_id')
        user_logged = User.objects.get(username=username)

        user_form = UserForm(request.POST, request.FILES, instance=user_logged)
        academic_form = AcademicInfoForm(request.POST, instance=user_logged.academic_info)

        if user_form.is_valid() and academic_form.is_valid():
            user_form.save()
            academic_form.save()
            
            return redirect("profile_view", username=username)

        context = {
            'user_logged': user_logged,
            'user_form': user_form,
            'academic_form': academic_form
        }
        return render(request, 'edit_profile.html', context)