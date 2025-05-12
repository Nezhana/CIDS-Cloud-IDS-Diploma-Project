from django.shortcuts import render
from django.core.cache import cache

import requests

# Create your views here.

def alerts(request):
    # logs = get_logs_data_from_api()
    # data = make_alerts_table(logs, 17)

    alerts = get_alert_data_from_api()
    print(alerts)

    # return render(request, 'cids_alerts/alerts.html', context=data)
    return render(request, 'cids_alerts/alerts.html')


def get_alert_data_from_api():
    cached = cache.get(f'fastapi_alerts')
    if cached:
        return cached
    
    try:
        response = requests.get("http://localhost:8000/api/alerts", timeout=90)
        if response.status_code == 200:
            data = response.json()
            result = data['alert_data']
            cache.set(f'fastapi_alerts', data['alert_data'], timeout=60)  # кешуємо на 60 секунд
            return result
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FastAPI: {e}")
    return []


def get_logs_data_from_api():

    cached = cache.get(f'fastapi_logs')
    if cached:
        return cached
    
    try:
        response = requests.get("http://localhost:8000/api/logs", timeout=90)
        if response.status_code == 200:
            data = response.json()
            result = data['logs']
            cache.set(f'fastapi_logs', data['logs'], timeout=60)  # кешуємо на 60 секунд
            return result
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FastAPI: {e}")
    return []


def make_alerts_table(data, log_counter):
    headers = []
    values = {}
    for ind in range(log_counter):
        values[str(ind)] = []
    for header, elements in data.items():
        if header in ['Time_Offset', 'Version_Id']:
            continue
        headers.append(header.replace('_', ' '))
        for key, element in elements.items():
            if header == 'Time':
                element = element.replace('[', '')
                element = element.replace(':', ' ', 1)
            values[key].append(element)
    
    return {'headers': headers, 'values': values}
