from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from .models import Post, Like, Comment, Trend
from .forms import PostForm
from .serializers import PostDetailSerializer, PostSerializer, CommentSerializer, TrendSerializer


@api_view(['GET'])
def post_list(request):

    # the feed shows posts from the user and their friends
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#'+trend)
    serializer = PostSerializer(posts, many=True)
    return JsonResponse({'data': serializer.data}, safe=False)


@api_view(['GET'])
def post_detail(request, pk):

    # pk is for the specific post
    post = Post.objects.get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data,
    })


@api_view(['GET'])
def post_list_profile(request):
    id = request.GET.get('id')

    user = User.objects.get(pk=id)

    posts = Post.objects.filter(created_by=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
    },
        safe=False,
    )


@api_view(['POST'])
def post_create(request):
    data = request.data
    print(data)
    form = PostForm(data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': form.errors}, status=400)


@api_view(['POST'])
def post_like(request, pk):
    if not post.likes.filter(created_by=request.user).exists():
        like = Like.objects.create(created_by=request.user)
        post = Post.objects.get(pk=pk)
        post.likes_count += 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'Like created'}, status=201)

    return JsonResponse({'message': 'Like already exists'}, status=400)


@api_view(['POST'])
def post_create_comment(request, pk):
    post = Post.objects.get(pk=pk)
    comment = Comment.objects.create(
        created_by=request.user, body=request.data['body'])
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    return JsonResponse(CommentSerializer(comment).data, safe=False, status=201)


@api_view(['GET'])
def get_trends(request):
    trends = Trend.objects.all()
    serializer = TrendSerializer(trends, many=True)
    return JsonResponse({'data': serializer.data}, safe=False)
