from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # nickname
    pass


class Tag(models.Model):
    name = models.CharField(max_length=10)


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # likes = models.ManyToManyField(User, related_name='like_posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    time = models.DateTimeField(null=True, blank=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
