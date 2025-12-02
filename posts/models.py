from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class ReallyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,
                               verbose_name='Аватар', default='avatars/image.png')
    biography = models.CharField(max_length=250, verbose_name="Биография", null=True)

    class Meta(AbstractUser.Meta):
        pass


class Post(models.Model):
    post_text = models.TextField(verbose_name="Текст поста")
    author = models.ForeignKey('ReallyUser', on_delete=models.CASCADE, verbose_name='Автор поста', null=True)
    pub_date = models.DateTimeField(default=datetime.now, verbose_name="Дата публикации")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.post_text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    comment_text = models.TextField(verbose_name="Текст комментария")
    post = models.ForeignKey('Post', on_delete=models.CASCADE,
                                      verbose_name="Комментарий к посту", blank=True, null=True)
    commenter = models.ForeignKey('ReallyUser', on_delete=models.CASCADE, verbose_name='Автор комментария', null=True)

    def __str__(self):
        return self.comment_text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
