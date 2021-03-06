from typing import Tuple

from utils.download import get_file


def download_model(model_name: str = 'archive.zip', cache_dir = '/usr/src/tf-models') -> Tuple[str, str]:
    url = 'http://storage.googleapis.com/download.tensorflow.org/models/tflite/coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip'
    model_archive_file_hash = 'a809cd290b4d6a2e8a9d5dad076e0bd695b8091974e0eed1052b480b2f21b6dc'
    label_file_hash = '93f235896748537fc71325a070ee32e9a0afda2481ceb943559325619763fa6d'

    archive = get_file(
        cache_dir=cache_dir,
        fname=model_name,
        origin=url,
        extract=True,
        file_hash=model_archive_file_hash)

    labels = get_file(
        cache_dir=cache_dir,
        fname='coco_labels.txt',
        origin='https://dl.google.com/coral/canned_models/coco_labels.txt',
        file_hash=label_file_hash
    )

    return f'{cache_dir}/detect.tflite', labels
