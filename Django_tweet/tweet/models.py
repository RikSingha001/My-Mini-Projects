from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tweet(models.Model):
   user= models.ForeignKey(User,on_delete=models.CASCADE)
   text = models.TextField(max_length=280)
   photo = models.ImageField(upload_to='tweet_photos/',blank=True,null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
      return f'{self.user.username} - {self.text[:10]} ' 
class Chat(models.Model):
    users = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id}"

class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
