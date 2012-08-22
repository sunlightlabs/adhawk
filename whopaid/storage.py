from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
import os


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """
    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "django.contrib.staticfiles.storage.StaticFilesStorage")()

    def save(self, name, content):
        content.seek(0, os.SEEK_SET)
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
