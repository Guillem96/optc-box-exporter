import json
from pathlib import Path
from typing import Any, List, Union, Tuple

import tqdm.auto as tqdm

import cv2
import numpy as np

from square_detection import detect_characters

image_size = 64
_portraits_paths = None
_portraits = None
_units = None

FindCharactersResult = Union[List[int], Tuple[List[int], np.ndarray]]


def find_characters_from_screenshot(screenshot: np.ndarray) -> List[Any]:
    global _units

    characters = detect_characters(screenshot)
    id_matches = find_characters_ids(characters)

    if _units is None:
        _units = json.load(open('data/units.json'))
        _units = [_viable_unit(o) for o in _units]

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


def _viable_unit(unit):
    if all(o is not None for o in unit):
        return unit
    
    if all(unit[i] is not None for i in range(9, 15)):
        return unit

    return []


def main():
    characters = detect_characters(
        r'data\screenshots\Screenshot_20201014-155031.jpg', image_size)

    id_matches, best_portraits = find_characters_ids(characters, True)

    cols = 3
    rows = characters.shape[0] // cols
    demo_image = np.zeros((rows * image_size,
                           image_size * cols * 2,
                           3), dtype='uint8')

    for i, c in enumerate(characters):
        portrait_match = best_portraits[i]
        row = i % rows
        column = i % cols

        start_h = row * image_size
        end_h = start_h + image_size

        start_w = column * image_size * 2
        end_w = start_w + image_size

        demo_image[start_h: end_h, start_w:end_w] = c
        demo_image[start_h: end_h, end_w:end_w + image_size] = portrait_match

    cv2.imshow('distances', demo_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
