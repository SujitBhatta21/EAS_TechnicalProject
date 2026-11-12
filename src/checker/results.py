from dataclasses import dataclass
from datetime import datetime


@dataclass
class HostCheckResult:
    hostname: str
    status: str
    http_status: int | None = None
    response_time_ms: float | None = None
    message: str = ""
