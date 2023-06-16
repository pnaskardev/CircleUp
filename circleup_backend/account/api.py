from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignUpForm
from .models import FriendshipRequest
from .models import User
from .serializers import UserSerializer, FriendshipRequestSerializer

# authentication and permission classes are empty so that we
# we can acces this controller without being logged in


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    # validating incoming data
    form = SignUpForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2')
    })

    if form.is_valid():
        form.save()

        # SEND VERIFICATION EMAIL LATER!!

    else:
        message = form.errors

    # return JsonResponse({'status':message})
    return JsonResponse({'status': message, 'id': form.instance.id})


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
    })


@api_view(['POST'])
def send_friend_request(request):
    pk = request.GET.get('pk')
    print('send_friend_request:-', pk)
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(
        created_for=request.user).filter(created_by=user).exists()
    check2 = FriendshipRequest.objects.filter(
        created_for=user).filter(created_by=request.user).exists()

    if (not check1 and not check2):
        friendship_request = FriendshipRequest.objects.create(
            created_for=user, created_by=request.user)
        return JsonResponse({'status': 'friend ship request created'})

    return JsonResponse({'status': 'friendship request already exists'})


@api_view(['GET'])
def friends(request):
    pk = request.GET.get('pk')
    user = User.objects.get(pk=pk)
    requests = []

    # u=request.user
    # u.friends_count=1
    # u.save()

    # user.friends_count=1
    # user.save()

    if user == request.user:
        requests = FriendshipRequest.objects.filter(
            created_for=request.user, status=FriendshipRequest.SENT)

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': FriendshipRequestSerializer(requests, many=True).data
    }, safe=False)


@api_view(['POST'])
def handle_request(request):
    pk = request.data.get('pk')
    status = request.data.get('status')
    print('handle_request:-', pk, status)

    user = User.objects.get(pk=pk)

    friendship_request = FriendshipRequest.objects.filter(
        created_for=request.user).get(created_by=user)

    # friendship_request.status = status
    # friendship_request.save()

    if status == FriendshipRequest.ACCEPTED and friendship_request.status == FriendshipRequest.SENT:
        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()

        friendship_request.status = status
        friendship_request.save()

        request.user.friends.friends_count = user.friends.friends_count + 1
        request.user.save()
        return JsonResponse({'status': 'friendship request updated'})
    else:
        return JsonResponse({'status': 'friendship request already accepted'})


@api_view(['POST'])
def edit_profile(request):
    user=request.user
    email=request.data.get('email')


    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        user.email=email
        user.name=request.data.get('name')
        user.save()
        return JsonResponse({'message': 'profile updated'})