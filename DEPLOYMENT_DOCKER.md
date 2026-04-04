# Guía de Despliegue con Docker - LAVNet en gipimo.ddns.net

## Información del Servidor

- **Host**: gipimo.ddns.net
- **Puerto SSH**: 2025
- **Puerto HTTP**: 8000
- **Directorio**: /var/www/gipimo
- **URLs**:
  - Zacatecas: http://gipimo.ddns.net:8000/lavnet-zac/
  - Argentina: http://gipimo.ddns.net:8000/lavnet-arg/

## Pre-requisitos en el Servidor

```bash
# Conectar al servidor
ssh -p 2025 usuario@gipimo.ddns.net

# Instalar Docker y Docker Compose
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker

# Agregar tu usuario al grupo docker (opcional, para no usar sudo)
sudo usermod -aG docker $USER
# Cerrar sesión y volver a entrar para que aplique
```

## Paso 1: Transferir Archivos al Servidor

### Opción A: Usando SCP desde Windows

```powershell
# Desde tu máquina Windows PowerShell
cd "E:\9no semestre\saz"

# Copiar todos los archivos
scp -P 2025 -r * usuario@gipimo.ddns.net:/var/www/gipimo/
```

### Opción B: Usando Git (Recomendado)

```bash
# En el servidor
cd /var/www
sudo mkdir -p gipimo
sudo chown $USER:$USER gipimo
cd gipimo

# Clonar repositorio (si tienes uno)
git clone tu-repo-url .

# O inicializar para recibir archivos
git init
```

## Paso 2: Configurar Variables de Entorno

```bash
# Conectar al servidor
ssh -p 2025 usuario@gipimo.ddns.net

# Ir al directorio
cd /var/www/gipimo

# Crear archivo .env para producción
nano .env
```

Contenido del archivo `.env`:

```bash
# Generar SECRET_KEY (ejecutar en tu máquina local o servidor con Python):
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

SECRET_KEY=tu-secret-key-super-segura-generada
DEBUG=False
ALLOWED_HOSTS=gipimo.ddns.net,localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=lavnet_site.settings
```

## Paso 3: Construir y Ejecutar con Docker

```bash
# En el servidor, dentro de /var/www/gipimo

# Construir la imagen de producción
docker-compose -f docker-compose.prod.yml build

# Iniciar los contenedores en segundo plano
docker-compose -f docker-compose.prod.yml up -d

# Ver logs para verificar que todo está bien
docker-compose -f docker-compose.prod.yml logs -f
```

## Paso 4: Ejecutar Migraciones (Primera vez)

```bash
# Ejecutar migraciones dentro del contenedor
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Crear superusuario (opcional)
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

## Paso 5: Verificar Despliegue

```bash
# Ver estado de contenedores
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs web

# Probar desde el servidor
curl http://localhost:8000/lavnet-zac/
curl http://localhost:8000/lavnet-arg/
```

Desde tu navegador:
- http://gipimo.ddns.net:8000/lavnet-zac/
- http://gipimo.ddns.net:8000/lavnet-arg/

## Comandos Útiles

### Ver logs en tiempo real
```bash
docker-compose -f docker-compose.prod.yml logs -f web
```

### Reiniciar contenedores
```bash
docker-compose -f docker-compose.prod.yml restart
```

### Detener contenedores
```bash
docker-compose -f docker-compose.prod.yml down
```

### Detener y eliminar volúmenes
```bash
docker-compose -f docker-compose.prod.yml down -v
```

### Ver contenedores corriendo
```bash
docker ps
```

### Acceder a la shell del contenedor
```bash
docker-compose -f docker-compose.prod.yml exec web bash
```

### Actualizar el proyecto
```bash
cd /var/www/gipimo

# Si usas git
git pull origin main

# Reconstruir imagen
docker-compose -f docker-compose.prod.yml build

# Reiniciar contenedores
docker-compose -f docker-compose.prod.yml up -d

# Ejecutar migraciones si hay nuevas
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
```

## Configurar Docker para Inicio Automático

### Opción 1: Docker Compose con Restart Policy (Ya incluido)

El archivo `docker-compose.prod.yml` ya tiene `restart: unless-stopped`, por lo que los contenedores se reiniciarán automáticamente.

### Opción 2: Servicio Systemd (Opcional)

Si quieres más control, crea un servicio systemd:

```bash
sudo nano /etc/systemd/system/lavnet-docker.service
```

Contenido:
```ini
[Unit]
Description=LAVNet Docker Compose Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/var/www/gipimo
ExecStart=/usr/bin/docker-compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker-compose -f docker-compose.prod.yml down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Activar el servicio:
```bash
sudo systemctl daemon-reload
sudo systemctl enable lavnet-docker
sudo systemctl start lavnet-docker
```

## Solución de Problemas

### Los contenedores no inician
```bash
# Ver logs detallados
docker-compose -f docker-compose.prod.yml logs

# Ver logs de un servicio específico
docker-compose -f docker-compose.prod.yml logs web

# Verificar que Docker está corriendo
sudo systemctl status docker
```

### Puerto 8000 ya está en uso
```bash
# Ver qué está usando el puerto
sudo lsof -i :8000

# Detener contenedores
docker-compose -f docker-compose.prod.yml down

# O cambiar el puerto en docker-compose.prod.yml
# ports:
#   - "8001:8000"  # Puerto externo:Puerto interno
```

### Healthcheck falla
```bash
# Verificar que la aplicación responde
docker-compose -f docker-compose.prod.yml exec web curl http://localhost:8000/lavnet-zac/

# Ver logs del healthcheck
docker inspect --format "{{json .State.Health }}" <container_id> | jq
```

### Archivos estáticos no se cargan
```bash
# Los archivos estáticos ya están incluidos en la imagen Docker
# Si hay problemas, reconstruir la imagen
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

### Limpiar imágenes antiguas
```bash
# Eliminar contenedores detenidos
docker container prune

# Eliminar imágenes sin usar
docker image prune

# Limpiar todo (cuidado!)
docker system prune -a
```

## Monitoreo

### Ver uso de recursos
```bash
# Uso de CPU y memoria de contenedores
docker stats

# Información del contenedor
docker-compose -f docker-compose.prod.yml ps
```

### Logs
```bash
# Logs de todos los servicios
docker-compose -f docker-compose.prod.yml logs -f

# Últimas 100 líneas
docker-compose -f docker-compose.prod.yml logs --tail=100

# Logs desde hace 1 hora
docker-compose -f docker-compose.prod.yml logs --since 1h
```

## Backup

### Base de datos
```bash
# Copiar base de datos desde el contenedor
docker-compose -f docker-compose.prod.yml exec web cp /app/db.sqlite3 /app/staticfiles/backup.db
docker cp $(docker-compose -f docker-compose.prod.yml ps -q web):/app/db.sqlite3 ./backup-$(date +%Y%m%d).db
```

### Volúmenes
```bash
# Hacer backup del volumen de estáticos
docker run --rm -v gipimo_static_volume:/data -v $(pwd):/backup ubuntu tar czf /backup/static-backup-$(date +%Y%m%d).tar.gz /data
```

## Seguridad

1. **Firewall**:
```bash
sudo ufw allow 2025/tcp  # SSH
sudo ufw allow 8000/tcp  # HTTP
sudo ufw enable
```

2. **Actualizar imágenes regularmente**:
```bash
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

3. **Variables de entorno**: Nunca subir `.env` al repositorio

4. **Permisos**: El contenedor corre con usuario no-root (ya configurado en Dockerfile.prod)

## Resumen de Comandos Rápidos

```bash
# Desplegar/Actualizar
cd /var/www/gipimo
git pull  # si usas git
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f

# Reiniciar
docker-compose -f docker-compose.prod.yml restart

# Detener
docker-compose -f docker-compose.prod.yml down

# Estado
docker-compose -f docker-compose.prod.yml ps
```

## Ventajas de Usar Docker

✅ Entorno consistente entre desarrollo y producción
✅ Fácil actualización y rollback
✅ Aislamiento del sistema host
✅ No necesitas instalar Python ni dependencias en el servidor
✅ Escalable (puedes agregar más contenedores fácilmente)
