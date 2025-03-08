from datetime import datetime
import pytz

KST = pytz.timezone('Asia/Seoul')

def datetime_now():
    return datetime.now(KST).strftime(r"%Y-%m-%d %H:%M")
