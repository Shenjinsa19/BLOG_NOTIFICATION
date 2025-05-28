from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='blogs/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blogs/logout.html'), name='logout'),
    path('post/', views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
    path('register/', views.register, name='register'),


]
