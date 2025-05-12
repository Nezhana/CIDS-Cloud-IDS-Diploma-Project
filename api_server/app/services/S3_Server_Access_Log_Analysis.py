import re
import pandas as pd
import os
from datetime import datetime
import numpy as np
import natsort

import requests
import ipaddress


class Logs_Analysis():
    def __init__(self, logs_df):
        self.logs_df = logs_df

    def check_for_malicious_ip(self):
    
        mal_ip_list = get_malicious_ip_address_list()

        ind_list = []
        ind = 0
        for remote_ip in self.logs_df['Remote_IP']:
            # if remote_ip in mal_ip_list:
            #     # print(f'{remote_ip} is a malicious ip address!')
            #     ind_list.append(ind)
            # else:
            #     # print(f'{remote_ip} is NOT a malicious ip address!')
            #     pass
            # ind+=1
        
            test_ip = ipaddress.ip_address(remote_ip)
            for net in mal_ip_list:
                if test_ip in net:
                    # print(f"{test_ip} is in {net}")
                    ind_list.append(ind)
            ind+=1
        
        return ind_list
    
    def get_malicious_ip_list(self):
        mal_ip_ind_list = self.check_for_malicious_ip()
        malicious_ip_lst = []
        if mal_ip_ind_list:
            for ind in mal_ip_ind_list:
                mal_ip_data = str(self.logs_df.iloc[[ind]][['Time', 'Remote_IP']]).split('\n')[1]
                malicious_ip_lst.append(mal_ip_data.split()[1:])
        else:
            print('No mal IP addresses detected.')
        return malicious_ip_lst


    def summary_for_gets_by_IP(self):
        res_lst = df_result_to_list(self.logs_df[(self.logs_df['Operation'] == 'REST.GET.OBJECT')]['Remote_IP'].value_counts())
        formated_res_lst = []
        for res in res_lst:
            formated_res = ' | '.join(res.split())
            formated_res += ' requests'
            formated_res_lst.append(formated_res)
        return formated_res_lst

    def summary_by_date(self):
        res_lst = df_result_to_list(self.logs_df['Time'].value_counts())
        sum_by_date_lst = []
        for res in res_lst:
            date = datetime.strptime(res.split()[0], "[%d/%b/%Y:%H:%M:%S")
            res = res.split()
            res[0] = date.strftime('%d/%m/%y')
            sum_by_date_lst.append(res)
        return sum_by_date_lst
    
    
    def summary_by_date_v2(self):
        date_list = []
        sum_by_date_dct = {}
        for date in self.logs_df['Time']:
            fdate = datetime.strptime(date, "[%d/%b/%Y:%H:%M:%S")
            fix_date = fdate.strftime('%d/%m/%y')
            if fix_date not in date_list:
                date_list.append(fix_date)
                sum_by_date_dct[fix_date] = 0
            sum_by_date_dct[fix_date] += 1
        sum_by_date_lst = [[ndate, str(val)] for ndate, val in sum_by_date_dct.items()]
        return sum_by_date_lst
    
    
    def get_last_log_data(self):
        sorted_by_date = self.logs_df.sort_values(by='Time', ascending=False, key=lambda series: pd.Series([datetime.strptime(t, "[%d/%b/%Y:%H:%M:%S") for t in series]))
        first_seven_logs = sorted_by_date.head(7)
        logs_lst = df_result_to_list(first_seven_logs[['Time', 'Remote_IP', 'Operation']])
        formated_logs = []
        for log in logs_lst:
            fix_date = datetime.strptime(log.split()[1], "[%d/%b/%Y:%H:%M:%S")
            formated_log = log.split()
            formated_log.pop(0)
            formated_log[0] = fix_date.strftime('%d-%m-%Y %H:%M:%S')
            formated_logs.append(' | '.join(formated_log))
        return formated_logs


def TEMPORARY_parse_s3_log(file_path):
    # Очікувана кількість полів у кожному записі (як у тебе — 24 рядків = 1 лог-запис)
    expected_fields = 25

    # Імена колонок (налаштовані відповідно до твоїх даних)
    columns = [
        'Bucket_Owner', 'Bucket', 'Time', 'Time_Offset', 'Remote_IP', 'Requester_ARN/Canonical_ID', 
        'Request_ID', 'Operation', 'Key', 'Request_URI', 'HTTP_status', 'Error_Code',
        'Bytes_Sent', 'Object_Size', 'Total_Time', 'Turn_Around_Time', 'Referrer',
        'User_Agent', 'Version_Id', 'Host_Id', 'Signature_Version', 'Cipher_Suite',
        'Authentication_Type', 'Host_Header', 'TLS_version'
    ]

    files = ['logs_example.txt', 'logs_example.txt', 'logs_example_2.txt', 'logs_example_2.txt', 'logs_example_3.txt', 'logs_example_2.txt', 'logs_example_3.txt']

    logs_final = []

    for file_path in files:

        # Читання файлу
        with open(file_path, 'r') as f:
            lines = []
            for line in f:
                striped_line = line.strip()
                if line[0] == '[':
                    splited_line = striped_line.split()
                    lines += [subline.replace('[', '').replace(']', '') for subline in splited_line]
                else:
                    lines.append(striped_line)
                
            # lines = [line.strip().split() for line in f if line.strip()]  # пропускаємо порожні рядки
            # print(lines)

        # Перевірка кількості рядків
        if len(lines) % expected_fields != 0:
            raise ValueError(f"Log file has {len(lines)} lines, which is not a multiple of {expected_fields}. "
                            "Possible malformed log.")

        # Групуємо в блоки по 25 рядків
        log_entries = [lines[i:i+expected_fields] for i in range(0, len(lines), expected_fields)]

        logs_final.append(*log_entries)

    # Створюємо DataFrame
    df = pd.DataFrame(logs_final, columns=columns)

    return df

def get_malicious_ip_address_list():
    url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/ipsum.txt'
    response = requests.get(url)

    if response.status_code == 200:
        lines = response.text.strip().splitlines()
        
        ip_set = set()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                ip_str = line.split()[0]  # Take only the first part (IP/CIDR)
                network = ipaddress.ip_network(ip_str, strict=False)
                ip_set.add(network)
            except ValueError:
                print(f"Invalid line skipped: {line}")

        print(f"✅ Parsed {len(ip_set)} IP ranges")

        # # Example: Print first 5
        # for i, net in enumerate(sorted(ip_set)[:5]):
        #     print(f"{i+1}. {net}")

        # # Example: Check if an IP is in the list
        # test_ip = ipaddress.ip_address('218.92.0.218')
        # for net in ip_set:
        #     if test_ip in net:
        #         print(f"{test_ip} is in {net}")
    else:
        print("❌ Failed to fetch file.")
    
    # print(sorted(ip_set)[0], type(sorted(ip_set)[0]), type(sorted(ip_set)), str(sorted(ip_set)[0])[:-3])

    return sorted(ip_set)


def df_result_to_list(df_res):
    result = str(df_res).split('\n')[1:-1]
    return result

def df_result_to_str(df_res):
    result = '\n'.join(str(df_res).split('\n')[1:-1])
    return result



# def main():

#     logs_df = TEMPORARY_parse_s3_log('logs_example.txt')
#     print(logs_df[['Time', 'Remote_IP', 'Operation']])

#     logs_analysis = Logs_Analysis(logs_df)

#     # # print(str(logs_analysis.summary_for_gets_by_IP()).split()[1:3])
#     # print(logs_analysis.summary_for_gets_by_IP())
#     print()
#     print(logs_analysis.summary_by_date())
#     print(logs_analysis.get_last_log_data())
#     print(logs_analysis.summary_for_gets_by_IP())
#     print(logs_analysis.get_malicious_ip_list())







# if __name__ == "__main__":
#     main()