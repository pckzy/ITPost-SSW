from django.contrib.auth.models import AbstractUser
from django.db import models

    
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # can_post_without_approval = models.BooleanField(default=False)
    # can_delete_others_posts = models.BooleanField(default=False)
    # can_approve_posts = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.username}) - {self.first_name} {self.last_name}"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_user_detail(self):
        return f"{self.role.name} - ({self.academic_info.major.code})"


class Major(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100,)

    def __str__(self):
        return self.code


class Specialization(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE, related_name='specializations')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"


class AcademicInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='academic_info')
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    year = models.PositiveIntegerField(choices=[(i, f'ปี {i}') for i in range(1, 5)])

    def __str__(self):
        spec = self.specialization.name if self.specialization else "ไม่มีแขนง"
        return f"{self.user.username} - {self.major.name} - {spec} (Year {self.year})"


class PostType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    post_type = models.ForeignKey(PostType, on_delete=models.SET_NULL, null=True)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    years = models.ManyToManyField('YearOption', blank=True)
    majors = models.ManyToManyField(Major, blank=True)
    specializations = models.ManyToManyField(Specialization, blank=True)

    annonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def like_count(self):
            return self.liked_by.count()
    

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name



class YearOption(models.Model):
    year = models.PositiveIntegerField(choices=[(i, f'ปี {i}') for i in range(1, 5)], unique=True)

    def __str__(self):
        return f"ปี {self.year}"


