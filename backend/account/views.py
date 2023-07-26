from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from . models import User, FriendshipRequest
from . serializers import UserSerializer, FriendshipRequestSerializer


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = []
    permission_classes = []
    http_method_names = ["post"]


# class FriendshipViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = FriendshipSerializer

#     def create(self, request, pk, *args, **kwargs):
#         received_user = User.objects.get(pk=pk)

#         friendship_request = FriendshipSerializer(
#             data=request.data, context={'created_by': request.user, 'created_for': received_user})

#         if friendship_request.is_valid(raise_exception=True):
#             friendship_request.save()
#             return JsonResponse({'message': 'friendship request created'})
#         return JsonResponse({'message': 'friendship request failed'})


@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(
        created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(
        created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        FriendshipRequest.objects.create(
            created_for=user, created_by=request.user)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []
    if user == request.user:
        requests = FriendshipRequest.objects.filter(
            created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data
    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(["POST"])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(
        created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count+1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count+1
    request_user.save()

    return JsonResponse({
        'message': 'friendship request updated'
    })
