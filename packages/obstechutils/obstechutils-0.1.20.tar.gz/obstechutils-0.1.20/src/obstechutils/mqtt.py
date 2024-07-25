from __future__ import annotations

from .credentials import Credentials
from .dataclasses import strictdataclass, Field, autoconverted 
from .types import QOSType, PortType

import paho.mqtt.client as mqtt
from typing_extensions import Annotated
from pydantic import  PositiveInt
from pydantic.networks import IPvAnyAddress
import json
import yaml
import re
            
CALLBACK_NAMES = [
    'on_connect', 'on_connect_fail', 'on_disconnect',
    'on_subscribe', 'on_unsubscribe',
    'on_message', 'on_publish', 'on_log'
]

    
def mqtt_client_from_api_version(n):
    try:
        api = getattr(mqtt.CallbackAPIVersion, f"VERSION{n}")
    except:
        raise RuntimeError(f'No such MQTT callback API: {n}')
    return mqtt.Client(api) 

MQTTClientType = autoconverted(
    mqtt.Client,
    converter_function=mqtt_client_from_api_version
)

@strictdataclass
class MQTTClient:

    username: str
    password: str
    server: IPvAnyAddress
    topics: list[str] = Field(default_factory=lambda: [])
    port: PortType = 1883
    qos: QOSType = 2
    timeout: PositiveInt = 60
    default_publish_topic: str = ''
    client: MQTTClientType = 2

    @classmethod
    def from_credentials(
        cls, 
        user: str ='generic_obstech', 
        **kwargs
    ) -> MQTTClient:

        creds = Credentials.load('mqtt', user=user)
        return cls(**creds, **kwargs)

    def __post_init__(self):

        self.client.username_pw_set(self.username, password=self.password)

        for callback_name in CALLBACK_NAMES:
            if callback := getattr(self, callback_name, None):
                setattr(self.client, callback_name, callback)

    def loop_forever(self): self.client.loop_forever()

    def loop_start(self): self.client.loop_start()

    def loop_stop(self): self.client.loop_stop()

    def publish(self, topic: str = '', payload: object = '', **kwargs): 
        if topic == '':
            topic = self.default_publish_topic
        self.client.publish(topic=topic, payload=payload, **kwargs)
       
    def publish_json(self, topic: str = '', payload: object = '', **kwargs): 
        self.publish(topic, json.dumps(payload), **kwargs)
 
    def connect(self):

        server = str(self.server)
        self.client.connect(server, self.port, self.timeout)

    def disconnect(self):

        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc, prop):

        if rc != 0:
            msg = 'MQTT connection to {self.server}:{self.port} failed'
            raise ConnectionError(msg)

        topics = [(t, self.qos) for t in self.topics]
        self.client.subscribe(topics)
    
   

class MQTTConsole(MQTTClient):
    
    def on_message(self, client, userdata, message):

        topic = message.topic
        data = message.payload.decode()
        # data = re.sub('\\s', '', data)
        msg = f"{topic} {data}"
        msg = msg if len(msg) < 80 else f"{msg[:77]}..."

        print(msg)
    
def console_script():

    import argparse

    parser = argparse.ArgumentParser(
        description='Print MQTT messages to the console'
    )
    parser.add_argument(
        '--topics', nargs="+", default=['#'], metavar='TOPIC',
        help='MQTT topics to monitor.  By default, all.'
    )
    args = parser.parse_args()

    user = 'generic_obstech'
    console = MQTTConsole.from_credentials(user, topics=args.topics)
    console.connect()
    console.loop_forever()
