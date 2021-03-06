from hello_django.loggers import LOGGER
from utils.mqtt.mqtt_data import MqttTopicSubscriptionBoolean, MqttTopicFilterSubscription, MqttTopicSubscription, \
    MqttMessage, MqttTopicSubscriptionJson
from utils.mqtt import MQTT
import alarm.tasks as tasks
from alarm.tasks import camera_motion_picture, camera_motion_detected, process_video
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from utils.mqtt.mqtt_status_handler import OnConnectedHandler, OnStatus, OnConnectedHandlerLog
from .communication.on_connected_services import OnConnectedCameraHandler, OnConnectedSpeakerHandler
import os

DEVICE_ID = os.environ['DEVICE_ID']

def split_camera_topic(topic: str, is_event_ref = False):
    data = topic.split('/')

    r_data = {
        'type': data[0],
        'service': data[1],
        'device_id': data[2]
    }

    if is_event_ref:
        r_data['event_ref'] = data[3]

        if len(data) == 5:
            r_data['status'] = data[4]

    return r_data


def on_motion_camera(message: MqttMessage):
    topic = split_camera_topic(message.topic)
    payload = message.payload

    LOGGER.info(f'on_motion_camera payload={payload}')

    data = {
        'device_id': topic['device_id'],
        'event_ref': payload['event_ref'],
        'status': payload['status'],
        'seen_in': {},
    }

    if data['status'] is True:
        data['seen_in'] = payload['seen_in']

    if data['event_ref'] != '0':
        # 0 = initialization
        camera_motion_detected.apply_async(kwargs=data)


def on_motion_video(message: MqttMessage):
    topic = split_camera_topic(message.topic, True)
    LOGGER.info(f'on_motion_video: topic={topic} {message.topic}')

    data = {
        'device_id': topic['device_id'],
        'event_ref': topic['event_ref'],
    }

    if data['device_id'] == DEVICE_ID:
        video_path = f'videos/{data["event_ref"]}.h264'
        # The system has some latency to save the video,
        # so we add a little countdown so the video will more likely be available after x seconds.
        process_video.apply_async(kwargs={'video_path': video_path}, countdown=3)

def on_motion_picture(message: MqttMessage):
    topic = split_camera_topic(message.topic, True)

    event_ref = topic['event_ref']
    status = topic['status']

    bool_status = None
    if status == '0':
        bool_status = False
    elif status == '1':
        bool_status = True
    else:
        raise ValueError(f'Status {status} should be "0" or "1".')

    LOGGER.info(f'on_motion_picture even_ref={event_ref}')

    if event_ref == "0":
        # Initialization: no motion
        return

    file_name = f'{event_ref}.jpg'

    # Remember: image is bytearray
    image = message.payload

    """
    Warning: hacky thing.
    - We need to save the file here because we cannot send it to a Task (memory consumption!).
    - So we save manually the file to the disk at the right place for Django.
    - But we can't use model.file.save('name.jpg', content, True) because we do not have the model instance here this is the task job.
    - So we go with low-level API.
    - at the end, picture_path is an absolute path e.g: "/usr/src/app/media/1be409e1-7625-490a-9a8a-428ba4b8e88c.jpg"
    """
    filename = default_storage.save(file_name, ContentFile(image))
    picture_path = default_storage.path(filename)

    data = {
        'device_id': topic['device_id'],
        'picture_path': picture_path,
        'event_ref': event_ref,
        'status': bool_status,
    }

    tasks.camera_motion_picture.apply_async(kwargs=data)


def bind_on_connected(service_name: str, handler_instance: OnConnectedHandler) -> MqttTopicSubscriptionBoolean:
    on_status = OnStatus(handler_instance)

    return MqttTopicSubscriptionBoolean(f'connected/{service_name}/+', on_status.on_connected)


def register(mqtt: MQTT):
    speaker = bind_on_connected('speaker', OnConnectedSpeakerHandler(mqtt))
    camera = bind_on_connected('camera', OnConnectedCameraHandler(mqtt))

    object_detection = bind_on_connected('object_detection', OnConnectedHandlerLog(mqtt))

    mqtt.add_subscribe([
        MqttTopicFilterSubscription(
            topic='motion/#',
            qos=1,
            topics=[
                MqttTopicSubscriptionJson('motion/camera/+', on_motion_camera),
                MqttTopicSubscription('motion/picture/+/+/+', on_motion_picture),
                MqttTopicSubscription('motion/video/+/+', on_motion_video),
            ],
        ),
        camera,
        speaker,
        object_detection,
    ])
