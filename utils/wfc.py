from datetime import datetime, timezone


def to_wcf_date(date_str: str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    dt = dt.replace(tzinfo=timezone.utc)
    ms = int(dt.timestamp() * 1000)
    return f"/Date({ms})/"