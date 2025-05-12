from fastapi import APIRouter
from app.services.S3_Alerts_Generator import Alert_Generator
from app.services.S3_Logs_Collector import Logs_Collector

router = APIRouter()

@router.get("/alerts")
def get_alerts():
    logs_collector = Logs_Collector()
    logs_collector.set_logs_bucket(logs_collector.get_logs_bucket())
    logs_df = logs_collector.get_log_data_in_DF()
    logs_alert = Alert_Generator(logs_df)

    alert_data = logs_alert.get_alert_data()
    # formated_alert_data = {}
    # for key, item in alert_data.items():
    #     formated_alert_data[key] = item.to_dict()
    
    # return {"alert_data": formated_alert_data}
    return {"alert_data": alert_data}

