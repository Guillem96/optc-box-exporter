import io
import json
import glob
import base64
from pathlib import Path
from typing import Union
import tqdm.auto as tqdm

import cv2
import numpy as np
from PIL import Image

import click

import optcbx


@click.command()
@click.argument('data-pattern')
def main(data_pattern: str):
    """Labels new images with th gradient based approach"""
    labelme_base_dict = {"version": "4.5.6", "flags": {}}

    fnames = glob.glob(data_pattern)

    for f in tqdm.tqdm(fnames):
        f = Path(f)
        annotation_path = f.parent / (f.stem + '.json')
        if annotation_path.exists():
            continue

        im_metadata = _process_image(f)
        annotation = dict(**im_metadata, **labelme_base_dict)
        json.dump(annotation, annotation_path.open('w'))


def _process_image(im_path: Union[Path, str]) -> dict:
    im_path = Path(im_path)
    im = cv2.imread(str(im_path))
    _, rects = optcbx.detect_characters(im, 64, return_rectangles=True)
    rects[..., 2] = rects[..., 0] + rects[..., 2]
    rects[..., 3] = rects[..., 1] + rects[..., 3]

    im_metadata = {
        "imageHeight": im.shape[0],
        "imageWidth": im.shape[1],
        "imageData": _img_to_b64(im),
        "imagePath": f"{im_path.stem}{im_path.suffix}",
        "shapes": []
    }

    for r in rects.tolist():
        im_metadata['shapes'].append({
            "label": "character",
            "points": [r[:2], r[2:]],
            "group_id": None,
            "shape_type": "rectangle",
            "flags": {}
        })

    return im_metadata


def _img_to_b64(im: np.ndarray) -> str:
    im = Image.fromarray(im[..., ::-1])
    buffered = io.BytesIO()
    im.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


if __name__ == "__main__":
    main()
