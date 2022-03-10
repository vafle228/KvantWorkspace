from io import BytesIO
from os.path import splitext
from sys import getsizeof

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


class ImageThumbnailBaseMixin:
    """ Генерирует миниатюру изображения по заданному коэффициенту """

    def __init__(self, coef: float):
        self.coef = coef

    def _getNewSize(self, width: int, height: int):
        """ Просчитывает размеры, с учетом ориентации картинки """
        if width > height:
            return int(width * self.coef), height * int(width * self.coef) // width
        return width * int(height * self.coef) // height, int(height * self.coef)
    
    def _processImage(self, img: Image, ext: str, mode: str, quality: int, name: str):
        """ Сохраняет картинку по заданным параметрам """
        new_image = BytesIO()
        img.convert(mode).save(new_image, format=ext, quality=quality)
        return InMemoryUploadedFile(
            new_image, 'ImageField', f'{name}.{ext}',
            'image/{type}', getsizeof(new_image), None
        )

    def makeImageThumbnail(self, image_file: InMemoryUploadedFile):
        """ Генерирует миниатюру картинки опираясь на канальность и коэффициент сжатия """
        image = Image.open(image_file)  # Открываем картинку
        image.thumbnail(self._getNewSize(*image.size), resample=Image.ANTIALIAS)  # Делаем миниатюру картинки

        if image.mode == 'RGBA':
            return self._processImage(image, 'png', 'RGBA', 80, splitext(image_file.name)[0])
        return self._processImage(image, 'jpeg', 'RGB', 90, splitext(image_file.name)[0])
