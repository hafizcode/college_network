from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('fetch-updates/', views.fetch_updates, name='fetch_updates'),
    path('manage/users/', views.user_list, name='user_list'),  # changed from admin/users/
    path('manage/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('manage/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
]
