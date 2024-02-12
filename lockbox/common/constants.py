
class UPLOAD_STATUS_TYPES:
    UPLOADING = "uploading"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


# Config

CONFIG_KEYS = {
    "EXPIRATION_DELTA_MINUTES":  {
        "description": "Date created + this delta at which file expires",
        "verbose_name": "File expiration delta (minutes)",
        "native_type": int,
        "default": 120,
    },

    "ABANDONED_DELTA_MINUTES": {
        "description": "Date created + this delta at which a file is marked as abandoned",
        "verbose_name": "Uncompleted file abandoned max age",
        "native_type": int,
        "default": 20,
    },

    "ABANDONED_EXPIRED_SCAN_INTERVAL": {
        "description": "Scan and scrub abandoned or expired uploads",
        "verbose_name": "Scan interval for abandoned/expired files",
        "native_type": int,
        "default": 20,
    },
}
