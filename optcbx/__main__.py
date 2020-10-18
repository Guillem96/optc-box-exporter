import os
import json

import cv2
import click
import numpy as np

import streamlit.cli

import optcbx


@click.group()
def main():
    pass

@main.command("streamlit")
def streamlit_app():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'app_st.py')
    args = []
    streamlit.cli._main_run(filename, args)


@main.command("demo")
@click.argument('screenshot', type=click.Path(dir_okay=False, exists=True))
@click.option('--units', type=click.Path(file_okay=True, exists=True), 
              default='data/units.json')
def demo(screenshot: str, units: str):
    im = cv2.imread(screenshot)
    image_size = 64
    
    characters = optcbx.detect_characters(im, 64)
    id_matches, best_portraits = optcbx.find_characters_ids(
        characters, True, dist_method='mse')

    units = json.load(open(units))
    units = optcbx.units.parse_units(units)
    units_ids = np.array([o.number for o in units])
    id_matches = [(units_ids == i).argmax() for i in id_matches]
    units = [units[i] for i in id_matches]

    print('\n'.join(map(str, units)))

    cols = 5
    col_margin = image_size // 4
    rows, m = divmod(characters.shape[0], cols)
    rows += (m > 0)

    demo_image = np.zeros((rows * image_size,
                           image_size * cols * 2 + col_margin * (cols - 1),
                           3), dtype='uint8')

    for i, c in enumerate(characters):
        portrait_match = best_portraits[i]
        row = i // cols
        column = i % cols

        start_h = row * image_size
        end_h = start_h + image_size

        start_w = column * image_size * 2 + (column * col_margin)
        end_w = start_w + image_size

        demo_image[start_h: end_h, start_w:end_w] = c
        demo_image[start_h: end_h, end_w:end_w + image_size] = portrait_match

    cv2.imshow('distances', demo_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
