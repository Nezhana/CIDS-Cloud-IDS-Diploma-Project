import re
import pandas as pd
import os
from datetime import datetime
import boto3


# s3_client = boto3.client('s3')
# bucket = 'my-logging-test-bucket-snizhana'
# prefix = 'logs/'


# log_objects = []

# paginator = s3_client.get_paginator('list_objects_v2')
# operation_parameters = {'Bucket': bucket}
# page_iterator = paginator.paginate(**operation_parameters)
# # page_iterator = paginator.paginate(Bucket = bucket, Prefix = 'demo-cf-origin')
# for page in page_iterator:
#     # print(page['Contents'])
#     key_list = page['Contents']
#     for key in key_list:
#         log_objects.append(key['Key'])


# log_data = []
# for log_key in log_objects:
#     log_data.append(pd.read_csv('s3://' + bucket + '/' + log_key, sep = " ", names=['Bucket_Owner', 'Bucket', 'Time', 'Time_Offset', 'Remote_IP', 'Requester_ARN/Canonical_ID',
#                'Request_ID',
#                'Operation', 'Key', 'Request_URI', 'HTTP_status', 'Error_Code', 'Bytes_Sent', 'Object_Size',
#                'Total_Time',
#                'Turn_Around_Time', 'Referrer', 'User_Agent', 'Version_Id', 'Host_Id', 'Signature_Version',
#                'Cipher_Suite',
#                'Authentication_Type', 'Host_Header', 'TLS_version'],
#         usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]))
    
# df = pd.concat(log_data)
# df.info() 

# print(df[(df['Operation'] == 'REST.GET.OBJECT')]['Key'].value_counts())


# -------------------------------------------------------------------------------


# def parse_s3_log(file_path):
#     # Очікувана кількість полів у кожному записі (як у тебе — 25 рядків = 1 лог-запис)
#     expected_fields = 25

#     # Імена колонок (налаштовані відповідно до твоїх даних)
#     columns = [
#         'Bucket_Owner', 'Bucket', 'Time', 'Time_Offset', 'Remote_IP', 'Requester_ARN/Canonical_ID', 
#         'Request_ID', 'Operation', 'Key', 'Request_URI', 'HTTP_status', 'Error_Code',
#         'Bytes_Sent', 'Object_Size', 'Total_Time', 'Turn_Around_Time', 'Referrer',
#         'User_Agent', 'Version_Id', 'Host_Id', 'Signature_Version', 'Cipher_Suite',
#         'Authentication_Type', 'Host_Header', 'TLS_version'
#     ]

#     # Читання файлу
#     with open(file_path, 'r') as f:
#         lines = [line.strip() for line in f if line.strip()]  # пропускаємо порожні рядки

#     # Перевірка кількості рядків
#     if len(lines) % expected_fields != 0:
#         raise ValueError(f"Log file has {len(lines)} lines, which is not a multiple of {expected_fields}. "
#                          "Possible malformed log.")

#     # Групуємо в блоки по 25 рядків
#     log_entries = [lines[i:i+expected_fields] for i in range(0, len(lines), expected_fields)]

#     # Створюємо DataFrame
#     df = pd.DataFrame(log_entries, columns=columns)

#     return df

# df = parse_s3_log('logs_example.txt')
# print(df.head())
# df.info()


# -------------------------------------------------------------------------------


# import requests
# import ipaddress

# url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'
# response = requests.get(url)

# if response.status_code == 200:
#     lines = response.text.strip().splitlines()
    
#     ip_set = set()
#     for line in lines:
#         line = line.strip()
#         if not line or line.startswith('#'):
#             continue
#         try:
#             ip_str = line.split()[0]  # Take only the first part (IP/CIDR)
#             network = ipaddress.ip_network(ip_str, strict=False)
#             ip_set.add(network)
#         except ValueError:
#             print(f"Invalid line skipped: {line}")

#     print(f"✅ Parsed {len(ip_set)} IP ranges")

#     # Example: Print first 5
#     for i, net in enumerate(sorted(ip_set)[:5]):
#         print(f"{i+1}. {net}")

#     # Example: Check if an IP is in the list
#     # test_ip = ipaddress.ip_address('1.1.1.1')
#     # for net in ip_set:
#     #     if test_ip in net:
#     #         print(f"{test_ip} is in {net}")
# else:
#     print("❌ Failed to fetch file.")

# print(sorted(ip_set)[0], type(sorted(ip_set)[0]), type(sorted(ip_set)), str(sorted(ip_set)[0])[:-3])