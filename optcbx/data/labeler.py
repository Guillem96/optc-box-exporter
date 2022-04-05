import base64
import glob
import io
import json
from pathlib import Path
from typing import Union

import click
import cv2
import numpy as np
import optcbx
import tqdm.auto as tqdm
from PIL import Image


@click.command()
@click.argument('data-pattern')
@click.option('--detection-approach',
              type=click.Choice(["smart", "gradient_based"]),
              default="smart")
def main(data_pattern: str, detection_approach: str) -> None:
    """Labels new images with th gradient based approach"""
    labelme_base_dict = {"version": "4.5.6", "flags": {}}

    fnames = glob.glob(data_pattern)

    for f in tqdm.tqdm(fnames):
        f = Path(f)
        annotation_path = f.parent / (f.stem + '.json')
        if annotation_path.exists():
            continue

        im_metadata = _process_image(f, detection_approach)
        annotation = dict(**im_metadata, **labelme_base_dict)
        json.dump(annotation, annotation_path.open('w'))


def _process_image(im_path: Union[Path, str], detection_approach: str) -> dict:
    im_path = Path(im_path)
    im = cv2.imread(str(im_path))
    _, rects = optcbx.detect_characters(im,
                                        64,
                                        return_rectangles=True,
                                        approach=detection_approach)

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
