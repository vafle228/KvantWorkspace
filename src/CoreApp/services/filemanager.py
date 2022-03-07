from os.path import basename
from storages.backends.s3boto3 import S3Boto3Storage


class FileMoveBaseMixin:
    """ Изменяет расположение файла в AWS Bucket'е """  
    def _getToPath(self, file, to_path: str):
        """ Создание нового валидного пути для file """
        return '/'.join([to_path, basename(file.name)])

    def changeDirectory(self, file, to_path: str, is_moveable=True):
        """ Изменяет расположения file по пути to_path при is_moveable """
        to_path = self._getToPath(file, to_path)
        if is_moveable and file.name != to_path:
            file.name = self._changeFileDirectory(file, to_path)
        return file
    
    def _changeFileDirectory(self, file, to_path: str):
        """ Движения file в AWS S3 до пути toPath """
        bucket = S3Boto3Storage()
        
        to_path = bucket._normalize_name(bucket._clean_name(to_path))
        from_path = bucket._normalize_name(bucket._clean_name(file.name))
        
        bucket.connection.meta.client.copy(
            {
                'Key': from_path,
                'Bucket': bucket.bucket_name
            }, 
            bucket.bucket_name, to_path)
        return to_path
