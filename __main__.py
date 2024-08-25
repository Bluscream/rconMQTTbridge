import config
from mqtt import MQTTClient
from rcon.source import SourceRCON

class RCONBridge:
    mqtt: MQTTClient = None
    rcon: list[SourceRCON] = []
    def __init__(self):
        try:
            self.mqtt = MQTTClient(config["mqtt"]["ip"], config["mqtt"]["port"], config["mqtt"]["pw"])

            for rcon in config["rcon"]:
                self.rcon.append(SourceRCON(rcon["ip"], rcon["port"], rcon["pw"], self.mqtt))
            
            for rcon in self.rcon:
                rcon.start()
                
            input("Press Enter to exit...")
            
        finally:
            if self.mqtt.connected:
                self.mqtt.stop()


if __name__ == "__main__":
    bridge = RCONBridge()