// Configuración del mapa solar
const MAP_WIDTH = 1400;
const MAP_HEIGHT = 700;
// Canvas pequeño para calcular la sombra rápido (Truco de rendimiento)
const SHADOW_RES_X = 200; 
const SHADOW_RES_Y = 100;

// Coordenadas de estaciones VLF
const STATIONS = {
    transmitters: [
        { name: 'NAA', lat: 44.65, lon: -67.28, freq: '24.0 kHz', location: 'Cutler, Maine' },
        { name: 'NDK', lat: 46.37, lon: -98.34, freq: '25.2 kHz', location: 'LaMoure, ND' },
        { name: 'NLK', lat: 48.20, lon: -121.92, freq: '24.8 kHz', location: 'Jim Creek, WA' },
        { name: 'NAU', lat: 18.40, lon: -67.18, freq: '40.75 kHz', location: 'Aguada, PR' },
        { name: 'NPM', lat: 21.42, lon: -158.15, freq: '21.4 kHz', location: 'Lualualei, HI' },
        { name: 'NWC', lat: -21.82, lon: 114.17, freq: '19.8 kHz', location: 'North West Cape, AU' }
    ],
    receiver: { name: 'Chile', lat: 22.77, lon: -102.58, location: 'Chile, MX' }
};

// Lista Extendida de Volcanes del Cinturón de Fuego +
const VOLCANOES = [
    // --- Sudamérica (Andes) ---
    { name: 'Villarrica', lat: -39.42, lon: -71.93 },
    { name: 'Ojos del Salado', lat: -27.11, lon: -68.54 },
    { name: 'Lascar', lat: -23.37, lon: -67.73 },
    { name: 'Sabancaya', lat: -15.78, lon: -71.85 },
    { name: 'Ubinas', lat: -16.35, lon: -70.90 },
    { name: 'Cotopaxi', lat: -0.68, lon: -78.43 },
    { name: 'Tungurahua', lat: -1.46, lon: -78.44 },
    { name: 'Sangay', lat: -2.00, lon: -78.34 },
    { name: 'Nevado del Ruiz', lat: 4.89, lon: -75.32 },
    { name: 'Galeras', lat: 1.22, lon: -77.37 },
    
    // --- Centroamérica y México ---
    { name: 'Arenal', lat: 10.46, lon: -84.70 },
    { name: 'Turrialba', lat: 10.02, lon: -83.76 },
    { name: 'Momotombo', lat: 12.42, lon: -86.54 },
    { name: 'Fuego', lat: 14.47, lon: -90.88 },
    { name: 'Pacaya', lat: 14.38, lon: -90.60 },
    { name: 'Santa María', lat: 14.75, lon: -91.55 },
    { name: 'San Miguel', lat: 13.43, lon: -88.27 },
    { name: 'Popocatépetl', lat: 19.02, lon: -98.62 },
    { name: 'Colima', lat: 19.51, lon: -103.62 },
    { name: 'Pico de Orizaba', lat: 19.03, lon: -97.27 },
    { name: 'Paricutín', lat: 19.49, lon: -102.25 },
    { name: 'El Chichón', lat: 17.36, lon: -93.22 },

    // --- USA / Canadá / Alaska (Cascadas y Aleutianas) ---
    { name: 'Santa Helena', lat: 46.20, lon: -122.19 },
    { name: 'Rainier', lat: 46.85, lon: -121.76 },
    { name: 'Shasta', lat: 41.40, lon: -122.19 },
    { name: 'Hood', lat: 45.37, lon: -121.69 },
    { name: 'Pavlof', lat: 55.41, lon: -161.88 },
    { name: 'Shishaldin', lat: 54.75, lon: -163.97 },
    { name: 'Redoubt', lat: 60.48, lon: -152.74 },
    { name: 'Augustine', lat: 59.36, lon: -153.43 },
    { name: 'Cleveland', lat: 52.82, lon: -169.94 },
    { name: 'Akutan', lat: 54.13, lon: -165.98 },

    // --- Rusia (Kamchatka / Kuriles) ---
    { name: 'Klyuchevskoy', lat: 56.05, lon: 160.64 },
    { name: 'Shiveluch', lat: 56.65, lon: 161.36 },
    { name: 'Bezymianny', lat: 55.97, lon: 160.59 },
    { name: 'Karymsky', lat: 54.05, lon: 159.44 },
    { name: 'Ebeko', lat: 50.69, lon: 156.01 },

    // --- Japón ---
    { name: 'Monte Fuji', lat: 35.36, lon: 138.72 },
    { name: 'Sakurajima', lat: 31.59, lon: 130.65 },
    { name: 'Monte Aso', lat: 32.88, lon: 131.10 },
    { name: 'Unzen', lat: 32.76, lon: 130.29 },
    { name: 'Asama', lat: 36.40, lon: 138.52 },

    // --- Sudeste Asiático (Indonesia / Filipinas) ---
    { name: 'Pinatubo', lat: 15.13, lon: 120.35 },
    { name: 'Mayon', lat: 13.25, lon: 123.68 },
    { name: 'Taal', lat: 14.00, lon: 120.99 },
    { name: 'Kanlaon', lat: 10.41, lon: 123.13 },
    { name: 'Krakatoa', lat: -6.10, lon: 105.42 },
    { name: 'Merapi', lat: -7.54, lon: 110.44 },
    { name: 'Semeru', lat: -8.10, lon: 112.92 },
    { name: 'Bromo', lat: -7.94, lon: 112.95 },
    { name: 'Agung', lat: -8.34, lon: 115.50 },
    { name: 'Tambora', lat: -8.25, lon: 118.00 },
    { name: 'Dukono', lat: 1.69, lon: 127.88 },
    { name: 'Ibu', lat: 1.48, lon: 127.63 },
    
    // --- Pacífico Sur (Vanuatu / Tonga / NZ) ---
    { name: 'Manam', lat: -4.10, lon: 145.06 },
    { name: 'Rabaul', lat: -4.27, lon: 152.20 },
    { name: 'Yasur', lat: -19.53, lon: 169.44 },
    { name: 'Hunga Tonga', lat: -20.57, lon: -175.38 },
    { name: 'Ruapehu', lat: -39.28, lon: 175.57 },
    { name: 'White Island', lat: -37.52, lon: 177.18 },

    // --- Otros Importantes (Hawaii / Islandia / Etna) ---
    { name: 'Mauna Loa', lat: 19.47, lon: -155.60 },
    { name: 'Kilauea', lat: 19.42, lon: -155.29 },
    { name: 'Etna', lat: 37.75, lon: 14.99 },
    { name: 'Stromboli', lat: 38.78, lon: 15.21 },
    { name: 'Vesubio', lat: 40.82, lon: 14.42 },
    { name: 'Hekla', lat: 63.99, lon: -19.70 },
    { name: 'Fagradalsfjall', lat: 63.90, lon: -22.27 },
    { name: 'Erebus', lat: -77.53, lon: 167.17 },
    { name: 'Kilimanjaro', lat: -3.06, lon: 37.35 }
];

// Variables globales
let canvas, ctx;
let shadowCanvas, shadowCtx; // Canvas invisible para la sombra
let currentTime = new Date();
let isRealTime = true;
let animationInterval = null;
let isAnimating = false;
let worldMapImage = null;
let imageLoaded = false;

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    console.log('Inicializando mapa solar optimizado...');
    
    canvas = document.getElementById('solarMap');
    if (!canvas) return;
    ctx = canvas.getContext('2d');
    
    // Configurar tamaño del canvas principal
    canvas.width = MAP_WIDTH;
    canvas.height = MAP_HEIGHT;

    // Crear canvas fantasma para la sombra (Optimización clave)
    shadowCanvas = document.createElement('canvas');
    shadowCanvas.width = SHADOW_RES_X;
    shadowCanvas.height = SHADOW_RES_Y;
    shadowCtx = shadowCanvas.getContext('2d');
    
    // Fondo inicial
    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, MAP_WIDTH, MAP_HEIGHT);
    
    // Cargar imagen del mapa
    worldMapImage = new Image();
    worldMapImage.crossOrigin = 'anonymous';
    worldMapImage.onload = () => {
        imageLoaded = true;
        updateMap();
    };
    worldMapImage.onerror = () => {
        imageLoaded = false;
        updateMap();
    };
    worldMapImage.src = 'https://upload.wikimedia.org/wikipedia/commons/8/83/Equirectangular_projection_SW.jpg';
    
    // Event listeners
    document.getElementById('btnRewind').addEventListener('click', () => adjustTime(-60));
    document.getElementById('btnBackward').addEventListener('click', () => adjustTime(-15));
    document.getElementById('btnRealTime').addEventListener('click', resetToRealTime);
    document.getElementById('btnForward').addEventListener('click', () => adjustTime(15));
    document.getElementById('btnFastForward').addEventListener('click', () => adjustTime(60));
    document.getElementById('btnToggleAnimation').addEventListener('click', toggleAnimation);
    
    // Iniciar ciclo de actualización
    updateMap();
    // Actualizar reloj cada segundo si es tiempo real
    setInterval(() => {
        if(isRealTime && !isAnimating) updateMap();
    }, 1000);
});

function adjustTime(minutes) {
    isRealTime = false;
    currentTime = new Date(currentTime.getTime() + minutes * 60000);
    updateMap();
}

function resetToRealTime() {
    isRealTime = true;
    isAnimating = false;
    clearInterval(animationInterval);
    const btn = document.getElementById('btnToggleAnimation');
    btn.classList.remove('active');
    btn.innerHTML = '<span>▶️</span> Animar';
    currentTime = new Date();
    updateMap();
}

function toggleAnimation() {
    const btn = document.getElementById('btnToggleAnimation');
    isAnimating = !isAnimating;
    
    if (isAnimating) {
        isRealTime = false;
        btn.classList.add('active');
        btn.innerHTML = '<span>⏸️</span> Pausar';
        // Animación fluida: 10 minutos cada 50ms
        animationInterval = setInterval(() => adjustTime(10), 50);
    } else {
        btn.classList.remove('active');
        btn.innerHTML = '<span>▶️</span> Animar';
        clearInterval(animationInterval);
    }
}

// Función principal de dibujado
function updateMap() {
    if (isRealTime && !isAnimating) {
        currentTime = new Date();
    }
    
    const sunPos = calculateSunPosition(currentTime);
    updateInfo(sunPos);

    // 1. Limpiar
    ctx.clearRect(0, 0, MAP_WIDTH, MAP_HEIGHT);

    // 2. Dibujar Mapa Base
    if (imageLoaded && worldMapImage) {
        ctx.drawImage(worldMapImage, 0, 0, MAP_WIDTH, MAP_HEIGHT);
    } else {
        ctx.fillStyle = '#1e3a5f';
        ctx.fillRect(0, 0, MAP_WIDTH, MAP_HEIGHT);
        drawWorldMapVector(); // Fallback vectorial si falla la imagen
    }

    // 3. Dibujar Sombra (Optimizado)
    drawShadowLayer(sunPos);

    // 4. Dibujar Elementos
    drawGrid();
    drawVolcanoes();
    drawPropagationLines();
    drawStations();
    drawSunPosition(sunPos);
    drawTimeZoneLabel();
}

// Cálculo astronómico robusto
function calculateSunPosition(date) {
    // Algoritmo simplificado pero preciso para mapas web
    const pi = Math.PI;
    const rad = pi / 180;
    
    // Obtener fecha UTC
    const now = date;
    const start = new Date(Date.UTC(now.getUTCFullYear(), 0, 0));
    const diff = now - start;
    const oneDay = 1000 * 60 * 60 * 24;
    const dayOfYear = Math.floor(diff / oneDay);
    
    // Calcular declinación (latitud del sol)
    // Fórmula aproximada: 23.45 * sin(360/365 * (d - 81))
    const declination = 23.45 * Math.sin(rad * (360 / 365) * (dayOfYear - 81));
    
    // Calcular Ecuación del Tiempo (EoT) para ajustar la longitud exacta
    const B = rad * (360 / 365) * (dayOfYear - 81);
    const eot = 9.87 * Math.sin(2 * B) - 7.53 * Math.cos(B) - 1.5 * Math.sin(B);

    // Calcular longitud del sol (GHA - Greenwich Hour Angle)
    const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60 + now.getUTCSeconds() / 3600;
    
    // El sol viaja 15 grados por hora. A las 12:00 UTC está en 0 grados (mas EoT).
    // 12 UTC = 0 deg. 13 UTC = -15 deg (Oeste).
    let longitude = -15 * (utcHours - 12 + eot / 60);
    
    // Normalizar a -180 / 180
    longitude = ((longitude + 180) % 360 + 360) % 360 - 180;

    return { lat: declination, lon: longitude };
}

// La Magia: Dibujar sombra en baja resolución y escalar
function drawShadowLayer(sunPos) {
    // Limpiar canvas pequeño
    shadowCtx.clearRect(0, 0, SHADOW_RES_X, SHADOW_RES_Y);
    
    // Obtener data de píxeles
    const imgData = shadowCtx.createImageData(SHADOW_RES_X, SHADOW_RES_Y);
    const data = imgData.data;
    
    const sunLatRad = sunPos.lat * (Math.PI / 180);
    const sunLonRad = sunPos.lon * (Math.PI / 180);

    // Recorrer solo el canvas pequeño (mucho más rápido)
    for (let y = 0; y < SHADOW_RES_Y; y++) {
        const lat = 90 - (y / SHADOW_RES_Y) * 180;
        const latRad = lat * (Math.PI / 180);
        
        for (let x = 0; x < SHADOW_RES_X; x++) {
            const lon = (x / SHADOW_RES_X) * 360 - 180;
            const lonRad = lon * (Math.PI / 180);

            // Cálculo de altitud solar (Ángulo cenital)
            // Math.sin(lat)*Math.sin(sunLat) + Math.cos(lat)*Math.cos(sunLat)*Math.cos(lon-sunLon)
            const sinAlt = Math.sin(latRad) * Math.sin(sunLatRad) + 
                           Math.cos(latRad) * Math.cos(sunLatRad) * Math.cos(lonRad - sunLonRad);
            
            const i = (y * SHADOW_RES_X + x) * 4;
            
            // Color de la sombra (Azul oscuro: 10, 20, 60)
            data[i] = 10;     // R
            data[i + 1] = 20; // G
            data[i + 2] = 60; // B

            // Alpha basado en la altitud del sol
            // Si sinAlt > 0 es día (Alpha 0). Si es < -0.1 es noche cerrada (Alpha 0.85)
            let alpha = 0;
            
            if (sinAlt > 0.05) { 
                alpha = 0; // Día pleno
            } else if (sinAlt > -0.1) { 
                // Crepúsculo (gradiente suave)
                // Mapear de 0.05 a -0.1 hacia 0 a 0.85
                const t = (0.05 - sinAlt) / 0.15;
                alpha = t * 0.85 * 255;
            } else {
                alpha = 0.85 * 255; // Noche cerrada
            }
            
            data[i + 3] = alpha;
        }
    }
    
    // Poner píxeles en canvas pequeño
    shadowCtx.putImageData(imgData, 0, 0);
    
    // Dibujar canvas pequeño estirado sobre el grande (suaviza los píxeles automáticamente)
    ctx.drawImage(shadowCanvas, 0, 0, MAP_WIDTH, MAP_HEIGHT);
}

// --- Funciones auxiliares visuales (Grid, Estaciones, etc) ---

function latLonToXY(lat, lon) {
    const x = ((lon + 180) / 360) * MAP_WIDTH;
    const y = ((90 - lat) / 180) * MAP_HEIGHT;
    return { x, y };
}

function drawGrid() {
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    // Meridianos y Paralelos
    for (let i = -180; i <= 180; i += 30) {
        const x = ((i + 180) / 360) * MAP_WIDTH;
        ctx.moveTo(x, 0); ctx.lineTo(x, MAP_HEIGHT);
    }
    for (let i = -90; i <= 90; i += 30) {
        const y = ((90 - i) / 180) * MAP_HEIGHT;
        ctx.moveTo(0, y); ctx.lineTo(MAP_WIDTH, y);
    }
    ctx.stroke();
    
    // Ecuador
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.beginPath();
    ctx.moveTo(0, MAP_HEIGHT/2); ctx.lineTo(MAP_WIDTH, MAP_HEIGHT/2);
    ctx.stroke();
}

function drawPropagationLines() {
    const rx = latLonToXY(STATIONS.receiver.lat, STATIONS.receiver.lon);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.setLineDash([4, 4]);
    ctx.beginPath();
    STATIONS.transmitters.forEach(tx => {
        const t = latLonToXY(tx.lat, tx.lon);
        ctx.moveTo(t.x, t.y); ctx.lineTo(rx.x, rx.y);
    });
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawStations() {
    // Transmisores
    STATIONS.transmitters.forEach(tx => {
        const p = latLonToXY(tx.lat, tx.lon);
        ctx.fillStyle = '#ff5252'; ctx.beginPath(); ctx.arc(p.x, p.y, 6, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = 'white'; ctx.font = '11px Arial'; ctx.textAlign = 'center'; 
        ctx.fillText(tx.name, p.x, p.y - 10);
    });
    // Receptor (Chile)
    const r = latLonToXY(STATIONS.receiver.lat, STATIONS.receiver.lon);
    ctx.fillStyle = '#00e676'; ctx.beginPath(); ctx.arc(r.x, r.y, 8, 0, Math.PI*2); ctx.fill();
    ctx.lineWidth = 2; ctx.strokeStyle = 'white'; ctx.stroke();
    ctx.fillStyle = 'white'; ctx.font = 'bold 12px Arial'; 
    ctx.fillText(STATIONS.receiver.name, r.x, r.y - 12);
}

function drawSunPosition(sunPos) {
    const p = latLonToXY(sunPos.lat, sunPos.lon);
    
    // Brillo
    const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 30);
    g.addColorStop(0, 'rgba(255, 255, 0, 0.8)');
    g.addColorStop(1, 'rgba(255, 255, 0, 0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, 30, 0, Math.PI*2); ctx.fill();
    
    // Cuerpo del sol
    ctx.fillStyle = '#ffeb3b'; ctx.beginPath(); ctx.arc(p.x, p.y, 8, 0, Math.PI*2); ctx.fill();
}

function drawVolcanoes() {
    ctx.fillStyle = '#ff3300';
    ctx.shadowColor = 'black';
    ctx.shadowBlur = 2;

    VOLCANOES.forEach(vol => {
        const p = latLonToXY(vol.lat, vol.lon);
        const size = 4;

        ctx.beginPath();
        ctx.moveTo(p.x, p.y - size);
        ctx.lineTo(p.x + size, p.y + size);
        ctx.lineTo(p.x - size, p.y + size);
        ctx.closePath();
        ctx.fill();
    });

    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
}

function drawTimeZoneLabel() {
    // Etiqueta en esquina superior izquierda
    ctx.save();
    ctx.font = 'bold 14px Arial';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.textAlign = 'left';
    ctx.fillText('UTC-6 (Chile)', 15, 25);
    
    // Fondo sutilmente oscuro detrás del texto para legibilidad
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.fillRect(10, 10, 165, 25);
    
    // Redibujar texto encima
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillText('UTC-6 (Chile)', 15, 25);
    ctx.restore();
}

function updateInfo(sunPos) {
    document.getElementById('timeUTC').textContent = currentTime.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
    // Local (Forzamos a UTC-6 para Chile visualmente, aunque el navegador sea otro)
    const localMs = currentTime.getTime() - (6 * 60 * 60 * 1000); 
    const localDate = new Date(localMs);
    document.getElementById('timeLocal').textContent = localDate.toISOString().slice(0, 19).replace('T', ' ');
    document.getElementById('sunPosition').textContent = `${sunPos.lat.toFixed(2)}°, ${sunPos.lon.toFixed(2)}°`;
    // Altitud en Chile
    const rLat = STATIONS.receiver.lat * (Math.PI/180);
    const sLat = sunPos.lat * (Math.PI/180);
    const dLon = (sunPos.lon - STATIONS.receiver.lon) * (Math.PI/180);
    const alt = Math.asin(Math.sin(rLat)*Math.sin(sLat) + Math.cos(rLat)*Math.cos(sLat)*Math.cos(dLon)) * (180/Math.PI);
    document.getElementById('sunAltitude').textContent = `${alt.toFixed(1)}°`;
}

// Fallback si no carga la imagen
function drawWorldMapVector() {
    // Dibujo simplificado solo si falla la imagen de Wikipedia
    ctx.fillStyle = '#3a5a40'; // Continentes verdes
    ctx.fillRect(200, 150, 300, 200); // Norteamerica (fake)
    ctx.fillRect(350, 400, 150, 250); // Sudamerica (fake)
    ctx.fillRect(700, 150, 100, 100); // Europa (fake)
    ctx.fillRect(700, 300, 200, 200); // Africa (fake)
    ctx.fillRect(1100, 450, 150, 100); // Australia (fake)
}