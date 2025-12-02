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
    path('profile/change-password', views.ChangingPasswordView.as_view(), name='password-change'),
    path('post/<int:pk>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('post/<int:pk>/toggle_like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/delete', views.post_delete_view, name='delete-post'),
    path('post/<int:pk>/edit', views.post_change_view, name='edit-post'),
    path('/create', views.PostCreate.as_view(), name='create')
]