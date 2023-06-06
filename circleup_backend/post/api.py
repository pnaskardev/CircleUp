from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes, permission_classes
from .models import Post
from .forms import PostForm
from .serializers import PostSerializer


@api_view(['GET'])
def post_list(request):
    posts=Post.objects.all()

    serializer=PostSerializer(posts,many=True)
    return JsonResponse({'data':serializer.data},safe=False)

@api_view(['POST'])
def post_create(request):
    data=request.data
    print(data)
    form=PostForm(data)
    if form.is_valid():
        post=form.save(commit=False)
        post.created_by=request.user
        post.save()

        serializer=PostSerializer(post)

        return JsonResponse(serializer.data,safe=False)
    else:
        return JsonResponse({'error':form.errors},status=400)
        
