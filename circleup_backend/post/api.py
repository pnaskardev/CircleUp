from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all()  # change later to feed
    serializer = PostSerializer(posts, many=True)
    return JsonResponse({'data': serializer.data}, safe=False)


@api_view(['GET'])
def post_list_profile(request):
    id = request.GET.get('id')

    user = User.objects.get(pk=id)

    posts = Post.objects.filter(created_by=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)
    return JsonResponse({
            'posts':posts_serializer.data,
            'user':user_serializer.data,
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

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': form.errors}, status=400)
