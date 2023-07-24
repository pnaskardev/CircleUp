from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.decorators import api_view


from . models import Post, Like
from . serializers import PostSerializer

from account.models import User
from account.serializers import UserSerializer


class Posts(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_ids = [request.user.id]

        for user in request.user.friends.all():
            user_ids.append(user.id)

        posts = Post.objects.filter(created_by__in=list(user_ids))
        serializer = PostSerializer(posts, many=True)
        # return super().list(request, *args, **kwargs)
        return JsonResponse(serializer.data, safe=False)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = PostSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return JsonResponse(serializer.data)


# @api_view(['GET'])
# def feed(request):
#     list = Post.objects.all()
#     serializer = PostSerializer(list, many=True)
#     return JsonResponse(serializer.data, safe=False)

class UserPosts(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def list(self, request, id, *args, **kwargs):
        user = User.objects.get(pk=id)
        user_serializer = UserSerializer(user)
        data = Post.objects.all().filter(created_by_id=id)
        posts = PostSerializer(data, many=True)
        return JsonResponse({'posts': posts.data, 'user': user_serializer.data}, safe=False)


# class LikeViewSet(generics.CreateAPIView):
#     queryset = Like.objects.all()
#     def create(self, request, pk, *args, **kwargs):
#         like=Like.objects.create(created_by=request.user)
        

#         return super().create(request, *args, **kwargs)

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})