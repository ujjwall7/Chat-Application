from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.group_name = f"room_{self.room_name}"
        print("===========Connect===========")
        print()
        print(f"{self.scope = }")  
        print(f"{self.group_name = }")  
        print(f"{self.scope['url_route'] = }")
        print(f"{self.scope['url_route']['kwargs'] = }")
        print(f"{self.scope['url_route']['kwargs']['room_code'] = }")
        print()
        print("===========Connect Ended===========")

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

        data = {'type' : 'connected'}

        self.send(text_data = json.dumps({
            'payload' : 'Connected'
        }))

    def receive(self, text_data):
        print(f"{text_data = }")
        print()
        data = json.loads(text_data)
        print(f"{data = }")

        payload = {
            'message' : data.get('message'),
            'sender' : data.get('sender'),
        }
        async_to_sync(self.channel_layer.group_send)(   
            f"room_{self.room_name}", {
                "type" : "send_message",
                "value" : json.dumps(payload)
            }
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )
        print(f"Client disconnected from room: {self.group_name}, Close code: {close_code}")

    def send_message(self, text_data):
        print(f"{text_data = }")
        print(f"{type(text_data) = }")

        data = text_data.get('value')

        print(f"{data = }")

        self.send(text_data = json.dumps({
            'payload' : data
        }))




