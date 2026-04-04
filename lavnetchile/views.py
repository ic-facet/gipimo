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
instalado en Chile, una antena receptora de radio que forma parte de la Red
Latinoamericana de Muy Baja Frecuencia (LAVNet-Chile), extendiendo así la cobertura de
la Red VLF Sudamericana.

Esta estación receptora está diseñada para detectar cambios sutiles en la fase y amplitud de
ondas electromagnéticas en el rango de 15 a 48 kHz, transmitidas por estaciones distribuidas
globalmente. Dichas ondas, al propagarse en la guía de ondas Tierra-ionosfera, son reflejadas
principalmente por la capa D de la ionosfera, permitiendo que la antena registre perturbaciones
causadas por variaciones en la densidad electrónica y en la estructura de esta región. Gracias
a su alta sensibilidad y ubicación estratégica, LAVNet-Chile constituye una herramienta
valiosa para estudiar los procesos dinámicos de la ionosfera y monitorear fenómenos asociados
a la actividad solar y geomagnética en América del Sur.'''

	return render(request, 'lavnetchile/home.html', {
		'site_title': 'LAVNet-Chile',
		'description': description,
		'api_base_url': '/lavnet-chile/api',
	})


def graficas_page(request):
	return render(request, 'lavnetchile/graficas.html', {
		'site_title': 'LAVNet-Chile - Gráficas',
		'api_base_url': '/lavnet-chile/api',
	})


def mapa_solar_page(request):
	return render(request, 'lavnetchile/mapa_solar.html', {
		'site_title': 'LAVNet-Chile - Mapa Solar',
	})


def descargar_muestra(request):
	return render(request, 'lavnetchile/descargar.html', {
		'site_title': 'LAVNet-Chile - Descargar muestra',
		'api_base_url': '/lavnet-chile/api',
	})

def graficas_vlf_page(request):
    return render(request, 'lavnetchile/graficas_vlf.html', {
        'site_title': 'LAVNet-Chile - Gráficas VLF',
        'api_base_url': '/lavnet-chile/api',
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
    """Proxy para obtener datos de Chile desde el servidor de Node.js del profe."""
    try:
        fechainicial = request.POST.get('fechainicial')
        fechafinal = request.POST.get('fechafinal')
        
        if not fechainicial or not fechafinal:
            return JsonResponse({'error': 'Faltan parámetros de fecha'}, status=400)
        
        # Endpoint específico para Chile (UNACH)
        endpoint_profe = "http://idawis-uaz.ddns.net:3000/getUNACHEFMDate"
        
        # Payload que espera el servidor de Node.js
        payload = {
            'fechainicial': fechainicial,
            'fechafinal': fechafinal
        }
        
        # Hacemos la petición POST al servidor del profe
        respuesta = requests.post(endpoint_profe, data=payload, timeout=20)
        
        if respuesta.status_code != 200:
            return JsonResponse({'error': f'Error en servidor remoto: {respuesta.status_code}'}, status=502)
            
        datos = respuesta.json()
        return JsonResponse(datos, safe=False)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'No se pudo conectar al servidor del profe: {str(e)}'}, status=503)
    except Exception as e:
        return JsonResponse({'error': f'Error interno en Django: {str(e)}'}, status=500)
