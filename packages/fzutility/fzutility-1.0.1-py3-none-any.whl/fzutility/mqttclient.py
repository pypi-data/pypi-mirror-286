import inspect
import json
import os
import random
import time

import paho.mqtt.client as mqtt

from fzutility import logger


@logger.logger_decorator(level="INFO", save_path="logs")
class MqttClient:
    def __init__(
        self,
        id: str = "",
        pw: str = "",
        topic: str = None,  # destination : this topic is subscriber topic name
        qos: int = 0,
        host: str = "",
        port: int = 1883,
    ):
        self.sub_topic = topic
        self.qos = qos
        self.logger.info(f"{self.sub_topic}, {self.qos}")
        self.client = mqtt.Client()
        self.client.username_pw_set(id, pw)

        self.broker_ip = host
        self.broker_port = port

        self.listener = {}
        self.max_delay = 30
        self.initial_delay = 1.0
        self.factor = 2.7182818284590451
        self.jitter = 0.119626565582
        self.delay = self.initial_delay

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.connect(self.broker_ip, self.broker_port)
        self.messages = None

    def connect(self, ip, port):
        try:
            self.client.connect(ip, port, keepalive=60)
        except Exception as e:
            self.logger.error(f"{inspect.currentframe().f_code.co_name} - {e}")
            self.reconnect()

    def reconnect(self):
        while True:
            try:
                self.delay = self.delay * self.factor
                if self.delay > self.max_delay:
                    self.delay = self.initial_delay
                self.delay = random.normalvariate(
                    self.delay,
                    self.delay * self.jitter,
                )
                time.sleep(self.delay)
                self.client.reconnect()
                self.logger.warning("mqtt reconnect")
                break
            except Exception as e:
                self.logger.info(f"{inspect.currentframe().f_code.co_name} - {e}")

    def add_listener(self, func):
        self.listener.update({self.sub_topic: func})

    def remove_listener(self, topic):
        if topic in self.listener:
            del self.listener[topic]

    def on_connect(self, client, userdata, flags, return_code):
        if self.sub_topic is not None:
            self.client.subscribe(self.sub_topic, self.qos)
        self.logger.debug(f"Connected with result code: {str(return_code)}")

    def on_disconnect(self, client, userdata, reture_code):
        self.logger.debug(f"Disconnected with result code: {reture_code}")
        self.reconnect()

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.logger.debug(f"subscribed: {mid} - {granted_qos}")

    def on_message(self, client, userdata, msg):
        if msg.topic in self.listener:
            self.listener[msg.topic](json.loads(msg.payload.decode("utf-8")))

    def pub_message(self, topic, msg):
        try:
            self.client.loop_start()
            msg = json.dumps(msg, indent=4)
            if self.client.is_connected():
                if msg is not None:
                    self.client.publish(topic, msg)
                    self.logger.debug(f"{msg}")
                else:
                    self.logger.debug("pub data is None")
            else:
                self.reconnect()

        except Exception as e:
            self.logger.error(f"{inspect.currentframe().f_code.co_name} - {e}")

    def mqtt_callback(self, payload):
        try:
            if payload:
                self.messages = payload
            else:
                self.logger.error(f"fail : {payload}")
        except Exception as e:
            self.logger.error(f"{inspect.currentframe().f_code.co_name} - {e}")

    def sub_message(self):
        try:
            self.add_listener(self.mqtt_callback)
            self.client.loop_forever()
        except Exception as e:
            self.logger.error(f"{inspect.currentframe().f_code.co_name} - {e}")
