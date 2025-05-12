from django.shortcuts import render
from django.core.cache import cache

import requests

# Create your views here.

def loglist(request):
    logs = get_logs_data_from_api()

    print(logs)

    # # ----------------------------------
    # # Обробка параметрів GET
    # sort_by = request.GET.get('sort_by')
    # filter_value = request.GET.get('filter')
    # filter_column = request.GET.get('filter_column')
    # # ----------------------------------

    data = make_logs_table(logs, 17)

    # # ----------------------------------

    # # Застосування фільтрування
    # if filter_value and filter_column and filter_column in data['headers']:
    #     index = data['headers'].index(filter_column)
    #     filtered = {}
    #     for k, row in data['values'].items():
    #         if filter_value.lower() in row[index].lower():
    #             filtered[k] = row
    #     data['values'] = filtered

    # # Застосування сортування
    # if sort_by and sort_by in data['headers']:
    #     index = data['headers'].index(sort_by)
    #     sorted_items = sorted(data['values'].items(), key=lambda x: x[1][index])
    #     data['values'] = dict(sorted_items)
    
    # # ----------------------------------

    # print(data['values'], type(data['values']))

    return render(request, 'cids_log_list/log_list.html', context=data)

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


def make_logs_table(data, log_counter):
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
