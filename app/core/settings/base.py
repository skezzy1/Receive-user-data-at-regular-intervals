import os
from enum import Enum

from pydantic_settings import BaseSettings


class AppEnvTypes(Enum):
    development: str = 'development'
    qa: str = 'qa'
    production: str = 'production'


class AppUploadFolders(Enum):
    users: str = 'users'


class BaseAppSettings(BaseSettings):
    env: AppEnvTypes = os.getenv('env') or AppEnvTypes.development
