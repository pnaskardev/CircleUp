from django.db import models
from django.utils.timesince import timesince
import uuid

from account.models import User


class Like(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by=models.ForeignKey(User,name="likes",on_delete=models.CASCADE,related_name='likes')
    created_at=models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body=models.TextField(blank=True,null=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)
        # return timesince(self.created_at)+' ago'

class PostAttachment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image=models.ImageField(upload_to='post_attachments')
    created_by=models.ForeignKey(User,related_name='post_attachments',on_delete=models.CASCADE)

class Post(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body=models.TextField(blank=True,null=True)
    attachments=models.ManyToManyField(PostAttachment,blank=True)
    
    #Likes
    likes=models.ManyToManyField(Like,blank=True)
    likes_count=models.IntegerField(default=0)
    
    # comments
    comments=models.ManyToManyField(Comment,blank=True)
    comments_count=models.IntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')

    class Meta:
        ordering=['-created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)
        # return timesince(self.created_at)+' ago'

