import json, time
from valve.source.a2s import ServerQuerier

from typing import TYPE_CHECKING
if TYPE_CHECKING: from mqtt import MQTTClient

class SourceRCON:
    rcon_address: str
    rcon_password: str
    mqtt_client: MQTTClient
    server_info: dict = {}
    def __init__(self, rcon_address, rcon_password, mqtt_client: MQTTClient):
        self.rcon_address = rcon_address
        self.rcon_password = rcon_password
        self.mqtt_client = mqtt_client
        try: self.rcon_querier = ServerQuerier(self.rcon_address, timeout=5.0)
        except Exception as e:
            print(f"Failed to connect to RCON server: {e}")


    def _get_server_info(self):
        info = self.rcon_querier.info()
        return {
            "server_name": info["server_name"],
            "map": info["map"],
            "num_players": info["player_count"],
            "max_players": info["max_players"],
            "game_mode": info["folder"],
            "platform": str(info["platform"]),
            "server_type": str(info["server_type"])
        }

    def publish_server_info(self):
        if self.server_info:
            json_string = json.dumps(self.server_info)
            self.mqtt_client.publish("source_server_info", json_string)

    def start(self):
        self.mqtt_client.subscribe("source_server_info")
        
        # Periodically update server info
        while True:
            self.update_and_publish_server_info()
            time.sleep(60)  # Update every minute

    def update_and_publish_server_info(self):
        if self.rcon_querier:
            try:
                self.server_info = self._get_server_info()
                json_string = json.dumps(self.server_info)
                self.mqtt_client.publish("source_server_info", json_string)
                print("Server info published")
            except Exception as e:
                print(f"Error updating server info: {e}")

    def close(self):
        if self.rcon_querier:
            self.rcon_querier.close()
