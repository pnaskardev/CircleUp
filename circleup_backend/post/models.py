from django.db import models
from django.utils.timesince import timesince
import uuid

from account.models import User

class PostAttachment(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image=models.ImageField(upload_to='post_attachments')
    created_by=models.ForeignKey(User,related_name='post_attachments',on_delete=models.CASCADE)

class Post(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body=models.TextField(blank=True,null=True)
    attachments=models.ManyToManyField(PostAttachment,blank=True)
    # likes
    # likes_count
    # comments

    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name='posts')

    class Meta:
        ordering=['-created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)
        # return timesince(self.created_at)+' ago'

