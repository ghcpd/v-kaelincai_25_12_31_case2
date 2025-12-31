import json
import urllib.request
import urllib.error
import datetime

base_url = 'http://127.0.0.1:5000/api/register'
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
for k, v in formats.items():
    payload = json.dumps({'name': f'Test {k}', 'email': f'{k}@example.com', 'event_datetime': v}).encode('utf-8')
    req = urllib.request.Request(base_url, data=payload, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode('utf-8')
            results[k] = {'status': resp.status, 'body': body}
    except Exception as e:
        results[k] = {'error': str(e)}

print(json.dumps(results, indent=2))
