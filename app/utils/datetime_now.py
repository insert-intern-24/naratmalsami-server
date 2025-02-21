from datetime import datetime, timezone

KST = pytz.timezone('Asia/Seoul')

def datetime_now():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M")