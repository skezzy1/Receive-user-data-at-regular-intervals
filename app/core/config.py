from functools import lru_cache
from typing import Type

from app.core.settings.app import AppSettings
from app.core.settings.base import AppEnvTypes, BaseAppSettings
from app.core.settings.development import DevelopmentAppSettings
from app.core.settings.production import ProductionAppSettings
from app.core.settings.qa import QAAppSettings

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
