from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse, reverse_lazy

from .forms import RegistrationForm, ChangeUserInfoForm
from django.contrib.auth.decorators import login_required
from .models import Post


def index(request):
    posts = Post.objects.all()[:50]
    context = {'posts': posts}
    return render(request, 'index.html', context)


def register_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            print(form.errors)
            return render(request, 'register.html', {'form': form})
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


class TheLoginView(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def profile_view(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        'posts': posts,
        'user': request.user
    }
    return render(request, 'profile.html', context)


@login_required
def user_delete_view(request):
    user_to_delete = request.user
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect(reverse('index'))
    return render(request, 'delete_user.html', {'user_to_delete': user_to_delete})


@login_required
def user_change_view(request):
    if request.method == 'POST':
        form = ChangeUserInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))
        else:
            return render(request, 'change_user.html', {'form': form})
    else:
        form = ChangeUserInfoForm(instance=request.user)

    return render(request, 'change_user.html', {'form': form})


class ChangingPasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('profile')