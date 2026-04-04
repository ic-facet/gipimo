# LAVNet - Dockerización

Este proyecto Django para LAVNet (Zacatecas y Argentina) está dockerizado para facilitar su despliegue.

## Requisitos previos

- Docker
- Docker Compose

## Construcción y ejecución

### Opción 1: Usando Docker Compose (Recomendado)

```bash
# Construir y levantar los contenedores
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener los contenedores
docker-compose down
```

### Opción 2: Usando Docker directamente

```bash
# Construir la imagen
docker build -t lavnet-app .

# Ejecutar el contenedor
docker run -p 8000:8000 lavnet-app
```

## Acceso a la aplicación

Una vez iniciado, el servidor estará disponible en:

- **LAVNet Zacatecas**: http://localhost:8000/lavnet-zac/
- **LAVNet Argentina**: http://localhost:8000/lavnet-arg/
- **Admin**: http://localhost:8000/admin/

## Configuración para producción

Para desplegar en producción en `gipimo.ddns.net`:

1. Actualizar `ALLOWED_HOSTS` en `settings.py` (ya configurado)
2. Cambiar `DEBUG = False` en producción
3. Configurar un servidor web (nginx) como proxy reverso
4. Usar gunicorn en lugar de runserver:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lavnet_site.wsgi:application"]
```

## Estructura del proyecto

```
/lavnet-zac/          # Aplicación LAVNet Zacatecas
/lavnet-arg/          # Aplicación LAVNet Argentina
/admin/               # Panel de administración Django
```

## Comandos útiles

```bash
# Ejecutar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Recolectar archivos estáticos
docker-compose exec web python manage.py collectstatic

# Acceder al shell de Django
docker-compose exec web python manage.py shell

# Ver logs en tiempo real
docker-compose logs -f web
```

## Variables de entorno

El proyecto usa las siguientes variables de entorno (configurables en `docker-compose.yml`):

- `DJANGO_SETTINGS_MODULE`: Módulo de configuración de Django
- `DEBUG`: Modo debug (True/False)
- `ALLOWED_HOSTS`: Hosts permitidos para el servidor

## Notas

- Los archivos estáticos se recolectan automáticamente al construir la imagen
- La base de datos SQLite se mantiene en el contenedor (considerar usar PostgreSQL en producción)
- El puerto 8000 está expuesto para acceso externo
