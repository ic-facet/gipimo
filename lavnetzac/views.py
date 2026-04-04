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
	description = '''La ionosfera, una región de la atmósfera terrestre ionizada que se extiende aproximadamente entre 60 y 1000 km de altitud, responde de manera sensible a eventos solares y geomagnéticos repentinos, como las tormentas solares y las eyecciones de masa coronal. El estudio
de estas respuestas es fundamental para caracterizar la dinámica de las capas ionosféricas
inferiores y para predecir fenómenos que pueden afectar las comunicaciones radioeléctricas,
los sistemas de navegación y las redes de distribución eléctrica. Con este propósito, se ha
instalado en Zacatecas, México, una antena receptora de radio que forma parte de la Red
Latinoamericana de Muy Baja Frecuencia (LAVNet-ZacMx), extendiendo así la cobertura de
la Red VLF Sudamericana al hemisferio norte.

Esta estación receptora está diseñada para detectar cambios sutiles en la fase y amplitud de
ondas electromagnéticas en el rango de 15 a 48 kHz, transmitidas por estaciones distribuidas
globalmente. Dichas ondas, al propagarse en la guía de ondas Tierra-ionosfera, son reflejadas
principalmente por la capa D de la ionosfera, permitiendo que la antena registre perturbaciones
causadas por variaciones en la densidad electrónica y en la estructura de esta región. Gracias
a su alta sensibilidad y ubicación estratégica, LAVNet-ZacMx constituye una herramienta
valiosa para estudiar los procesos dinámicos de la ionosfera y monitorear fenómenos asociados
a la actividad solar y geomagnética en latitudes medias del hemisferio norte.'''

	return render(request, 'lavnetzac/home.html', {
		'site_title': 'LAVNet-Zac-Mx',
		'description': description,
		'api_base_url': '/lavnet-zac/api',
	})


def graficas_page(request):
	return render(request, 'lavnetzac/graficas.html', {
		'site_title': 'LAVNet-Zac-Mx - Gráficas',
		'api_base_url': '/lavnet-zac/api',
	})


def mapa_solar_page(request):
	return render(request, 'lavnetzac/mapa_solar.html', {
		'site_title': 'LAVNet-Zac-Mx - Mapa Solar',
	})


def descargar_muestra(request):
	return render(request, 'lavnetzac/descargar.html', {
		'site_title': 'LAVNet-Zac-Mx - Descargar muestra',
		'api_base_url': '/lavnet-zac/api',
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
	"""Proxy para obtener datos de radob desde el servidor externo (Zacatecas/SAZ)."""
	try:
		fechainicial = request.POST.get('fechainicial')
		fechafinal = request.POST.get('fechafinal')
		estacion = request.POST.get('estacion')
		
		if not fechainicial or not fechafinal or not estacion:
			return JsonResponse({'error': 'Faltan parámetros fechainicial, fechafinal o estacion'}, status=400)
		
		# Diccionario de rutas para Zacatecas (SAZ) 
		rutas_saz = {
			'NAA': 'http://idawis-uaz.ddns.net:3000/getSAZNAADate',
			'NDK': 'http://idawis-uaz.ddns.net:3000/getSAZNDKDate',
			'NPM': 'http://idawis-uaz.ddns.net:3000/getSAZNPMDate',
			'NWC': 'http://idawis-uaz.ddns.net:3000/getSAZNWCDate',
			'NLK': 'http://idawis-uaz.ddns.net:3000/getSAZNLKDate',
			'NAU': 'http://idawis-uaz.ddns.net:3000/getSAZNAUDate'
		}
		
		endpoint = rutas_saz.get(estacion)
		
		# Si la estación no está en el diccionario, devolvemos un array vacío
		if not endpoint:
			return JsonResponse([], safe=False)
		
		# Hacer la petición al servidor externo
		response = requests.post(
			endpoint,
			data={
				'fechainicial': fechainicial,
				'fechafinal': fechafinal
			},
			timeout=30
		)
		
		if response.status_code == 200:
			return JsonResponse(response.json(), safe=False)
		else:
			return JsonResponse({'error': f'Error del servidor: {response.status_code}'}, status=response.status_code)
			
	except requests.exceptions.Timeout:
		return JsonResponse({'error': 'Timeout al conectar con el servidor'}, status=504)
	except requests.exceptions.RequestException as e:
		return JsonResponse({'error': f'Error de conexión: {str(e)}'}, status=503)
	except Exception as e:
		return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

