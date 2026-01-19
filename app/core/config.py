from functools import lru_cache
from typing import Type

from core.settings.app import AppSettings
from core.settings.base import AppEnvTypes, BaseAppSettings
from core.settings.development import DevelopmentAppSettings
from core.settings.production import ProductionAppSettings
from core.settings.qa import QAAppSettings

environments: dict[AppEnvTypes, Type[AppSettings]] = {
    AppEnvTypes.development: DevelopmentAppSettings,
    AppEnvTypes.qa: QAAppSettings,
    AppEnvTypes.production: ProductionAppSettings,
}


@lru_cache
def get_settings() -> AppSettings:
    app_env = BaseAppSettings().env
    config = environments[app_env]
    return config()
