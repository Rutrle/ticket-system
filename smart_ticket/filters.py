from smart_ticket import app

@app.template_filter('format_time')
def format_time(timestamp):
    return timestamp.strftime("%m/%d/%Y, %H:%M")