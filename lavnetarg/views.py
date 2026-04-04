from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
import csv
import io
from datetime import datetime, timezone
from django.views.decorators.csrf import csrf_exempt
import requests


def home(request):
	description = '''Bienvenidos al sitio de la estación receptora LAVNet-Ar (Latin America Very Low Frequency Network - Argentina). Este es uno de los 5 sitios en América Latina de la red LAVNet que realizan sondeo ionosférico en baja frecuencia para estudiar la dinámica de la región D ante eventos perturbativos de origen terrestre y extraterrestre.

El personal a cargo de este sitio pertenece al Departamento de Física, el Departamento de Geofísica y Geodesia y al Laboratorio de Telecomunicaciones de la Facultad de Ciencias Exactas y Tecnología de la Universidad Nacional de Tucumán (26°49'00"S 65°13'00"O).'''

	return render(request, 'lavnetarg/home.html', {
		'site_title': 'LAVNet-Argentina',
		'description': description,
		'api_base_url': '/lavnet-arg/api',
		'latitude': -26.8167,
		'longitude': -65.2167,
	})


def graficas_page(request):
	return render(request, 'lavnetarg/graficas.html', {
		'site_title': 'LAVNet-Argentina - Gráficas',
		'api_base_url': '/lavnet-arg/api',
	})


def mapa_solar_page(request):
	return render(request, 'lavnetarg/mapa_solar.html', {
		'site_title': 'LAVNet-Argentina - Mapa Solar',
		'latitude': -26.8167,
		'longitude': -65.2167,
		'location_name': 'Tucumán, Argentina',
	})


def descargar_muestra(request):
	return render(request, 'lavnetarg/descargar.html', {
		'site_title': 'LAVNet-Argentina - Descargar muestra',
		'api_base_url': '/lavnet-arg/api',
	})


@require_GET
def api_timeseries(request):
	"""Stub: endpoint /api/timeseries.
	Actualmente no devuelve datos reales; esta vista es un placeholder
	listo para integrar con la API real más adelante.
	"""
	return JsonResponse({'error': 'not implemented', 'message': 'api_timeseries is a stub for now'}, status=501)


@require_GET
def api_events(request):
	"""Stub: endpoint /api/events. Placeholder para futuros datos reales."""
	return JsonResponse({'error': 'not implemented', 'message': 'api_events is a stub for now'}, status=501)


@require_GET
def api_export(request):
	"""Genera un CSV o XLSX con la muestra solicitada entre start/end."""
	start = request.GET.get('start')
	end = request.GET.get('end')
	fmt = request.GET.get('format', 'csv')
	# Mantener export como stub hasta integrar la API real.
	return JsonResponse({'error': 'not implemented', 'message': 'api_export is a stub for now'}, status=501)


@csrf_exempt
@require_POST
def api_radob_data(request):
	"""Proxy para obtener datos de radob desde el servidor externo."""
	try:
		fechainicial = request.POST.get('fechainicial')
		fechafinal = request.POST.get('fechafinal')
		
		if not fechainicial or not fechafinal:
			return JsonResponse({'error': 'Faltan parámetros fechainicial o fechafinal'}, status=400)
		
		# Argentina no tiene datos disponibles para ninguna estación
		# Devolver array vacío para simular respuesta sin datos
		return JsonResponse([], safe=False)
			
	except Exception as e:
		return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
