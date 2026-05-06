from django.shortcuts import render


def index(request):
    stations = [
        {
            'name': 'LAVNet-Ar',
            'subtitle': 'Argentina',
            'location': 'Tucumán, Argentina',
            'coords': '26°49\'00"S 65°13\'00"O',
            'description': 'Estación receptora a cargo del Departamento de Física, Departamento de Geofísica y Geodesia y el Laboratorio de Telecomunicaciones de la FACET-UNT.',
            'url_name': 'lavnetarg:home',
            'color': '#0d47a1',
            'flag': 'AR',
        },
        {
            'name': 'LAVNet-Zac',
            'subtitle': 'Zacatecas, México',
            'location': 'Zacatecas, México',
            'coords': '22°46\'N 102°35\'O',
            'description': 'Estación receptora ubicada en Zacatecas, México, parte de la red latinoamericana LAVNet.',
            'url_name': 'lavnetzac:home',
            'color': '#1b5e20',
            'flag': 'MX',
        },
        {
            'name': 'LAVNet-Chile',
            'subtitle': 'Chile',
            'location': 'Chile',
            'coords': '',
            'description': 'Estación receptora chilena de la red LAVNet, operada en colaboración con la UNACH.',
            'url_name': 'lavnetchile:home',
            'color': '#b71c1c',
            'flag': 'CL',
        },
        {
            'name': 'LAVNet-UNAM',
            'subtitle': 'México (UNAM)',
            'location': 'Ciudad de México, México',
            'coords': '',
            'description': 'Estación operada por el Instituto de Geofísica de la UNAM, incluye también datos del espectrómetro Callisto.',
            'url_name': 'lavnetunam:home',
            'color': '#4a148c',
            'flag': 'MX',
        },
    ]
    return render(request, 'index.html', {'stations': stations})
