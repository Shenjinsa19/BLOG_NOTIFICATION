from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return f"{self.title[:30]} by {self.author.username}"




class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'author')


