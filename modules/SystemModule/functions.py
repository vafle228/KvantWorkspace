def format_image(image_file, coefficient):
    from PIL import Image
    from io import BytesIO
    from sys import getsizeof
    from django.core.files.uploadedfile import InMemoryUploadedFile

    image = Image.open(image_file)  # Открываем картинку
    width, height = image.size  # Получаем размеры картинки
    new_image = BytesIO()  # Создаем байтовое представление

    resize = (width * int(height * coefficient) // height, int(height * coefficient))  # Изменение по высоте

    if width > height:  # Если горизонтальная картинка
        resize = (int(width * coefficient), height * int(width * coefficient) // width)  # Изменение по ширине

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


def change_file_directory(file, to_path, from_path):
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