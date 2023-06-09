from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'body', 'likes_count','created_by', 'created_at_formatted']
        # read_only_fields = ['id', 'created_at', 'created_by']