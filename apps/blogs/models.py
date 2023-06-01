from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from apps.products.models import Category


class Tag(models.Model):
    title = models.CharField(max_length=21)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    content = models.TextField()
    author_name = models.CharField(max_length=255)
    author_image = models.ImageField(upload_to='author')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

