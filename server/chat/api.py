from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User

from .models import Conversation, ConversationMessage
from .serializers import ConversationSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(
        users__in=list([request.user])
    )

    return JsonResponse(
        ConversationSerializer(conversations, many=True).data,
        safe=False
    )


@api_view(['GET'])
def conversation_get_or_create(request, pk):
    user = User.objects.get(pk=pk)

    conversations = Conversation.objects.filter(
        users__in=list([request.user])).filter(users__in=list([user]))

    if conversations.exists():
        conversation = conversation.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(user, request.user)
        conversation.save()

    return JsonResponse(
        ConversationSerializer(conversation).data,
        safe=False
    )


@api_view(['GET'])
def conversation_detail(request, conversation_id):
    conversation = Conversation.objects.filter(
        users__in=list([request.user])).get(pk=conversation_id)

    return JsonResponse(
        ConversationDetailSerializer(conversation).data,
        safe=False
    )


@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(
        users__in=list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user
            break

    conversation_message = ConversationMessage.objects.create(
        conversation=conversation,
        body=request.data['body'],
        created_by=request.user,
        sent_to=sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)
    return JsonResponse(serializer.data, safe=False)
