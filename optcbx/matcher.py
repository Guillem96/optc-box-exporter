import json
import functools
import multiprocessing as mp
from pathlib import Path
from typing import Any, List, Union, Tuple

import tqdm.auto as tqdm

import cv2
import numpy as np

import torch

from skimage.metrics import structural_similarity as ssim

from optcbx import detect_characters
from optcbx.units import parse_units, Character


# Keep computational expensive variables in memory
_portraits_paths = None
_portraits = {}
_units = None
_units_ids = None


FindCharactersResult = Union[List[int], Tuple[List[int], np.ndarray]]


def find_characters_from_screenshot(
        screenshot: np.ndarray,
        image_size: Union[int, Tuple[int, int]] = 64,
        dist_method: str = 'mse',
        return_thumbnails: bool = False) -> List[Character]:

    if isinstance(image_size, int):
        image_size = (image_size,) * 2

    global _units, _units_ids

    characters = detect_characters(screenshot, image_size)
    id_matches = find_characters_ids(characters, dist_method=dist_method)

    if _units is None:
        _units = json.load(open('data/units.json'))
        _units = parse_units(_units)
        _units_ids = np.array([o.number for o in _units])

    id_matches = [(_units_ids == i).argmax() for i in id_matches]
    matched_units = [_units[i] for i in id_matches]

    if not return_thumbnails:
        return matched_units
    else:
        return matched_units, characters


def find_characters_ids(
        characters: np.ndarray,
        return_portraits: bool = False,
        dist_method: str = 'mse') -> FindCharactersResult:

    image_size = characters.shape[1:3]

    global _portraits, _portraits_paths

    if _portraits_paths is None:
        _portraits_paths = list(Path('data/Portrait').glob('*.png'))

    if _portraits.get(image_size) is None:
        _portraits[image_size] = np.array(
            [_load_im(o, image_size) for o in tqdm.tqdm(_portraits_paths)])

    best_matches = _top_similarities(characters,
                                     _portraits[image_size],
                                     method=dist_method)
    ids = [int(_portraits_paths[i].stem) for i in best_matches]

    if not return_portraits:
        return ids
    else:
        return ids, _portraits[image_size][best_matches]


def _load_im(path, size):
    im = cv2.imread(str(path))
    return cv2.resize(im, size[::-1])


def _top_similarities(characters: np.ndarray, 
                      portraits: np.ndarray,
                      method: str = 'mse'):

    print('Computing distances...')
    if method == 'mse':
        cd = characters.reshape(len(characters), 1, -1)
        pd = portraits.reshape(1, len(portraits), -1)

        distances = np.mean(np.square(cd - pd), -1)
        best_matches = np.argmax(-distances, -1)

    elif method == 'ssim':
        distances = []
        pool = mp.Pool(mp.cpu_count())
        for c in tqdm.tqdm(characters):
            dist_fn = functools.partial(ssim, im2=c, multichannel=True)
            cur_dists = list(tqdm.tqdm(pool.imap(dist_fn, portraits),
                                       total=len(portraits)))
            distances.append(cur_dists)
        pool.close()

        distances = np.array(distances)
        best_matches = np.argmax(distances, -1)

    elif method == 'feature_vectors':
        import torch.nn.functional as F
        from optcbx.nn.features import (get_feature_vector,
                                        feature_extractor,
                                        load_portrait_features)

        m = feature_extractor()
        portraits_features = load_portrait_features()

        units_features = get_feature_vector(m, characters, 3).cpu()
        units_features = units_features.view(len(characters), 1, -1)

        similarities = F.cosine_similarity(units_features, 
                                           portraits_features, 
                                           dim=-1)
        best_matches = similarities.argmax(-1)

    else:
        raise ValueError(f"Method {method} not supported")

    return best_matches.tolist()
