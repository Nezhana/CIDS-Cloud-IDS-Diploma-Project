
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


class Alert_Generator():
    def __init__(self, logs_df):
        self.KNOWN_USER_AGENTS = ['Mozilla', 'Chrome', 'Safari', 'Edge', 'Postman']
        self.df = logs_df


    def detect_request_rate_anomalies(self, df, threshold_z=3):
        # Переконаймося, що timestamp — це datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Створимо копію з datetime-індексом
        df_with_index = df.set_index('timestamp')

        # Групування по IP і часах
        req_counts = (
            df_with_index
            .groupby('remote_IP')
            .resample('1min')
            .size()
            .reset_index()
            .rename(columns={0: 'count'})
        )

        # Статистика
        stats = req_counts.groupby('remote_IP')['count'].agg(['mean', 'std']).reset_index()
        
        req_counts = req_counts.merge(stats, on='remote_IP')
        req_counts['z_score'] = (req_counts['count'] - req_counts['mean']) / req_counts['std']
        
        anomalies = req_counts[req_counts['z_score'] > threshold_z]
        return anomalies[['remote_IP', 'timestamp', 'count', 'z_score']]


    def detect_suspicious_user_agents(self, df):
        def is_known(ua):
            return any(known in ua for known in self.KNOWN_USER_AGENTS)
        
        df['suspicious_ua'] = df['UserAgent'].apply(lambda x: not is_known(x))
        return df[df['suspicious_ua']][['timestamp', 'remote_IP', 'UserAgent']]


    def detect_off_hours_activity(self, df, start=0, end=5):
        df['hour'] = df['timestamp'].dt.hour
        return df[(df['hour'] >= start) & (df['hour'] <= end)][['timestamp', 'remote_IP', 'UserAgent']]

    def study_model(self):
        df = pd.DataFrame()

        sus_df = pd.read_csv("app/services/suspicious_log.csv")
        with_sus_df = pd.concat([self.df, sus_df]).reset_index(drop=True)

        ind = 0
        for time in with_sus_df["Time"]:
            try:
                fix_date = datetime.strptime(time, "[%d/%b/%Y:%H:%M:%S")
                with_sus_df.loc[ind, "Time"] = fix_date.strftime('%d-%m-%Y %H:%M:%S')
            except:
                continue
            ind += 1


        # Побудова ознак для моделі
        df["timestamp"] = pd.to_datetime(with_sus_df["Time"], dayfirst=True)
        df["minute"] = df["timestamp"].dt.floor("min")
        df["remote_IP"] = with_sus_df["Remote_IP"]
        df["req_per_minute"] = df.groupby(["remote_IP", "minute"])["remote_IP"].transform("count")
        df["hour"] = df["timestamp"].dt.hour
        df["useragent_len"] = with_sus_df["User_Agent"].apply(len)
        df["UserAgent"] = with_sus_df["User_Agent"]
        df["Method"] = with_sus_df["Operation"]

        # Вибираємо ознаки
        features = df[["req_per_minute", "hour", "useragent_len"]]

        # Навчання моделі
        model = IsolationForest(contamination=0.05, random_state=42)
        df["anomaly"] = model.fit_predict(features)
        # print(df["anomaly"])
        # print()

        # Виділення аномалій
        anomalies = df[df["anomaly"] == -1]
        # print(anomalies)

        return {
            'df': df,
            'anomalies': anomalies[["timestamp", "remote_IP", "UserAgent", "Method", "req_per_minute", "anomaly"]]
        }

    def get_alert_data(self):

        new_df = self.study_model()['df']

        anomalous_rate = self.detect_request_rate_anomalies(new_df)
        suspicious_uas = self.detect_suspicious_user_agents(new_df)
        night_activity = self.detect_off_hours_activity(new_df)

        print("🔺 Аномальна частота:")
        print(anomalous_rate)

        print("\n🔺 Підозрілі User-Agent-и:")
        print(suspicious_uas)

        print("\n🔺 Нічна активність:")
        print(night_activity)

        alerts = {
            "anomalous_rate": anomalous_rate.to_dict(),
            "suspicious_uas": suspicious_uas.to_dict(),
            "night_activity": night_activity.to_dict()
            }
        
        formated_and_sorted_alerts = format_and_sort_alerts(alerts)

        # return {"anomalous_rate": anomalous_rate, "suspicious_uas": suspicious_uas, "night_activity": night_activity}
        return formated_and_sorted_alerts

    
def anomalous_rate_finder(alerts):
    print(alerts)
    anomalies = []
    ind = 0
    for key, item in alerts['z_score'].items():
        if item >= 90.0:
            # date = ' '.join(alerts['timestamp'][key].split('T')).replace('-', '/')
            date = alerts['timestamp'][key].strftime('%d/%m/%Y %H:%M:%S')
            message = 'DDoS Warning'
            trigger = f"{(alerts['remote_IP'][key])} exceeded requests"
            anomalies.append({ind: [ date, message, trigger ]})
            ind += 1
    return anomalies

def suspicious_uas_formater(alerts):
    anomalies = []
    ind = 0
    for key, item in alerts['timestamp'].items():
        # date = ' '.join(alerts['timestamp'][key].split('T')).replace('-', '/')
        date = alerts['timestamp'][key].strftime('%d/%m/%Y %H:%M:%S')
        message = f"Access Denied: {(alerts['remote_IP'][key])}"
        trigger = f"Unknown user agent: {(alerts['UserAgent'][key])}"
        anomalies.append({ind: [ date, message, trigger ]})
        ind += 1
    return anomalies


def night_activity_formater(alerts):
    anomalies = []
    ind = 0
    for key, item in alerts['timestamp'].items():
        # date = ' '.join(alerts['timestamp'][key].split('T')).replace('-', '/')
        date = alerts['timestamp'][key].strftime('%d/%m/%Y %H:%M:%S')
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
    # sorted_alerts = sorted(formated_alerts, key=lambda x: x[0])
    sorted_alerts = sorted(formated_alerts, key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H:%M:%S"))
    # print(sorted_alerts)

    result = []
    ind = 1
    for el in sorted_alerts:
        result.append({'ID': ind, 'timestamp': el[0], 'message': el[1], 'trigger': el[2]})
        ind += 1
    
    return result

