# Takes a group of images and builds a GIF from them.
# Assumes that only images you want to convert are in the source directory
# Assumes that the images are in a sortable name format (0, 1, 2... 21, etc.)
# Requires natsort library, which handles abnormally numbered files, which may need installed
import glob
from PIL import Image
from natsort import natsorted
import argparse
from pathlib import Path

# Build a parser (Require infile directory, accept outfile and infile extension, with defaults)
parser = argparse.ArgumentParser(
    prog='frames_to_gif', description='Converts a group of images to a gif')
parser.add_argument("Path", type=Path, help="Path to folder of images")
parser.add_argument("-o", '--outfile', help="Path to output file", default='./mygif.gif')
parser.add_argument("-t", '--filetype', help="File type if other than png (no leading period)", default='png')
p = parser.parse_args()


def make_gif(location, outfile, ftype):
    """Build a list of input files, sort the list so that the images are in sequence. Build a gif"""
    # Build and sort a list of files to turn into a gif
    frame_list = glob.glob(f"{location}/*.{ftype}")
    sorted_files = natsorted(frame_list)
    # Open these files
    frames = [Image.open(image) for image in sorted_files]
    # Starting with the first file (frame_one), construct a gif. Disposal needs to be set to 2 to prevent
    # some strange ghosting from happening caused by transparency
    frame_one = frames[0]
    frame_one.save(outfile, format="GIF", append_images=frames[1:], save_all=True, duration=100, loop=0, disposal=2)


if __name__ == "__main__":
    make_gif(p.Path, p.outfile, p.filetype)
