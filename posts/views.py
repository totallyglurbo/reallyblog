from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from .forms import RegistrationForm, ChangeUserInfoForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, Comment


def index(request):
    posts = Post.objects.all().order_by('-pub_date')[:50]
    paginator = Paginator(posts, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'posts': page.object_list, 'page': page}
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
    posts = Post.objects.filter(author=request.user).order_by('-pub_date')
    paginator = Paginator(posts, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        'posts': page.object_list,
        'user': request.user,
        'page': page
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


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data.get('description')
            Comment.objects.create(
                post=post,
                comment_text=comment_text if comment_text else '',
                commenter=request.user
            )
            return redirect('index')
        else:
            pass
    else:
        form = CommentForm()
    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'add_comment.html', context)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.commenter:
        return redirect('index')

    if request.method == 'POST':
        comment.delete()
        return redirect('index')

    return redirect('index')


@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.commenter:
        return redirect('index')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.comment_text = form.cleaned_data['description']
            comment.save()
            return redirect('index')
    else:
        form = CommentForm(initial={'description': comment.comment_text})

    context = {'form': form, 'comment': comment}
    return render(request, 'edit_comment.html', context)