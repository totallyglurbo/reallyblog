from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class ReallyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,
                               verbose_name='Аватар', default='avatars/image.jpg')
    biography = models.CharField(max_length=250, verbose_name="Биография", null=True)

    class Meta(AbstractUser.Meta):
        pass


class Post(models.Model):
    post_text = models.TextField(verbose_name="Текст поста")
    author = models.ForeignKey('ReallyUser', on_delete=models.CASCADE, verbose_name='Автор поста', null=True)
    pub_date = models.DateTimeField(default=datetime.now, verbose_name="Дата публикации")
    post_comments = models.ForeignKey('Comment', on_delete=models.CASCADE,
                                      verbose_name="Комментарии к посту", blank=True, null=True)

    def __str__(self):
        return self.post_text

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    comment_text = models.TextField(verbose_name="Текст комментария")

    def __str__(self):
        return self.comment_text
