from django import forms
from django.core.exceptions import ValidationError
from .models import ReallyUser, Comment, Post


class RegistrationForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)
    biography = forms.CharField(label='Биография', required=False)
    password1 = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                'Пароли не совпадают.', code='password_mismatch')}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = ReallyUser
        fields = ('username', 'password1', 'password2', 'avatar', 'biography')


class ChangeUserInfoForm(forms.ModelForm):
    biography = forms.CharField(label='Биография', required=False)
    avatar = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = ReallyUser
        fields = ('username', 'biography', 'avatar')


class CommentForm(forms.Form):
    description = forms.CharField(required=True, label="Комментарий")

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get('description')

        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text',)

