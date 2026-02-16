# MQTT Broker setup using hbmqtt (for local use only)
from hbmqtt.broker import Broker
import asyncio

broker_config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883'
        }
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True
    }
}

async def start_broker():
    broker = Broker(broker_config)
    await broker.start()

if __name__ == '__main__':
    asyncio.run(start_broker())
