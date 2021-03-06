import uuid
from unittest import skip
from unittest.mock import Mock, call, patch

from django.forms import model_to_dict
from django.test import TestCase
from django.utils import timezone

from alarm.communication.out_alarm import NotifyAlarmStatus
from alarm.factories import AlarmStatusFactory
from camera.factories import CameraROIFactoryConf, CameraROIFactory, CameraRectangleROIFactory
from alarm.models import AlarmStatus
from camera.models import CameraMotionDetected
from devices.models import Device


class NotifyAlarmStatusTestCase(TestCase):
    def setUp(self) -> None:
        self.alarm_status: AlarmStatus = AlarmStatusFactory()
        self.device: Device = self.alarm_status.device

        self.roi = CameraROIFactory(device=self.device)

        self.roi1 = CameraRectangleROIFactory(camera_roi=self.roi)
        self.roi2 = CameraRectangleROIFactory(camera_roi=self.roi)

        self.alarm_messaging_mock = Mock()

    def test_publish_false(self):
        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_status_changed(self.device.id, False)

        self.alarm_messaging_mock.publish_alarm_status.assert_called_once()

        expected_calls = [call(self.device.device_id, False, None)]
        self.alarm_messaging_mock.publish_alarm_status.assert_has_calls(expected_calls)

    def test_no_publish_motion_being(self):
        event_ref = str(uuid.uuid4())

        CameraMotionDetected.objects.create(event_ref=event_ref, motion_started_at=timezone.now(), device=self.device)

        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_status_changed(self.device.id, False)

        self.alarm_messaging_mock.publish_alarm_status.assert_not_called()

    def test_force_publish_motion_being(self):
        event_ref = str(uuid.uuid4())

        CameraMotionDetected.objects.create(event_ref=event_ref, motion_started_at=timezone.now(), device=self.device)

        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_status_changed(self.device.id, False, force=True)

        self.alarm_messaging_mock.publish_alarm_status.assert_called_once_with(self.device.device_id, False, None)

    def test_publish_false_motion_ended(self):
        event_ref = str(uuid.uuid4())

        CameraMotionDetected.objects.create(
            event_ref=event_ref,
            motion_started_at=timezone.now(),
            motion_ended_at=timezone.now(),
            device=self.device)

        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_status_changed(self.device.id, False)

        expected_calls = [call(self.device.device_id, False, None)]
        self.alarm_messaging_mock.publish_alarm_status.assert_has_calls(expected_calls)

    def test_publish_false_last_motion_being_done(self):
        """
            We have a motion unfinished (something went wrong...)
            But after that, we have a done motion (motion then no more motion).
            It should turn off the service.
        """
        CameraMotionDetected.objects.create(
            event_ref=str(uuid.uuid4()),
            motion_started_at=timezone.now(),
            device=self.device)

        CameraMotionDetected.objects.create(
            event_ref=str(uuid.uuid4()),
            motion_started_at=timezone.now(),
            motion_ended_at=timezone.now(),
            device=self.device)

        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_status_changed(self.device.id, False)

        expected_calls = [call(self.device.device_id, False, None)]
        self.alarm_messaging_mock.publish_alarm_status.assert_has_calls(expected_calls)

    def test_publish_true_with_roi(self):
        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_status_changed(self.device.id, True)

        self.alarm_messaging_mock.publish_alarm_status.assert_called_once()

        payload = {
            'rois': {
                'definition_width': CameraROIFactoryConf.default_image_width,
                'definition_height': CameraROIFactoryConf.default_image_height,
                'rectangles': [model_to_dict(self.roi1), model_to_dict(self.roi2)]
            }
        }

        expected_calls = [call(self.device.device_id, True, payload)]
        self.alarm_messaging_mock.publish_alarm_status.assert_has_calls(expected_calls)

    def test_publish_roi_changed_false(self):
        self.alarm_status.running = False
        self.alarm_status.save()

        fake_roi = [{}, {}]
        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_roi_changed(self.device.id, self.roi, fake_roi)

        self.alarm_messaging_mock.publish_alarm_status.assert_not_called()

    def test_publish_roi_changed_true_with_roi(self):
        self.alarm_status.running = True
        self.alarm_status.save()

        fake_roi = [self.roi1, self.roi2]
        notify = NotifyAlarmStatus(self.alarm_messaging_mock)
        notify.publish_roi_changed(self.device.id, self.roi, fake_roi)

        self.alarm_messaging_mock.publish_alarm_status.assert_called_once()

        payload = {
            'rois': {
                'definition_width': CameraROIFactoryConf.default_image_width,
                'definition_height': CameraROIFactoryConf.default_image_height,
                'rectangles': [self.roi1, self.roi2]
            }
        }

        expected_calls = [call(self.device.device_id, True, payload)]
        self.alarm_messaging_mock.publish_alarm_status.assert_has_calls(expected_calls)


class NotifyAlarmStatusCalledTestCase(TestCase):
    def setUp(self) -> None:
        self.alarm_status: AlarmStatus = AlarmStatusFactory()

    @skip
    def test_notify_when_status_change(self):
        with patch.object(NotifyAlarmStatus, 'publish_status_changed', return_value=None) as mock:
            self.alarm_status.running = False
            self.alarm_status.save()

            expected_call = [call(self.alarm_status.device.pk, False)]
            mock.assert_called_once()
            mock.assert_has_calls(expected_call)

            mock.reset_mock()

            self.alarm_status.running = True
            self.alarm_status.save()

            expected_call = [call(self.alarm_status.device.pk, True)]
            mock.assert_called_once()
            mock.assert_has_calls(expected_call)
