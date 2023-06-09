from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'created_at', 'modified_at']


class ConversationMessageSeriallizer(serializers.ModelSerializerSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ['id', 'body', 'sent_to',
                  'created_at_formatted', 'created_by']


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSeriallizer(read_only=True, many=True)

    class Meta:
        model = Conversation
        fields = ['id', 'users', 'modified_at_formatted', 'messages']
