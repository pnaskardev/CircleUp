from rest_framework import serializers

from . import models
from account.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.Post
        fields = ['id', 'body', 'likes_count',
                  'created_by', 'created_at_formatted']

    def create(self, validated_data):
        user = self.context.get('request').user
        extra_data = {
            'created_by': user
        }
        validated_data.update(extra_data)
        print(validated_data)

        return super().create(validated_data)
