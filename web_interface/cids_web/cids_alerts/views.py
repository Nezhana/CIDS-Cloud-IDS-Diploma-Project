from django.shortcuts import render
from django.core.cache import cache

import requests

# Create your views here.

def alerts(request):
    alerts = get_alert_data_from_api()
    # print(alerts)
    # formated_and_sorted_alerts = format_and_sort_alerts(alerts)
    # print(formated_and_sorted_alerts)

    # return render(request, 'cids_alerts/alerts.html', context={'alerts': formated_and_sorted_alerts})
    return render(request, 'cids_alerts/alerts.html', context={'alerts': alerts})


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

def anomalous_rate_finder(alerts):
    anomalies = []
    ind = 0
    for key, item in alerts['z_score'].items():
        if item >= 90.0:
            date = ' '.join(alerts['timestamp'][key].split('T')).replace('-', '/')
            message = 'DDoS Warning'
            trigger = f"{(alerts['remote_IP'][key])} exceeded requests"
            anomalies.append({ind: [ date, message, trigger ]})
            ind += 1
    return anomalies

def suspicious_uas_formater(alerts):
    anomalies = []
    ind = 0
    for key, item in alerts['timestamp'].items():
        date = ' '.join(alerts['timestamp'][key].split('T')).replace('-', '/')
        message = f"Access Denied: {(alerts['remote_IP'][key])}"
        trigger = f"Unknown user agent: {(alerts['UserAgent'][key])}"
        anomalies.append({ind: [ date, message, trigger ]})
        ind += 1
    return anomalies


def night_activity_formater(alerts):
    anomalies = []
    ind = 0
    for key, item in alerts['timestamp'].items():
        date = ' '.join(alerts['timestamp'][key].split('T')).replace('-', '/')
        message = f"Access Denied: {(alerts['remote_IP'][key])}"
        trigger = f"Unusual activity timestamp"
        anomalies.append({ind: [ date, message, trigger ]})
        ind += 1
    return anomalies

def format_and_sort_alerts(alerts):
    a_rate = anomalous_rate_finder(alerts['anomalous_rate'])
    # print(a_rate)
    sus_uas = suspicious_uas_formater(alerts['suspicious_uas'])
    # print(sus_uas)
    mal_act = night_activity_formater(alerts['night_activity'])
    # print(mal_act)

    all_alerts = [*a_rate, *sus_uas, *mal_act]
    formated_alerts = [list(el.values())[0] for el in all_alerts]
    # print(formated_alerts)
    sorted_alerts = sorted(formated_alerts, key=lambda x: x[0])
    # print(sorted_alerts)

    result = []
    ind = 1
    for el in sorted_alerts:
        result.append({'ID': ind, 'timestamp': el[0], 'message': el[1], 'trigger': el[2]})
        ind += 1
    
    return result

