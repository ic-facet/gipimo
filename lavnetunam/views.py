from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
import csv
import io
from datetime import datetime, timezone
from django.views.decorators.csrf import csrf_exempt
import requests
import os
from datetime import datetime, timedelta


def home(request):
	description = '''La ionosfera, una región de la atmósfera terrestre ionizada que se extiende aproximadamente entre 60 y 1000 km de altitud, responde de manera sensible a eventos solares y geomagnéticos repentinos, como las tormentas solares y las eyecciones de masa coronal. El estudio
de estas respuestas es fundamental para caracterizar la dinámica de las capas ionosféricas
inferiores y para predecir fenómenos que pueden afectar las comunicaciones radioeléctricas,
los sistemas de navegación y las redes de distribución eléctrica. Con este propósito, se ha
instalado en la UNAM, México, una antena receptora de radio que forma parte de la Red
Latinoamericana de Muy Baja Frecuencia (LAVNet-UNAM), extendiendo así la cobertura de
la Red VLF en México.

Esta estación receptora está diseñada para detectar cambios sutiles en la fase y amplitud de
ondas electromagnéticas en el rango de 15 a 48 kHz, transmitidas por estaciones distribuidas
globalmente. Dichas ondas, al propagarse en la guía de ondas Tierra-ionosfera, son reflejadas
principalmente por la capa D de la ionosfera, permitiendo que la antena registre perturbaciones
causadas por variaciones en la densidad electrónica y en la estructura de esta región. Gracias
a su alta sensibilidad y ubicación estratégica, LAVNet-UNAM constituye una herramienta
valiosa para estudiar los procesos dinámicos de la ionosfera y monitorear fenómenos asociados
a la actividad solar y geomagnética.'''

	return render(request, 'lavnetunam/home.html', {
		'site_title': 'LAVNet-UNAM',
		'description': description,
		'api_base_url': '/lavnet-unam/api',
	})


def graficas_page(request):
	return render(request, 'lavnetunam/graficas.html', {
		'site_title': 'LAVNet-UNAM - Gráficas',
		'api_base_url': '/lavnet-unam/api',
	})


def mapa_solar_page(request):
	return render(request, 'lavnetunam/mapa_solar.html', {
		'site_title': 'LAVNet-UNAM - Mapa Solar',
	})


def descargar_muestra(request):
	return render(request, 'lavnetunam/descargar.html', {
		'site_title': 'LAVNet-UNAM - Descargar muestra',
		'api_base_url': '/lavnet-unam/api',
	})

def vista_callisto(request):
    fecha_seleccionada = request.GET.get('fecha', '2026-03-06')
    nombre_carpeta = f"{fecha_seleccionada}_INDIVIDUALES"
    
    ruta_dir = os.path.join(
        settings.BASE_DIR, 
        'lavnetunam', 'static', 'lavnetunam', 'scripts', 'resultados_mexico_lance', 
        nombre_carpeta
    )
    ruta_estatica_imgs = f"lavnetunam/scripts/resultados_mexico_lance/{nombre_carpeta}"

    bloques_finales = []
    mensaje_error = None

    if os.path.exists(ruta_dir):
        todos_los_archivos = sorted(os.listdir(ruta_dir))
        espectros = [f for f in todos_los_archivos if f.endswith('_ESPECTRO.png')]
        
        for arch in espectros:
            prefijo = arch.replace('_ESPECTRO.png', '')
            partes = prefijo.split('_')
            hora_str = partes[2] if len(partes) > 2 else "Sin hora"
            
            # Formato UTC
            hora_formateada = f"{hora_str[:2]}:{hora_str[2:4]}:{hora_str[4:]}"
            
            # CÁLCULO DE HORA LOCAL (Hora Centro México = UTC - 6)
            hora_local_formateada = "N/A"
            if hora_str != "Sin hora" and len(hora_str) == 6:
                try:
                    utc_time = datetime.strptime(hora_str, "%H%M%S")
                    local_time = utc_time - timedelta(hours=6)
                    hora_local_formateada = local_time.strftime("%H:%M:%S")
                except ValueError:
                    pass

            bloques_finales.append({
                'hora': hora_formateada,
                'hora_local': hora_local_formateada, # <--- Enviamos la nueva hora al HTML
                'id_bloque': prefijo,
                'url_espectro': f"{ruta_estatica_imgs}/{arch}",
                'url_curva': f"{ruta_estatica_imgs}/{prefijo}_CURVA_LUZ.png",
                'url_frecuencia': f"{ruta_estatica_imgs}/{prefijo}_ESPECTRO_FREC.png"
            })
    else:
        mensaje_error = f"No existen gráficas generadas para el día {fecha_seleccionada}."

    return render(request, 'lavnetunam/callisto_view.html', {
        'bloques': bloques_finales,
        'fecha': fecha_seleccionada,
        'error': mensaje_error
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
	"""Proxy para obtener datos de radob desde el servidor externo (UNAM)."""
	try:
		fechainicial = request.POST.get('fechainicial')
		fechafinal = request.POST.get('fechafinal')
		estacion = request.POST.get('estacion')
		
		if not fechainicial or not fechafinal or not estacion:
			return JsonResponse({'error': 'Faltan parámetros fechainicial, fechafinal o estacion'}, status=400)
		
		# Diccionario de rutas para la UNAM
		rutas_unam = {
			'NAA': 'http://idawis-uaz.ddns.net:3000/getUNAMNAADate',
			'NDK': 'http://idawis-uaz.ddns.net:3000/getUNAMNDKDate',
			'NLK': 'http://idawis-uaz.ddns.net:3000/getUNAMNLKDate',
			'NPM': 'http://idawis-uaz.ddns.net:3000/getUNAMNPMDate',
			'NWC': 'http://idawis-uaz.ddns.net:3000/getUNAMNWCDate',
			'NAU': 'http://idawis-uaz.ddns.net:3000/getUNAMNAUDate'
		}
		
		endpoint = rutas_unam.get(estacion)
		
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