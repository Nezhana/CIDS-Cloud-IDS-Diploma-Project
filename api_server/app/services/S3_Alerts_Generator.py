
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

        ind = 0
        for time in self.df["Time"]:
            print(time)
            try:
                fix_date = datetime.strptime(time, "[%d/%b/%Y:%H:%M:%S")
                self.df.loc[ind, "Time"] = fix_date.strftime('%d-%m-%Y %H:%M:%S')
            except:
                continue
            ind += 1


        # Побудова ознак для моделі
        df["timestamp"] = pd.to_datetime(self.df["Time"], dayfirst=True)
        df["minute"] = df["timestamp"].dt.floor("min")
        df["remote_IP"] = self.df["Remote_IP"]
        df["req_per_minute"] = df.groupby(["remote_IP", "minute"])["remote_IP"].transform("count")
        df["hour"] = df["timestamp"].dt.hour
        df["useragent_len"] = self.df["User_Agent"].apply(len)
        df["UserAgent"] = self.df["User_Agent"]
        df["Method"] = self.df["Operation"]

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

        return {"anomalous_rate": anomalous_rate, "suspicious_uas": suspicious_uas, "night_activity": night_activity}

