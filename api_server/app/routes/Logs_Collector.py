from fastapi import APIRouter
from app.services.S3_Logs_Collector import Logs_Collector

router = APIRouter()

@router.get("/logs")
def get_logs():
    logs_collector = Logs_Collector()
    logs_collector.set_logs_bucket(logs_collector.get_logs_bucket())
    df = logs_collector.get_log_data_in_DF()
    logs = df.to_dict()
    return {"logs": logs}
