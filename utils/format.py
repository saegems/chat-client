from datetime import datetime


def formatDate(time_str):
    if not time_str or time_str.lower() == "now":
        return "Now"
    try:
        if 'T' in time_str:
            dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")
        else:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        formatted_time_str = dt.strftime("%I:%M %p, %d %B, %Y")
        return formatted_time_str
    except (ValueError, TypeError):
        return time_str if time_str else "Unknown"
