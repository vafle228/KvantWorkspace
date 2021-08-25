from abc import abstractmethod

class ImageMixinBase:
    def __init__(self, coef):
        self.coef = coef
    
    @abstractmethod
    def get_image_file(self):
        pass

    @abstractmethod
    def get_instance_image(self):
        pass

    def clean_image(self):
        image = self.get_image_file()
        instance_image = self.get_instance_image()

        return instance_image if image == instance_image else self.format_image(image)

    def get_new_size(self, width, height):
        if width > height:
            return (int(width * self.coef), height * int(width * self.coef) // width)
        return (width * int(height * self.coef) // height, int(height * self.coef))
    
    def format_image(self, image_file):
        from PIL import Image
        from io import BytesIO
        from sys import getsizeof
        from django.core.files.uploadedfile import InMemoryUploadedFile

        image = Image.open(image_file)  # Открываем картинку
        new_image = BytesIO()  # Создаем байтовое представление

        resize = self.get_new_size(*image.size)

        image.thumbnail(resize, resample=Image.ANTIALIAS)  # Делаем миниатюру картинки
        image = image.convert('RGB')  # Убираем все лишние каналы
        image.save(new_image, format='JPEG', quality=90)  # Конвертируем в JPEG, ибо мало весит

        new_image.seek(0)  # Возвращение в начало файла

        name = f'{image_file.name.split(".")[0]}.jpeg'  # Имя файла

        # Перезапись файла в базе данных
        model_image = InMemoryUploadedFile(
            new_image, 'ImageField',  # Картинка, поля сохранения
            name, 'image/jpeg',  # Имя картинки, содержание
            getsizeof(new_image), None  # Размер, доп инфа
        )
        return model_image
    


class FileManagerMixinBase:
    @abstractmethod
    def is_file_moveable(self, file):
        pass

    def change_directory(self, file, from_path, to_path):
        if self.is_file_moveable(file):
            file.name = self.change_file_directory(file, from_path, to_path)
        return file
    
    def change_file_directory(self, file, from_path, to_path):
        from storages.backends.s3boto3 import S3Boto3Storage
    
        bucket = S3Boto3Storage()
        file_name = file.name.split('/')[-1]
        
        from_path = bucket._normalize_name(bucket._clean_name(f'{from_path}/{file_name}'))
        to_path = bucket._normalize_name(bucket._clean_name(f'{to_path}/{file_name}'))
        
        bucket.connection.meta.client.copy_object(
            Bucket=bucket.bucket_name,
            CopySource=bucket.bucket_name + "/" + from_path,
            Key=to_path)
        bucket.delete(from_path)
        
        return to_path
