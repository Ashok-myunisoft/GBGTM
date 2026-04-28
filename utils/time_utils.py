def hhmm_to_minutes(time_str: str):
    hh, mm = map(int, time_str.split(":"))
    return hh * 60 + mm