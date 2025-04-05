from datetime import datetime, timedelta


CREATE_DATE = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

CLOSE_DATE = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')
