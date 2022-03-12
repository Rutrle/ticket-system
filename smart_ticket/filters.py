from smart_ticket import app

@app.template_filter('format_time')
def format_time(timestamp):
    return timestamp.strftime("%d/%m/%Y, %H:%M")