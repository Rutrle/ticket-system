from smart_ticket import app
from datetime import datetime


@app.template_filter('format_time')
def format_time(timestamp: datetime) -> str:
    """
    returns readable string from datetime object 'timestamp'
    """
    return timestamp.strftime("%d/%m/%Y, %H:%M")
