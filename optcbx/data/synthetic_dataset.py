import json
import shutil
import random
from pathlib import Path
from typing import List, Tuple

import click
import tqdm.auto as tqdm

import cv2
import numpy as np


@click.command()
@click.option('-i', '--input-path', required=True, 
              type=click.Path(exists=True, file_okay=False))
@click.option('-o', '--output', required=True, 
              type=click.Path(file_okay=False))
@click.option('--epochs', type=int, default=3)
@click.option('--mix-from', type=int, default=3)
@click.option('--min-portraits', type=int, default=2)
@click.option('--max-portraits', type=int, default=15)
def main(input_path: str, output: str, 
         epochs: int, mix_from: int, min_portraits: int, max_portraits: int):
    """Given ground truth annotations mixes a set of images to generate a 
    synthetic a dataset
    """
    base_path = Path(input_path)

    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    annotations_paths = base_path.glob('*.json')
    annotations_paths = list(annotations_paths)

    for epoch in range(epochs):
        for annotation_path in tqdm.tqdm(annotations_paths,
                                         desc=f'Epoch {epoch}'):
            mix_with = [random.choice(annotations_paths) for _ in range(mix_from)]
            mixers = _pick_mixers(base_path, 
                                  mix_with, 
                                  min_portraits, 
                                  max_portraits)
            res_im = _paste_mixers(base_path, annotation_path, mixers)
            annot = _override_image_data(annotation_path, res_im)

            out_im_path = f'{annotation_path.stem}_{epoch}.jpg'
            out_im_path = output_path / out_im_path

            dst_copy_annot = f'{annotation_path.stem}_{epoch}.json'
            dst_copy_annot = output_path / dst_copy_annot
 
            cv2.imwrite(str(out_im_path), res_im)
            json.dump(annot, dst_copy_annot.open('w'))


def _pick_mixers(base_path: Path, 
                 mix_with: List[Path], 
                 min_portraits: int, 
                 max_portratits: int) -> List[np.ndarray]:

    mix_rects = []
    mix_ims = []
    indices = []
    for i, mw in enumerate(mix_with):
        cur_mix_im, cur_mix_rects = _load_example(base_path, mw)
        mix_rects.append(cur_mix_rects)
        mix_ims.append(cur_mix_im)
        indices.extend([i] * cur_mix_rects.shape[0])

    mix_rects = np.concatenate(mix_rects, axis=0)
    indices = np.array(indices)

    n = random.randint(min_portraits, 
                       min(max_portratits, indices.shape[0]))
    random_rects_idx = _randint(0, mix_rects.shape[0], size=(n,))

    selected_rects = mix_rects[random_rects_idx].astype('int32')
    selected_indices = indices[random_rects_idx]
    selected_ims = [mix_ims[i] for i in selected_indices]
    return [im[r[1]: r[3], r[0]: r[2]] 
            for im, r in zip(selected_ims, selected_rects)]


def _override_image_data(annotation_path: Path, new_im: np.ndarray) -> dict:
    from optcbx.labeler import _img_to_b64
    annot = json.load(annotation_path.open())
    annot['imageData'] = _img_to_b64(new_im)
    return annot


def _paste_mixers(base_path: Path,
                  annotation_path: Path, 
                  mixers: List[np.ndarray]) -> np.ndarray:
    im, rects = _load_example(base_path, annotation_path)
    selected_rects_idx = _randint(0, rects.shape[0], 
                                  size=(min(len(mixers), rects.shape[0]),))
    selected_rects = rects[selected_rects_idx].astype('int32')

    for r, m in zip(selected_rects, mixers):
        w = r[2] - r[0]
        h = r[3] - r[1]

        m = cv2.resize(m, (w, h))
        im[r[1]: r[3], r[0]: r[2]] = m

    return im


def _load_example(base_path: Path,
                  annotation_path: Path) -> Tuple[np.ndarray, np.ndarray]:
    annotation = json.load(annotation_path.open())
    
    im_path = base_path / annotation['imagePath']
    im = cv2.imread(str(im_path))

    rects = [sum(a['points'], []) for a in annotation['shapes']]
    rects = np.array(rects)

    return im, rects

def _randint(min_val: int, max_val: int, size: Tuple[int, ...]) -> np.ndarray:
    val_range = np.arange(min_val, max_val)
    return np.random.choice(val_range, size=size, replace=False)


if __name__ == "__main__":
    main()
