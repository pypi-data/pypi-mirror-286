from dataclasses import dataclass
from px_settings.contrib.django import settings as s

from .const import MiB


__all__ = 'NAME', 'Settings', 'settings',

NAME = 'PXD_UPLOAD'


@s(NAME)
@dataclass
class Settings:
    TO: str = 'pxd-upload'
    SIZE_LIMIT: int = 10 * MiB
    ALLOW_META: bool = True
    SIGNER_SALT: str = 'pxd-upload'


settings = Settings()
