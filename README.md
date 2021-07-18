# Prepare image-pack for Telegram-Stickers-bot.

Simply resize & optimize images in directory to the special png format.

By default, script run will clean both folders. For the full list of argument check the code of `.py`.

## How to Run
I present 2 options:
1. Use your venv with all requirement installed according to `requirement.txt` file with command
```
python resize_optimize_images4tg.py --help
```

2. Run in Docker

The line below represents how to build image and run container by the 1 line:
```
docker build -t tg-images4stickers . && docker container run --rm -v $(pwd):/script --name tiny-tg-container -t tg-images4stickers
```
Note:
> you able to merely pass arguments to the resize_optimize_images4tg.py file on docker run command, e.g.:
```
docker container run --rm -v $(pwd):/script --name my1 -t tiny_script --force-save True
```
( --force-save arg. passed):
