import datetime
from zoneinfo import ZoneInfo

schema_get_current_time = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "returns users current local time",
        "parameters": {
            "type": "object",
        },
    },
}

def get_current_time() -> str:
    local_time = datetime.datetime.now(ZoneInfo("localtime")).strftime("%I:%M %p, %B %d, %Y")
    return local_time