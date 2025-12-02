from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register_user, name='register'),
    path('login', views.TheLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/delete', views.user_delete_view, name='user-delete'),
    path('profile/change', views.user_change_view, name='user-change'),
    path('profile/change-password', views.PasswordChangeView.as_view(), name='password-change')
]