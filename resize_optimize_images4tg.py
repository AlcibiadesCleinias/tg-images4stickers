"""
We go through passed dirs, i.e. all dirs which are inside the passed
and reseize&optimize images with saving PNGs into dir-readies.

Saved images by defualt satisfy requirements for @stikers tg-bot.

>> python3 resize_optimize_images4tg.py
"""

from PIL import Image
from pathlib import Path
import os
from tqdm import tqdm
import argparse

MAX_WIDTH = 512
MAX_HEIGH = 512
DIR_ORIGINALS = './originals'
DIR_READIES = './ready4tg'
SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png']
DEFAULT_QUALITY = 85

def resize_image(path2image, max_width=MAX_WIDTH, max_heigh=MAX_HEIGH) -> Image:
    ''' It returns resized image. '''

    path2image = Path(path2image)
    img = Image.open(path2image)
    width, heigh = img.size
    ratio = min(max_width / width, max_heigh / heigh)
    img = img.resize((int(width*ratio), int(heigh*ratio)), Image.ANTIALIAS)
    return img

def save_optimized_png(img, path2save, quality=85):
    '''  We save img with compression quality. '''

    img.save(path2save, optimize=True, quality=quality)

def main(args):

    logs_new_saved = []
    for data in os.walk(args.dir_originals):
        path, subdirs, files = data
        for f in tqdm(files, position=0):
            if f.rsplit('.', 1)[-1].lower() not in ['jpg', 'jpeg', 'png']:
                continue

            file_path = os.path.join(path, f)
            resized_img = resize_image(file_path, args.max_width, args.max_heigh)

            new_name = f.replace('/','').lower().replace('.jpg', '.png').replace('.jpeg', '.png')
            path2save = os.path.join(args.dir_readies, new_name)

            if not path2save.split('/')[-1] in os.listdir(args.dir_readies) or args.force_save:
                save_optimized_png(resized_img, str(Path(path2save).with_suffix('.png')), quality=args.quality)
                logs_new_saved.append(path2save)
            else:
                pass

    if logs_new_saved:
        print('New file(s):')
        print("\n".join(logs_new_saved))
    else:
        print('No new files.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--max-width', type=int, default=MAX_WIDTH,
                        help="Max width.")

    parser.add_argument('--max-heigh', type=int, default=MAX_HEIGH,
                    help="Max heigh.")

    parser.add_argument('--dir-originals', type=str, default=DIR_ORIGINALS,
                        help="Dir with images to be proceeded.")

    parser.add_argument('--dir-readies', type=str, default=DIR_READIES,
                        help="Dir with images ready to be posted to tg-stickers-bot.")

    parser.add_argument('--quality', type=int, default=DEFAULT_QUALITY,
                        help="Desirable quality for resized files in percents.")

    parser.add_argument('--force-save', type=bool, default=False,
                        help="Define if you want to rewrite files in dir-readies.")

    args, unparsed = parser.parse_known_args()
    if unparsed and len(unparsed) > 0:
        print(unparsed)
        assert False

    main(args)
