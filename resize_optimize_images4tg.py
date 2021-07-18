"""
We go through passed dir, i.e. through all nested dirs as well
and reseize&optimize images with saving PNGs into dir for processed
images.

Processed images satisfy requirements for @stikers tg-bot.

E.g.
>>> python3 resize_optimize_images4tg.py
"""

from PIL import Image
from pathlib import Path
import os
from tqdm import tqdm
import argparse

MAX_WIDTH = 512
MAX_HEIGH = 512
DEFAULT_DIR_WITH_ORIGINALS = './originals'
DEFAULT_DIR_WITH_READIES = './ready4tg'
SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png']
DEFAULT_QUALITY = 85


def resize_image(path2image, max_width=MAX_WIDTH, max_heigh=MAX_HEIGH) -> Image:
    """It returns the resized image."""

    path2image = Path(path2image)
    img = Image.open(path2image)
    width, heigh = img.size
    ratio = min(max_width / width, max_heigh / heigh)
    img = img.resize((int(width * ratio), int(heigh * ratio)), Image.ANTIALIAS)
    return img


def save_optimized_png(img, path2save, quality=DEFAULT_QUALITY):
    img.save(path2save, optimize=True, quality=quality)


def rm_file(file_path):
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)


def clean_dir(dir_path):
    for filename in os.listdir(dir_path):
        if filename == '.gitignore':
            pass
        else:
            rm_file(os.path.join(dir_path, filename))


def main(args):
    if args.clean_folders:
        clean_dir(args.dir_readies)

    saved = []
    file_paths = [
        os.path.join(dirpath, file) for (dirpath, subdirs, files) in os.walk(args.dir_originals) for file in files
        if file.rsplit('.', 1)[-1].lower() in SUPPORTED_FORMATS
    ]

    for file_path in tqdm(file_paths, position=0):

        resized_img = resize_image(file_path, args.max_width, args.max_heigh)
        if args.clean_folders:
            rm_file(file_path)

        new_name = file_path.replace('/', '').lower().replace('.jpg', '.png').replace('.jpeg', '.png')
        path2save = os.path.join(args.dir_readies, new_name)

        if not path2save.split('/')[-1] in os.listdir(args.dir_readies) or args.force_save:
            save_optimized_png(resized_img, str(Path(path2save).with_suffix('.png')), quality=args.quality)
            saved.append(path2save)
        else:
            pass

    if saved:
        print('New file(s):')
        print("\n".join(saved))
    else:
        print('No new files.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--max-width', type=int, default=MAX_WIDTH,
                        help="Max width.")

    parser.add_argument('--max-heigh', type=int, default=MAX_HEIGH,
                        help="Max heigh.")

    parser.add_argument('--dir-originals', type=str, default=DEFAULT_DIR_WITH_ORIGINALS,
                        help="Dir with images to be proceeded.")

    parser.add_argument('--dir-readies', type=str, default=DEFAULT_DIR_WITH_READIES,
                        help="Dir with images ready to be posted to tg-stickers-bot.")

    parser.add_argument('--quality', type=int, default=DEFAULT_QUALITY,
                        help="Desirable quality for resized files in percents.")

    parser.add_argument('--force-save', type=bool, default=False,
                        help="Define if you want to rewrite files in dir-readies.")

    parser.add_argument('--clean-folders', action='store_true', default=True,
                        help="""If the script should clean both folders before proceed the action.""")

    args, unparsed = parser.parse_known_args()
    if unparsed and len(unparsed) > 0:
        print(unparsed)
        assert False

    main(args)
