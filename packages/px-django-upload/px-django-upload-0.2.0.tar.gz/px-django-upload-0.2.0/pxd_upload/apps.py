from django.apps import AppConfig
from django.utils.translation import pgettext_lazy


__all__ = ('UploadConfig',)


class UploadConfig(AppConfig):
    name = 'pxd_upload'
    verbose_name = pgettext_lazy('pxd_upload', 'Upload')

