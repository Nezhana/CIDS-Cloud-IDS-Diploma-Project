from fastapi import APIRouter
import app.services.S3_Server_Access_Log_Analysis as analyzer
from app.services.S3_Logs_Collector import Logs_Collector

router = APIRouter()

@router.get("/analyze")
def get_analysis():
    logs_collector = Logs_Collector()
    logs_collector.set_logs_bucket(logs_collector.get_logs_bucket())
    logs_df = logs_collector.get_log_data_in_DF()
    logs_analysis = analyzer.Logs_Analysis(logs_df)

    print(logs_analysis.summary_by_date_v2())
    print(logs_analysis.get_last_log_data())
    print(logs_analysis.summary_for_gets_by_IP())
    # print(logs_analysis.get_malicious_ip_list())

    analysis_data = {
        'summary_by_date': logs_analysis.summary_by_date_v2(),
        'get_last_log_data': logs_analysis.get_last_log_data(),
        'summary_for_gets_by_IP':logs_analysis.summary_for_gets_by_IP(),
        'get_malicious_ip_list': logs_analysis.get_malicious_ip_list()}
    
    return {"analysis_data": analysis_data}

