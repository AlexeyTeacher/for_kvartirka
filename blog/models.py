from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    content = models.TextField(default="TEXT")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'id{self.pk} post: {self.content[:len(self.content) % 20]}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(default="TEXT")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='comment')

    def __str__(self):
        return f"id{self.pk} post:{self.post.pk}: {self.text[:len(self.text) % 20]}"