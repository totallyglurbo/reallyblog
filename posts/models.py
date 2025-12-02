from django.db import models
from django.contrib.auth.models import AbstractUser


class ReallyUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True,
                               verbose_name='Аватар', default='avatars/image.jpg')

    class Meta(AbstractUser.Meta):
        pass

# Create your models here.
