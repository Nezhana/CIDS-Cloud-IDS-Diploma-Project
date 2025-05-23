from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
from django.core.cache import cache
import requests

FASTAPI_URL = "http://localhost:8000/api/analyze"

DATA_TYPES = ['summary_by_date', 'get_last_log_data', 'summary_for_gets_by_IP', 'get_malicious_ip_list']

def dashboard(request):
    return render(request, 'cids_dashboard/dashboard.html')


def get_logs_data_from_api(data_type):

    cached = cache.get(f'fastapi_{data_type}')
    if cached:
        return cached

    try:
        response = requests.get(FASTAPI_URL, timeout=90)
        if response.status_code == 200:
            data = response.json()
            result = data['analysis_data'][data_type]
            for Dtype in DATA_TYPES:
                cache.set(f'fastapi_{Dtype}', data['analysis_data'][Dtype], timeout=60)  # кешуємо на 60 секунд
            return result
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FastAPI: {e}")
    return []

def api_event_data(request):
    summary_by_date = get_logs_data_from_api('summary_by_date')

    print(summary_by_date)

    data = {"labels": [], 'values': []}
    for col in summary_by_date:
        data['labels'].append(col[0])
        data['values'].append(col[1])

    print(data)

    # data = {
    #     "labels": ["12/03", "13/03", "14/03", "15/03", "16/03", "17/03", "18/03"],
    #     "values": [15, 10, 13, 16, 14, 13, 11]
    # }

    return JsonResponse(data)

def api_logs(request):
    logs = get_logs_data_from_api('get_last_log_data')
    print(logs)

    # logs = [
    #     "22-04-2025 12:53:41 | 168.132.14.148 | Malicious IP Address",
    #     "22-04-2025 12:53:41 | 164.112.14.189 | Malicious IP Address",
    #     "22-04-2025 12:53:41 | 112.132.11.56 | Malicious IP Address",
    #     "22-04-2025 12:53:41 | 176.13.12.113 | GET key_name.txt",
    #     "22-04-2025 12:53:41 | 111.111.11.111 | Malicious IP Address"
    # ]

    return JsonResponse({"logs": logs})

def api_top_requests(request):
    top_requests = get_logs_data_from_api('summary_for_gets_by_IP')
    print(top_requests)


    # top_requests = [
    #     {"ip": "176.13.12.113", "count": 5},
    #     {"ip": "164.112.14.189", "count": 4},
    #     {"ip": "111.111.11.111", "count": 3},
    #     {"ip": "112.132.11.56", "count": 2}
    # ]

    return JsonResponse({"requests": top_requests})

def api_alerts(request):
    # alerts = get_logs_data_from_api('get_malicious_ip_list')

    alerts = get_alert_data_from_api()
    print(alerts)

    str_alerts = []
    for el in alerts:
        str_alerts.append(' '.join([el['timestamp'], '-', f"{el['message']}:", el['trigger']]))

    print(str_alerts)
    return JsonResponse({"alerts": str_alerts})



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



# from django.shortcuts import render
# from django.http import JsonResponse
# import requests

# def dashboard(request):
#     return render(request, 'main/index.html')

# def api_event_data(request):
#     try:
#         response = requests.get("http://localhost:8000/api/analyze", timeout=60)
#         if response.status_code == 200:
#             data = response.json()
#             analysis_data = data.get('analysis_data', {})
#             summary_by_date = analysis_data.get('summary_by_date', [])

#             labels = [item[0] for item in summary_by_date]
#             values = [item[1] for item in summary_by_date]

#             return JsonResponse({"labels": labels, "values": values})
#     except requests.exceptions.RequestException as e:
#         print(f"Error connecting to FastAPI: {e}")
    
#     return JsonResponse({"labels": [], "values": []})

# def api_logs(request):
#     logs = [
#         "22-04-2025 12:53:41 | 168.132.14.148 | Malicious IP Address",
#         "22-04-2025 12:53:41 | 164.112.14.189 | Malicious IP Address",
#     ]
#     return JsonResponse({"logs": logs})


# def api_top_requests(request):
#     # top_requests = get_logs_data_from_api('summary_for_gets_by_IP')

#     top_requests = [
#         {"ip": "176.13.12.113", "count": 5},
#         {"ip": "164.112.14.189", "count": 4},
#         {"ip": "111.111.11.111", "count": 3},
#         {"ip": "112.132.11.56", "count": 2}
#     ]

#     return JsonResponse({"requests": top_requests})


# def api_alerts(request):
#     alerts = [
#         "17/03/2025 11:20:00 - Malicious IP address detected: 112.132.11.56",
#     ]
#     return JsonResponse({"alerts": alerts})
