from typing import Callable
import datetime
import re
import io
import numpy as np
from PIL import Image
from camera.videostream import VideoStream
from tflite_runtime.interpreter import Interpreter


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='jpeg')
    imgByteArr = imgByteArr.getvalue()

    return imgByteArr


class DetectMotion():

    def __init__(self, presenceCallback: Callable[[bool, str], None], noMorePresenceCallback: Callable):
        # State
        self._last_time_people_detected = None

        self.args = {
            'model': 'tensorflow-object-detection/data/detect.tflite',
            'labels': 'tensorflow-object-detection/data/coco_labels.txt',
            'threshold': 0.5
        }

        self.labels = self._load_labels(self.args['labels'])
        self.interpreter = Interpreter(self.args['model'])
        self.interpreter.allocate_tensors()
        _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']

        self._presenceCallback = presenceCallback
        self._noMorePresenceCallback = noMorePresenceCallback
        self._run()

    def _load_labels(self, path):
        """Loads the labels file. Supports files with or without index numbers."""
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)

                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()

        return labels

    def _set_input_tensor(self, interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def _get_output_tensor(self, interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor

    def _detect_objects(self, interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self._set_input_tensor(interpreter, image)
        interpreter.invoke()

        # Get all output details
        boxes = self._get_output_tensor(interpreter, 0)
        classes = self._get_output_tensor(interpreter, 1)
        scores = self._get_output_tensor(interpreter, 2)
        count = int(self._get_output_tensor(interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }

                results.append(result)

        return results

    def _processFrame(self, stream):
        image = Image.fromarray(stream).convert('RGB').resize(
            (self.input_width, self.input_height), Image.ANTIALIAS)

        results = self._detect_objects(
            self.interpreter, image, self.args['threshold'])

        for obj in results:
            label = self.labels[obj['class_id']]
            score = obj['score']

            if label == 'person':
                print(f'we found {label} score={score}')
                if self._last_time_people_detected is None:
                    print('WE NOTIFY')
                    self._presenceCallback(image_to_byte_array(image))

                self._last_time_people_detected = datetime.datetime.now()

        time_lapsed = (self._last_time_people_detected is not None) and (
            datetime.datetime.now() - self._last_time_people_detected).seconds >= 5

        if time_lapsed:
            self._last_time_people_detected = None
            self._noMorePresenceCallback()

    def _run(self):
        CAMERA_WIDTH = 640
        CAMERA_HEIGHT = 480

        # TODO: see issue #78
        VideoStream(self._processFrame, resolution=(
            CAMERA_WIDTH, CAMERA_HEIGHT), framerate=1, usePiCamera=False)
