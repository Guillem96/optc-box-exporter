import click
from pathlib import Path

import cv2

import tqdm.auto as tqdm


@click.command()
@click.option('--portraits-path',
              default='data/Portrait',
              type=click.Path(exists=True, file_okay=False))
@click.option('--avg-multiple', default=3, type=int)
@click.option('--output', type=click.Path(dir_okay=False))
def main(portraits_path, avg_multiple, output):
    """Using a pretrained CNN, the command computes a feature vector encoding
    each portrait
    """
    import torch
    from optcbx.nn.features import feature_extractor, get_feature_vector

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    output = Path(output)
    output.parent.mkdir(exist_ok=True, parents=True)

    portraits_paths = list(Path(portraits_path).glob('*.png'))
    portraits = [cv2.imread(str(o)) for o in tqdm.tqdm(portraits_paths)]

    m = feature_extractor()
    m.to(device)

    fv = get_feature_vector(m, portraits, average_multiple=avg_multiple)
    torch.save(fv, output)
