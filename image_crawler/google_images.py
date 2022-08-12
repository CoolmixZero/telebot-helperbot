import os
import shutil

from aiogram import types
from icrawler.builtin import GoogleImageCrawler
from settings.config import type_and_size

dir_path = '/PyCharm Projects/Telegram_bot/image_crawler_downloads/'


def delete_images_from_dir():
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))
    os.chmod(dir_path, 755)


def get_images_from_dir():
    files = [os.path.join(root, file) for root, dirs, files in os.walk(dir_path)
             for file in files if '.jpg' or '.png' in file]
    return files


def get_image(image_name: types.Message, image_type='photo', image_size='medium', amount=3) -> (str, int):
    """Gets image from Google

    :param image_name: name of the image
    :param image_type: [photo, face, clipart, linedrawing, animated]
    :param image_size: [large, medium, icon]
    :param amount: amount of pictures to download, max=20
    :return: None
    """
    image_name = image_name.text.title()
    if len(type_and_size) > 0:
        if type_and_size['type'] in ('photo', 'face', 'clipart', 'linedrawing', 'animated'):
            image_type = type_and_size['type']
        if type_and_size['size'] in ('large', 'medium', 'icon'):
            image_size = type_and_size['size']
        if type_and_size['amount'] in ('3', '5', '10'):
            amount = type_and_size['amount']

    if int(amount) > 10:
        raise ValueError('Amount should be less than or equal 10')

    try:
        delete_images_from_dir()
        crawler = GoogleImageCrawler(storage={'root_dir': dir_path})
        filters = dict(
            type=image_type,  # photo, face, clipart, linedrawing, animated
            size=image_size  # large, medium, icon
        )
        crawler.crawl(keyword=image_name,
                      max_num=int(amount),
                      filters=filters)

        return image_name, int(amount)

    except Exception as e:
        print(e)
