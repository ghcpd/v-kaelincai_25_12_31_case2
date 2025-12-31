import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import app
import datetime

future = datetime.datetime.now() + datetime.timedelta(days=30)
formats = {
    'iso': future.strftime('%Y-%m-%dT%H:%M'),
    'iso_sec': future.strftime('%Y-%m-%dT%H:%M:%S'),
    'slash': future.strftime('%Y/%m/%d %H:%M'),
    'us_am_pm': future.strftime('%m/%d/%Y %I:%M %p'),
    'text_month': future.strftime('%b %d, %Y %H:%M'),
    'eu': future.strftime('%d-%m-%Y %H:%M')
}

results = {}
app.config['TESTING'] = True
with app.test_client() as client:
    for k, v in formats.items():
        data = {'name': f'Test {k}', 'email': f'{k}@example.com', 'event_datetime': v}
        resp = client.post('/api/register', json=data)
        try:
            body = resp.get_json()
        except Exception:
            body = resp.data.decode('utf-8')
        results[k] = {'status_code': resp.status_code, 'body': body}

print(json.dumps(results, indent=2))
