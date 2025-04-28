from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/event-data/', views.api_event_data, name='api_event_data'),
    path('api/logs/', views.api_logs, name='api_logs'),
    path('api/top-requests/', views.api_top_requests, name='api_top_requests'),
    path('api/alerts/', views.api_alerts, name='api_alerts'),
]