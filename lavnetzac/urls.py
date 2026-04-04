from django.urls import path
from . import views

app_name = 'lavnetzac'

urlpatterns = [
    path('', views.home, name='home'),
    path('graficas/', views.graficas_page, name='graficas'),
    path('mapa-solar/', views.mapa_solar_page, name='mapa_solar'),
    path('descargar/', views.descargar_muestra, name='descargar'),
    # API
    path('api/timeseries', views.api_timeseries, name='api_timeseries'),
    path('api/events', views.api_events, name='api_events'),
    path('api/export', views.api_export, name='api_export'),
    path('api/radob-data', views.api_radob_data, name='api_radob_data'),
]
