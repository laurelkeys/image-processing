import os
import argparse
import subprocess

DEFAULT_PGM_PATH = "o"
DEFAULT_PNG_PATH = os.path.join(DEFAULT_PGM_PATH, "png")

parser = argparse.ArgumentParser()
parser.add_argument("--pgm_path", "-pgm", type=str, default=DEFAULT_PGM_PATH)
parser.add_argument("--png_path", "-png", type=str, default=DEFAULT_PNG_PATH)
parser.add_argument("--unix", "-u", action="store_true", help="Set if running on *nix")
parser.add_argument("--no_exec", "-ne", action="store_true", help="Just show what would be executed")
args = parser.parse_args()

pgm_imgs = [os.path.splitext(file)[0] for file in os.listdir(args.pgm_path) 
            if file.endswith(".pgm")]
png_imgs = [os.path.splitext(file)[0] for file in os.listdir(args.png_path) 
            if file.endswith(".png")]

for img in [img for img in pgm_imgs if img not in png_imgs]:
    print(f"converting.. ", end='')
    pgm_img_path = os.path.join(args.pgm_path, img) + ".pgm"
    png_img_path = os.path.join(args.png_path, img) + ".png"
    
    command = f"convert {pgm_img_path} {png_img_path}"
    if not args.unix:
        command = "magick " + command

    print(f"{pgm_img_path} -> {png_img_path}")
    if args.no_exec:
        print(f">>> {command}\n")
    else:
        subprocess.run(command, shell=True)
