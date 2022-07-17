# This script is designed to take gif and break it down into individual (png) images for use in image cleanup, etc.
# Uses PIL, which you probably already have
from PIL import Image
import argparse
from pathlib import Path

# Build a parser (Require infile)
parser = argparse.ArgumentParser(
    prog='gif_to_frames', description='Take a source GIF file and convert it to individual images.')
parser.add_argument("Path", type=Path, help="Path to source GIF")
p = parser.parse_args()


def break_down_gif(path):
    # 24 appears to be the top-end for frames in a gif per second, but I don't do images for a living.
    # Adjust to your needs
    num_key_frames = 24

    with Image.open(str(path)) as im:
        for i in range(num_key_frames):
            im.seek(im.n_frames // num_key_frames * i)
            im.save('{}.png'.format(i))
        print('Images exported')


if __name__ == "__main__":
    break_down_gif(p.Path)
