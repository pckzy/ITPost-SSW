from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("logout/", views.LogoutView.as_view(), name="logout_view"),
    path("register/", views.RegisterView.as_view(), name="register_view"),
    path("create/", views.CreateView.as_view(), name="create_view"),
    # path("test/", views.TestView.as_view(), name="test_view"),
    path("", views.MainView.as_view(), name="main_view"),
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile_view"),
    path("comments/<int:post_id>/", views.PostCommentView.as_view(), name="post_comments"),
    path("comments/<int:post_id>/create/", views.PostCommentView.as_view(), name="comment_create"),
    path("post/<int:post_id>/like/", views.ToggleLikeView.as_view(), name="toggle_like"),
]