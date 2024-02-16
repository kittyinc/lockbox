from os import getenv
from unicodedata import normalize

from common.constants import CONFIG_KEYS


def normalize_string(string, form="NFKC"):
    return normalize(form, string)

def cast_to_native_type(key, value, native_type):
    try:
        return native_type(value)
    except ValueError as e:
        message = (
            f"Received unexpected value type for configuration key {key}\nValue: {value}\nExpected type : {native_type}"
        )
        raise ValueError(message) from e


def get_config(key):
    from common.models import Config, Configuration
    config = Config(**CONFIG_KEYS[key], key=key)

    obj = Configuration.objects.filter(key=key).first()

    if obj:
        config.value = cast_to_native_type(key, obj.value, config.native_type)
        config.source = "db"
        return config

    value = getenv(key)

    if value:
        config.value = cast_to_native_type(key, value, config.native_type)
        config.source = "env_variable"
        return config

    config.value = config.default
    config.source = "default"
    return config


def get_max_size_chunk_bytes():
    return get_config("MAX_UPLOAD_BYTES").value
