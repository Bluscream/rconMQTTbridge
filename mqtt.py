import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker, port):
        self.broker = broker
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.connected = False

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        self.connected = True

    def _on_message(self, client, userdata, message):
        print(f"Received MQTT message: {message.payload.decode()}")

    def connect(self):
        self.client.connect(self.broker, port=self.port)
        self.client.loop_start()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
