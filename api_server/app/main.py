from fastapi import FastAPI
from app.routes import Logs_Collector, Logs_Analyzer, Logs_Alerts

app = FastAPI()

app.include_router(Logs_Collector.router, prefix="/api")
app.include_router(Logs_Analyzer.router, prefix="/api")
app.include_router(Logs_Alerts.router, prefix="/api")
