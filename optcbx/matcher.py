import json
from pathlib import Path
from typing import Any, List, Union, Tuple

import tqdm.auto as tqdm

import cv2
import numpy as np

from optcbx import detect_characters
from optcbx.units import parse_units, Character


_portraits_paths = None
_portraits = None
_units = None
_units_ids = None

FindCharactersResult = Union[List[int], Tuple[List[int], np.ndarray]]


def find_characters_from_screenshot(screenshot: np.ndarray) -> List[Character]:
    global _units, _units_ids

    characters = detect_characters(screenshot)
    id_matches = find_characters_ids(characters)

    if _units is None:
        _units = json.load(open('data/units.json'))
        _units = parse_units(_units)
        _units_ids = np.array([o.number for o in _units])

    id_matches = [(_units_ids == i).argmax() for i in id_matches]
    return [_units[i] for i in id_matches]


def find_characters_ids(
        characters: np.ndarray, 
        return_portraits: bool = False) -> FindCharactersResult:

    global _portraits, _portraits_paths

    if _portraits_paths is None:
        _portraits_paths = list(Path('data/Portrait').glob('*.png'))

    if _portraits is None:
        _portraits = np.array([_load_im(o, characters.shape[1:3]) 
                               for o in tqdm.tqdm(_portraits_paths)])

    best_matches = _top_similarities(characters, _portraits)
    ids = [int(_portraits_paths[i].stem) for i in best_matches]
    

    if not return_portraits:
        return ids
    else:
        return ids, _portraits[best_matches]


def _load_im(path, size):
    im = cv2.imread(str(path))
    return cv2.resize(im, size[::-1])


def _top_similarities(characters, portraits):
    cd = characters.reshape(len(characters), 1, -1)
    pd = portraits.reshape(1, len(portraits), -1)

    print('Computing distances...')
    distances = np.mean(np.square(cd - pd), -1)
    best_matches = np.argmax(-distances, -1)
    return best_matches.tolist()

