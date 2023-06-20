from django.db import models

import uuid
from django.db import models

from account.models import User
from django.utils.timesince import timesince

# THIS CONVERSATION MODEL IS MY ROOM


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def modified_at_formatted(self):
        return timesince(self.created_at)

    def get_friend_usernames(self, userId):
        """
        Retrieve the usernames of the friends in the conversation, excluding the current user.
        """
        """
        Retrieve the usernames of the friends in the conversation, excluding the current user.
        """
        friend_usernames = []
        for user in self.users.all():
            if user.id != userId:
                friend_usernames.append(user.username)
        return friend_usernames

# THIS CONVERSATION MESSAGE MODEL IS MY MESSAGES MODEL


class ConversationMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, related_name='messages', on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)

    def created_at_formatted(self):
        return timesince(self.created_at)
