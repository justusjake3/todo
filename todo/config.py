"""
Application Configurations
Default Ellar Configurations are exposed here through `ConfigDefaultTypesMixin`
Make changes and define your own configurations specific to your application

export ELLAR_CONFIG_MODULE=todo_project.config:DevelopmentConfig
"""

import typing as t
import os.path
from pathlib import Path

from pydantic.json import ENCODERS_BY_TYPE as encoders_by_type
from pydantic.networks import PostgresDsn
from starlette.config import environ
from starlette.middleware import Middleware
from ellar.common import IExceptionHandler, JSONResponse
from ellar.core import ConfigDefaultTypesMixin
from ellar.core.versioning import BaseAPIVersioning, DefaultAPIVersioning

BASE_DIR = Path(__file__).parent.parent


class BaseConfig(ConfigDefaultTypesMixin):
    DEBUG: bool = False

    DEFAULT_JSON_CLASS: t.Type[JSONResponse] = JSONResponse
    SECRET_KEY: str = "ellar_YVVG5nzFMpTFFEzrwhdNF3ZOBASmF21wudN6_oMibtA"

    # injector auto_bind = True allows you to resolve types that are not registered on the container
    # For more info, read: https://injector.readthedocs.io/en/latest/index.html
    INJECTOR_AUTO_BIND = False

    # jinja Environment options
    # https://jinja.palletsprojects.com/en/3.0.x/api/#high-level-api
    JINJA_TEMPLATES_OPTIONS: t.Dict[str, t.Any] = {}

    # Application route versioning scheme
    VERSIONING_SCHEME: BaseAPIVersioning = DefaultAPIVersioning()

    # Enable or Disable Application Router route searching by appending backslash
    REDIRECT_SLASHES: bool = False

    # Define references to static folders in python packages.
    # eg STATIC_FOLDER_PACKAGES = [('boostrap4', 'statics')]
    STATIC_FOLDER_PACKAGES: t.Optional[t.List[t.Union[str, t.Tuple[str, str]]]] = []

    # Define references to static folders defined within the project
    STATIC_DIRECTORIES: t.Optional[t.List[t.Union[str, t.Any]]] = []

    # static route path
    STATIC_MOUNT_PATH: str = "/static"

    CORS_ALLOW_ORIGINS: t.List[str] = ["*"]
    CORS_ALLOW_METHODS: t.List[str] = ["*"]
    CORS_ALLOW_HEADERS: t.List[str] = ["*"]
    ALLOWED_HOSTS: t.List[str] = ["*"]

    # Application middlewares
    MIDDLEWARE: t.Sequence[Middleware] = []

    # A dictionary mapping either integer status codes,
    # or exception class types onto callables which handle the exceptions.
    # Exception handler callables should be of the form
    # `handler(context:IExecutionContext, exc: Exception) -> response` 
    # and may be either standard functions, or async functions.
    EXCEPTION_HANDLERS: t.List[IExceptionHandler] = []

    # Object Serializer custom encoders
    SERIALIZER_CUSTOM_ENCODER: t.Dict[
        t.Any, t.Callable[[t.Any], t.Any]
    ] = encoders_by_type

    SQLALCHEMY_URL = "postgresql://postgres:1234@localhost/todo"

class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True

class TestConfig(BaseConfig):
    DEBUG = bool = False
    SQLALCHEMY_URL = "postgresql://postgres:1234@localhost/test_db"