import os
import json

import cv2
import click
import numpy as np

import optcbx
from optcbx import data
from optcbx import nn


@click.group()
def main():
    pass


@main.command("flask")
@click.option("--debug/--prod", default=True)
def flask_app(debug: bool):
    """Runs a flask server serving the web app demonstration
    """
    from optcbx.app_flask import app
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 1234), debug=debug)


@main.command("demo")
@click.argument('screenshot', type=click.Path(dir_okay=False, exists=True))
@click.option('--units', type=click.Path(file_okay=True, exists=True), 
              default='data/units.json')
@click.option('--smart/--no-smart', default=True)
def demo(screenshot: str, units: str, smart: bool):
    """Given a screenshot generates an output demonstration
    """
    im = cv2.imread(screenshot)
    image_size = 64

    characters = optcbx.detect_characters(
        im, 64, approach='smart' if smart else 'gradient_based')

    id_matches, best_portraits = optcbx.find_characters_ids(
        characters, True, dist_method='feature_vectors')

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
    main.add_command(data.download_portraits.main, name='download-portraits')
    main.add_command(data.labeler.main, name='semi-supervised-labels')
    main.add_command(data.synthetic_dataset.main, name='synthetic')
    main.add_command(nn.compute_portraits_features.main, 
                     name='gen-portraits-features')
    main()
