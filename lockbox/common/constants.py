import re

CONTENT_RANGE_HEADER = "HTTP_CONTENT_RANGE"
CONTENT_RANGE_HEADER_PATTERN = re.compile(r"^bytes (?P<start>\d+)-(?P<end>\d+)/(?P<total>\d+)$")

class UPLOAD_STATUS_TYPES:
    UPLOADING = "uploading"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    PROCESSING = "processing"

# Config

CONFIG_KEYS = {
    "EXPIRATION_DELTA_MINUTES": {
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
    "MAX_UPLOAD_BYTES": {
        "description": "Max bytes that can be uploaded in one go",
        "verbose_name": "Max upload size in bytes",
        "native_type": int,
        "default": 2000000, # 2 MB
    },
}
