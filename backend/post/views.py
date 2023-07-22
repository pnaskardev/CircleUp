from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from . models import Post
from . serializers import PostSerializer

from account.models import User
from account.serializers import UserSerializer


class Posts(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, id,*args, **kwargs):
        user=User.objects.get(pk=id)
        user_serializer = UserSerializer(user)
        data = Post.objects.all().filter(created_by_id=id)
        posts = PostSerializer(data, many=True)
        return JsonResponse({'posts': posts.data, 'user': user_serializer.data}, safe=False)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PostSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return JsonResponse(serializer.data)


@api_view(['GET'])
def feed(request):
    list = Post.objects.all()
    serializer = PostSerializer(list, many=True)
    return JsonResponse(serializer.data, safe=False)


