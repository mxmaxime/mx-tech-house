import struct

from mqtt.mqtt_client import MqttClient
from thread.thread_manager import ThreadManager
import logging
import json


class MqttStatusManageThread:
    """
    This class synchronise the alarm status with MQTT.
    If we receive a message to switch on/off the alarm, we're doing it here.
    """
    def __init__(self, logger: logging, device_id: str, service_name: str, mqtt_client: MqttClient, thread_manager: ThreadManager, status_json = False):
        self._logger = logger
        self._thread_manager = thread_manager
        self._service_name = service_name
        self._status_json = status_json

        mqtt_topic = f'status/{service_name}/{device_id}'

        mqtt_client.client.subscribe(mqtt_topic, qos=1)
        mqtt_client.client.message_callback_add(mqtt_topic, self._switch_on_or_off)

        # Will message has to be set before we connect.
        mqtt_client.client.will_set(f'connected/{service_name}/{device_id}', payload=struct.pack('?', False), qos=1, retain=True)
        mqtt_client.connect()

        mqtt_client.client.publish(f'connected/{service_name}/{device_id}', payload=struct.pack('?', True), qos=1, retain=True)

    def _switch_on_or_off(self, client, userdata, msg):
        message = msg.payload
        data = None

        # TODO: #102 handle errors! Don't let the software crashes.
        if self._status_json is True:
            message = json.loads(message)
            status = message['status']
            data = message['data']
        else:
            status = struct.unpack('?', message)[0]

        print(f'Receive status {status} for {self._service_name} with data {data}')

        if status:
            self._thread_manager.run(True, data=data)
        else:
            self._thread_manager.run(False)


def mqtt_status_manage_thread_factory(*args, **kwargs):
    return MqttStatusManageThread(logging, *args, **kwargs)

# WIP: work with TLS.
# os.environ['REQUESTS_CA_BUNDLE'] = "/usr/local/share/ca-certificates/ca.cert"
# os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(
#     '/etc/ssl/certs/',
#     'ca-certificates.crt')

# CA = "./ca.crt"
# CERT_FILE = "./test_client.crt"
# KEY_FILE = "./test_client.key"

# client.tls_set(ca_certs=CA, certfile=CERT_FILE,
#                 keyfile=KEY_FILE, tls_version=ssl.PROTOCOL_TLSv1_2)
# client.tls_insecure_set(True)
