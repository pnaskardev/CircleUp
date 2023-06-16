from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Post, Comment, Trend


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count',
                  'created_by', 'created_at_formatted')
        # read_only_fields = ['id', 'created_at', 'created_by']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model: Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted')


class PostDetailSerializer(serializers.ModelSerializer):

    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'created_by',
                  'created_at_formatted', 'comments', 'comments_count')


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurences')
