import os

"""
MarcusLion Global variable
"""
global __env__
global __base_url__
global __api_key__
global __api_version__
global __project_id__
global __backend_base_url__
global __backend_api_version__

IS_BACKEND_PARAM = 'is_backend'


def __init__():
    global __base_url__
    global __backend_base_url__
    global __backend_api_version__
    global __env__
    global __api_key__
    global __api_version__
    global __project_id__

    __env__ = os.getenv('MARCUSLION_ENV', "uat")
    __api_key__ = os.getenv('MARCUSLION_API_KEY', "b7f88c9c-94ba-11ee-b9d1-0242ac120002")
    __base_url__ = os.getenv('MARCUSLION_API_HOST', "https://uat.marcuslion.com")
    __api_version__ = "core/api/v2"  # no starting slash
    __project_id__ = os.getenv('MARCUSLION_API_PROJECT_ID', "7ea7393b-017d-3ba9-a363-5b7a1043e0fes")
    __backend_api_version__ = "api/v2"
    __backend_base_url__ = __base_url__
    pass


def _set_env(env:str):
    global __base_url__
    global __env__
    global __backend_base_url__
    global __api_version__

    if env == "qa":
        __base_url__ = "https://qa1.marcuslion.com"
        __env__ = env
    elif env == "uat":
        __base_url__ = "https://uat.marcuslion.com"
        __env__ = env
    elif env == "dev":
        __base_url__ = "http://localhost:8384"
        __api_version__ = "api/v2"
        __backend_base_url__ = "http://localhost:8383"
        __env__ = env
    else:
        raise RuntimeError("Invalid environment")
    pass


def get_env():
    global __env__
    return __env__


def get_base_url():
    global __base_url__
    return __base_url__


def get_backend_base_url():
    global __backend_base_url__
    return __backend_base_url__


def get_backend_api_version():
    global __backend_api_version__
    return __backend_api_version__


def get_api_key():
    global __api_key__
    return __api_key__


def get_api_version():
    global __api_version__
    return __api_version__


def get_config():
    global __base_url__
    global __env__
    global __api_key__
    global __api_version__
    global __project_id__

    return {
        "env": __env__,
        "api_key": __api_key__,
        "base_url": __base_url__,
        "project_id": __project_id__,
        "api_version": __api_version__
    }
