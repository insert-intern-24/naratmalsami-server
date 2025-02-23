from datetime import datetime, timezone
import pytz

KST = pytz.timezone('Asia/Seoul')

def datetime_now():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M")