# Wrapper to use moviepy to directly convert a video file to a GIF
# GIFs may play slowly depending on the frame rate of the source material - if you want to modify this, you might want
# to do this process manually, but I'm no expert on A/V.
from moviepy.editor import VideoFileClip
import argparse
from pathlib import Path

# Build a parser (Require infile, accept outfile, with a default)
parser = argparse.ArgumentParser(
    prog='vid_to_gif', description='Take a source video file and convert it to a gif.')
parser.add_argument("Path", type=Path, help="Path to source GIF")
parser.add_argument("-o", '--outfile', type=Path, help="Path to output file", default='./converted_gif.gif')

p = parser.parse_args()


def convert_video(path, outfile):
    print(path, outfile)
    # Passes the source video to the gif writer, either using the default outfile name, or the custom passed one.
    vid_to_convert = VideoFileClip(str(path))
    vid_to_convert.write_gif(outfile)


if __name__ == "__main__":
    convert_video(p.Path, p.outfile)
