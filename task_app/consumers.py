import json
from .mongo_client import Repo
from .models import TaskModel
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer




class ChatConsumer(AsyncWebsocketConsumer):
    count = 0

    # Connection to socket channel
    async def connect(self):
        print(self.scope['url_route']['kwargs']['room_name'],'\n\nSCOPE')
        self.room_name = "chat22"
        self.room_group_name = "chat_group22"
        self.user = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        ChatConsumer.count += 1
        await self.accept()
        comment = Repo.find_all("comments")
        await self.send(text_data=json.dumps({
            "connection": "Created",
            "data": json.loads(comment)
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # echo to client
        if text_data_json.get("comment", False):
            Repo.put("comments", {
                "comment": text_data_json.get("comment")
            })
            await self.send(text_data=json.dumps({
                "msg": "Comment created"
            }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        "comment": text_data_json.get("comment")
                    }
                }
            )
        elif text_data_json.get("delete", False):
            if text_data_json["delete"] == "all":
                if Repo.delete("comments"):
                    await self.send(text_data=json.dumps({
                        "msg": "Successfuly deleted"
                    }))

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                "delete": True
                            }
                        }
                    )


        # Leave Websocket group

    async def disconnect(self, close_code):
        # Leave room group
        ChatConsumer.count -= 1
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))



class MyConsumer(AsyncWebsocketConsumer):
    count = 0

    # Connection to socket channel
    async def connect(self):
        print(self.scope['url_route']['kwargs']['room_name'],'\n\nSCOPE')
        self.room_name = "chat22"
        self.room_group_name = "chat_group22"
        self.user = self.scope['user']
        print(self.user,'\n\nUSERR')

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        ChatConsumer.count += 1
        await self.accept()
        comment = Repo.find_all("messages")
        comment1 = Repo.find_user('messages','narmin')
        for doc in comment1:
            print(doc,'\n\nCOMMNETS')
        await self.send(text_data=json.dumps({
            "connection": "Created",
            "data": json.loads(comment)
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # echo to client
        if text_data_json.get("comment", False):
            Repo.put("messages", {
                "comment": text_data_json.get("comment"),
                "user": self.user.username,
            })
            await self.send(text_data=json.dumps({
                "msg": "Comment created"
            }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        "comment": text_data_json.get("comment")
                    }
                }
            )
        elif text_data_json.get("delete", False):
            if text_data_json["delete"] == "all":
                if Repo.delete("messages"):
                    await self.send(text_data=json.dumps({
                        "msg": "Successfuly deleted"
                    }))

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                "delete": True
                            }
                        }
                    )


        # Leave Websocket group

    async def disconnect(self, close_code):
        # Leave room group
        ChatConsumer.count -= 1
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))




class NotificationConsumer(AsyncWebsocketConsumer):
    count = 0

    # Connection to socket channel
    @database_sync_to_async
    def get_username(self,id):
        return User.objects.filter(id=id).first().username

    @database_sync_to_async
    def get_task(self, id):
        return TaskModel.objects.filter(id=id).first().name

    async def connect(self):
        # print(self.scope['url_route']['kwargs']['room_name'],'\n\nSCOPE')
        self.room_name = f"notification{self.scope['url_route']['kwargs']['from_user']}"
        self.room_group_name = f"notification{self.scope['url_route']['kwargs']['from_user']}"
        self.user = self.scope['user']
        print('user\n\n',self.user.username)
        print('channels\n\n',self.channel_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        comment = Repo.find_all(f"notifications{self.user.username}")
        # Repo.delete(f"notifications{self.user.username}")

        # print(len(json.loads(comment)),'cOMMENT\n\n')
        # comment1 = Repo.find_user('messages','narmin')

        await self.send(text_data=json.dumps({
            "connection": "Created",
            "data": json.loads(comment)
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        channel_layer = get_channel_layer()

        # echo to client
        # print('RECEIVEEE\n\n')
        if text_data_json.get("from-user", False):
            from_id = text_data_json.get("from-user")
            to_id = text_data_json.get("to-user")
            task_id = text_data_json.get("task-id")

            from_user = await self.get_username(int(from_id))
            to_user = await self.get_username(int(to_id))
            mytask = await self.get_task(int(task_id))

            # print("YESSSS\n\n",from_user,to_user,mytask)



            Repo.put(f"notifications{to_user}", {
                "fromuser": f"{from_user}",
                'touser' : f"{to_user}",
                "task": f"{mytask}",
                'id' : task_id
            })
            await self.send(text_data=json.dumps({
                "msg": "Comment created"
            }))

            await self.channel_layer.group_send(
                f"notification{to_id}",
                {
                    'type': 'chat_message',
                    'message': {
                        "fromuser": f'{from_user}',
                        "task" : f'{mytask}',
                        'touser': f"{to_user}",
                        "count" : len(json.loads(Repo.find_all(f"notifications{to_user}"))),
                        'id' : task_id
                    }
                }
            )


        elif text_data_json.get("delete", False):
            if text_data_json["delete"] == "all":
                if Repo.delete("messages"):
                    await self.send(text_data=json.dumps({
                        "msg": "Successfuly deleted"
                    }))

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                "delete": True
                            }
                        }
                    )


        # Leave Websocket group

    async def disconnect(self, close_code):
        # Leave room group
        ChatConsumer.count -= 1
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print(message,'MESSAGEEEE')
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))


class CommentConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def get_username(self, id):
        return User.objects.filter(id=id).first().username

    async def connect(self):
        # print(self.scope['url_route']['kwargs']['room_name'],'\n\nSCOPE')
        self.room_name = f"comments{self.scope['url_route']['kwargs']['from_user']}{self.scope['url_route']['kwargs']['to_user']}{self.scope['url_route']['kwargs']['task_id']}"
        self.room_group_name = f"comments{self.scope['url_route']['kwargs']['from_user']}{self.scope['url_route']['kwargs']['to_user']}{self.scope['url_route']['kwargs']['task_id']}"
        self.user = self.scope['user']
        print('user\n\n',self.user.username)
        print('channels\n\n',self.room_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        comment = Repo.find_all(f"{self.room_name}")
        # Repo.delete(f"{self.room_name}")

        print(json.loads(comment),'cOMMENT\n\n')
        # comment1 = Repo.find_user('messages','narmin')

        await self.send(text_data=json.dumps({
            "connection": "Created",
            "data": json.loads(comment)
        }))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    # "connection": ChatConsumer.count
                }
            }
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        channel_layer = get_channel_layer()

        # echo to client
        # print('RECEIVEEE\n\n')
        if text_data_json.get("from-user", False):
            from_id = text_data_json.get("from-user")
            to_id = text_data_json.get("to-user")
            comment = text_data_json.get("comment")

            from_user = await self.get_username(int(from_id))
            to_user = await self.get_username(int(to_id))

            # print("YESSSS\n\n",from_user,to_user,mytask)



            Repo.put(f"{self.room_name}", {
                "fromuser": f"{from_user}",
                "touser": f"{to_user}",
                'comment' : comment
            })
            print("PUTTTTT")
            await self.send(text_data=json.dumps({
                "msg": "Comment created"
            }))

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        "fromuser": f"{from_user}",
                        "touser": f"{to_user}",
                        'comment': comment
                    }
                }
            )


        elif text_data_json.get("delete", False):
            if text_data_json["delete"] == "all":
                if Repo.delete("messages"):
                    await self.send(text_data=json.dumps({
                        "msg": "Successfuly deleted"
                    }))

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': {
                                "delete": True
                            }
                        }
                    )


        # Leave Websocket group

    async def disconnect(self, close_code):
        # Leave room group
        ChatConsumer.count -= 1
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    "connection": ChatConsumer.count
                }
            }
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print(message,'MESSAGEEEE')
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))