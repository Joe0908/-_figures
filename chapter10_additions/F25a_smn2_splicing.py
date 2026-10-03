"""Publish the user-selected F25a PNG without changing its bytes or pixels.

The uploaded raster is the source of truth. This script copies the PNG;
it does not recreate editable vector art. Earlier versions are in Git history.
"""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image

HERE = Path(__file__).resolve().parent
EXPECTED_SHA256 = '5b65264374431ae3900f66f68093f0f4f3fd8d28932945cf66980835277f9d4c'


def build():
    source = HERE / 'assets/F25a_user_supplied.png'
    output = HERE / 'outputs/png/F25a_smn2_splicing.png'
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError('Source differs from the image selected by the user')
    with Image.open(source) as image:
        image.verify()
    with Image.open(source) as image:
        size, mode = list(image.size), image.mode
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, output)
    assert hashlib.sha256(output.read_bytes()).hexdigest() == digest
    manifest = {
        'id': 'F25a',
        'current_version': 'user_selected_raster_2026-10-03',
        'source': 'assets/F25a_user_supplied.png',
        'output': 'outputs/png/F25a_smn2_splicing.png',
        'sha256': digest,
        'pixels': size,
        'mode': mode,
        'byte_identical': True,
        'image_integrity_verified': True,
        'original_editable_source_available': False,
        'previous_generated_commit': 'b78e50e1cae8b5af5b15ba45f2c592fa8a30b84b',
        'notes': 'Original PNG copied without resampling or editing. Earlier vector exports belong to the previous diagram.'
    }
    dest = HERE / 'outputs/manifests/F25a_validation.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + chr(10))
    return manifest


if __name__ == '__main__':
    print(json.dumps(build(), ensure_ascii=False))
