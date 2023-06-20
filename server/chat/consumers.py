import json

from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import sync_to_async, async_to_sync

from chat.models import Conversation, ConversationMessage
from account.models import User


class ChatConsumer(WebsocketConsumer):

    # Utility functions
    @sync_to_async
    def save_message(self, message, name, sent_to, created_by):
        conversation = Conversation.objects.get(id=self.conversationId)
        conversation_message = ConversationMessage.objects.create(
            conversation=conversation,
            body=message,
            sent_to=sent_to,
            created_by=created_by
        )
        conversation_message.save()
        return conversation_message
    
    @sync_to_async
    def get_conversation(self):
        self.conversation = Conversation.objects.get(id=self.conversationId)

    async def notify_friend_join(self):
        friend_list = self.conversation.get_friend_username(self, self.user.id)
        # message = f"{} has joined the conversation"
        await self.send(text_data=json.dumps({
            'message': '__ has joined the chat'
        }))


    async def connect(self):
        self.conversationId = self.scope["url_route"]["kwargs"]["conversationId"]
        self.conversation_group_name = f'chat_{self.conversationId}'
        self.user = self.scope['user']

        # Join Conversation
        await self.get_conversation()
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )
        await self.accept()

        await self.channel_layer.group_send(
            self.conversation_group_name, {
                'type': 'notify_friend_join',
            }
        )

    #  Disconnect Web socket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )
        


    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        name = text_data_json['name']
        sent_to = self.scope['user']
        created_by = self.scope['user']

        # Save Message to Database
        conversation_message = await self.save_message(message, name, sent_to, created_by)

        # Retrieve friend usernames in the conversation
        friend_usernames = self.conversation.get_friend_usernames(userId=sent_to.id)


        # Send message to room group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'name': name,
                # Assuming you have this method in your model
                'created_at': conversation_message.created_at_formatted(),
                # Add the friend_usernames to the event data
                'friend_usernames': friend_usernames
            }
        )

    # Receive message from room group     
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'message': event['message'],
            'name': event['name'],
            'created_at': event['created_at'],
            'friend_usernames': event['friend_usernames']
        }))

   