from fastapi import FastAPI
from app.routes import Logs_Collector, Logs_Analyzer

app = FastAPI()

app.include_router(Logs_Collector.router, prefix="/api")
app.include_router(Logs_Analyzer.router, prefix="/api")
