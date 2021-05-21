# Prepare image-pack for Telegram-Stickers-bot.

Simply resize & optimize images in directory to png allowed format.

## To Run
1. Use your venv with all requirement installed according to `requirement.txt` file with command
```
python resize_optimize_images4tg.py --help
```

2. Run docker image
```
docker build -t tiny_script . && docker container run --rm -v $(pwd):/script --name my1 -t tiny_script
```
Note:
> you can simple pass arguments for the script .py file, e.g.:
```
docker container run --rm -v $(pwd):/script --name my1 -t tiny_script --force-save True
```
( --force-save arg. passed):
