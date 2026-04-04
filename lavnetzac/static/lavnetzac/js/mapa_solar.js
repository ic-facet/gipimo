// Configuración del mapa solar
const MAP_WIDTH = 1400;
const MAP_HEIGHT = 700;
// Canvas pequeño para calcular la sombra rápido (Truco de rendimiento)
const SHADOW_RES_X = 200; 
const SHADOW_RES_Y = 100;

// Coordenadas de estaciones VLF
const STATIONS = {
    transmitters: [
        { name: "NAA", lat: 50.00, lon: -48 },   // Este de USA (Ajustado a la costa derecha)
        { name: "NLK", lat: 51.00, lon: -110 },  // Oeste de USA (Cerca de tu línea de Cascadia)
        { name: "NPM", lat: 21.42, lon: -145 },  // Hawaii (Centro del Pacífico)
        { name: "NWC", lat: -26.00, lon: 130 },  // Australia (Lado izquierdo, sin cambios)
        { name: "NDK", lat: 52.00, lon: -85 },    // Centro de USA
        { name: "NAU", lat: 20.00, lon: -46}    // Centro de US
    ],
    receivers: [
        { id: "UAZ", name: "LAVNet-UAZ-Mx", lat: 25.00, lon: -84, location: "Zacatecas, MX" } // Alineado con tu punto de México
    ]
};

// Lista de Volcanes 
const VOLCANOES = [
    { name: "Popocatépetl", lat: 22.00, lon: -81 }, 
    { name: "Colima", lat: 22.00, lon: -86 },

    { name: "Fuego", lat: 16.00, lon: -70 },

    { name: "Cotopaxi", lat: -0.67, lon: -58 },
    { name: "Ubinas", lat: -18.00, lon: -49 },
    { name: "Villarrica", lat: -30.00, lon: -49 },
    { name: "Tierra del Fuego", lat: -46, lon: -52 },

    { name: "St. Helens", lat: 60.00, lon: -193 },
    { name: "Shishaldin", lat: 54.00, lon: -110 },
    { name: "Alaska Peak", lat: 65, lon: -149 },

    { name: "Fuji", lat: 37.00, lon: 144 },
    { name: "Sakurajima", lat: 41.00, lon: 150 },
    { name: "Mayon", lat: 13.25, lon: 139 },

    { name: "Merapi", lat: -7.54, lon: 124 },
    { name: "Krakatoa", lat: -8.00, lon: 128 },
    { name: "Ruapehu", lat: -42.00, lon: 184 }
];

// Líneas de Placas Tectónicas 
const TECTONIC_LINES = [
    // --- TRAMO IZQUIERDO (Asia/Oceanía) - Se mantiene como está ---
    [{lat: 67, lon: -140}, {lat: 56, lon: 200}, {lat: 56, lon: 170}, {lat: 50, lon: 156}, {lat: 45, lon: 158}, {lat: 35, lon: 140}],
    [{lat: 35, lon: 140}, {lat: 15, lon: 124}, {lat: 0, lon: 110}, {lat: -8, lon: 120}, {lat: -5, lon: 130}],
    [{lat: -5, lon: 130}, {lat: 1, lon: 155}, {lat: -20, lon: 175}, {lat: -37, lon: 178}],


    [
        {lat: 67, lon: -140},
        {lat: 60, lon: -120}, 
        {lat: 48, lon: -112}, 
        {lat: 34, lon: -105}, 
        {lat: 23, lon: -92},  
        {lat: 15, lon: -80}  
    ],
    [
        {lat: 15, lon: -80}, 
        {lat: 5, lon: -58},   
        {lat: -10, lon: -60}, 
        {lat: -20, lon: -55},
        {lat: -24, lon: -49},
        {lat: -30, lon: -50}, 
        {lat: -55, lon: -58}  
    ]
];
// Variables globales
let canvas, ctx;
let shadowCanvas, shadowCtx;
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
    

    canvas.width = MAP_WIDTH;
    canvas.height = MAP_HEIGHT;


    shadowCanvas = document.createElement('canvas');
    shadowCanvas.width = SHADOW_RES_X;
    shadowCanvas.height = SHADOW_RES_Y;
    shadowCtx = shadowCanvas.getContext('2d');
    

    ctx.fillStyle = '#1a1a2e';
    ctx.fillRect(0, 0, MAP_WIDTH, MAP_HEIGHT);
    
    // Cargar imagen del mapa
    worldMapImage = new Image();
    worldMapImage.crossOrigin = 'anonymous';

    worldMapImage.onload = () => {
        const offscreenCanvas = document.createElement('canvas');
        offscreenCanvas.width = MAP_WIDTH;
        offscreenCanvas.height = MAP_HEIGHT;
        const offCtx = offscreenCanvas.getContext('2d');

        offCtx.filter = 'brightness(0.85) contrast(1.1) sepia(0.2) hue-rotate(180deg) saturate(0.8)';
        offCtx.drawImage(worldMapImage, 0, 0, MAP_WIDTH, MAP_HEIGHT);

        worldMapImage = offscreenCanvas; 
        
        imageLoaded = true;
        updateMap();
    };


    worldMapImage.onerror = () => {
        imageLoaded = false;
        updateMap();
    };
    worldMapImage.src = '/static/lavnetzac/images/mapamundi_pacifico.png';
    
    // Event listeners
    document.getElementById('btnRewind').addEventListener('click', () => adjustTime(-60));
    document.getElementById('btnBackward').addEventListener('click', () => adjustTime(-15));
    document.getElementById('btnRealTime').addEventListener('click', resetToRealTime);
    document.getElementById('btnForward').addEventListener('click', () => adjustTime(15));
    document.getElementById('btnFastForward').addEventListener('click', () => adjustTime(60));
    document.getElementById('btnToggleAnimation').addEventListener('click', toggleAnimation);
    

    updateMap();

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
        animationInterval = setInterval(() => adjustTime(10), 50);
    } else {
        btn.classList.remove('active');
        btn.innerHTML = '<span>▶️</span> Animar';
        clearInterval(animationInterval);
    }
}


function updateMap() {
    if (isRealTime && !isAnimating) {
        currentTime = new Date();
    }
    
    const sunPos = calculateSunPosition(currentTime);
    updateInfo(sunPos);


    ctx.clearRect(0, 0, MAP_WIDTH, MAP_HEIGHT);


    if (imageLoaded && worldMapImage) {
        ctx.save();
        ctx.filter = 'brightness(0.9) hue-rotate(180deg) saturate(0.5) invert(0.05)';
        ctx.drawImage(worldMapImage, 0, 0, MAP_WIDTH, MAP_HEIGHT);
        ctx.restore();
    } 
    else {
        ctx.fillStyle = '#1e3a5f';
        ctx.fillRect(0, 0, MAP_WIDTH, MAP_HEIGHT);
        drawWorldMapVector(); // Fallback vectorial si falla la imagen
    }

  
    drawShadowLayer(sunPos);

   
    drawGrid();
    drawTectonicPlates();
    drawVolcanoes();
  
    drawStations(); 
    drawSunPosition(sunPos);
    drawTimeZoneLabel();
}


function calculateSunPosition(date) {
    const pi = Math.PI;
    const rad = pi / 180;
    
    const now = date;
    const start = new Date(Date.UTC(now.getUTCFullYear(), 0, 0));
    const diff = now - start;
    const oneDay = 1000 * 60 * 60 * 24;
    const dayOfYear = Math.floor(diff / oneDay);
    
    const declination = 23.45 * Math.sin(rad * (360 / 365) * (dayOfYear - 81));
    const B = rad * (360 / 365) * (dayOfYear - 81);
    const eot = 9.87 * Math.sin(2 * B) - 7.53 * Math.cos(B) - 1.5 * Math.sin(B);

    const utcHours = now.getUTCHours() + now.getUTCMinutes() / 60 + now.getUTCSeconds() / 3600;
    let longitude = -15 * (utcHours - 12 + eot / 60);
    longitude = ((longitude + 180) % 360 + 360) % 360 - 180;

    return { lat: declination, lon: longitude };
}

function drawShadowLayer(sunPos) {
    shadowCtx.clearRect(0, 0, SHADOW_RES_X, SHADOW_RES_Y);
    const imgData = shadowCtx.createImageData(SHADOW_RES_X, SHADOW_RES_Y);
    const data = imgData.data;
    
    const sunLatRad = sunPos.lat * (Math.PI / 180);
    const sunLonRad = sunPos.lon * (Math.PI / 180);

    for (let y = 0; y < SHADOW_RES_Y; y++) {
    
        const lat = 90 - (y / SHADOW_RES_Y) * 180;
        const latRad = lat * (Math.PI / 180);
        
        for (let x = 0; x < SHADOW_RES_X; x++) {
  
            let lon = (x / SHADOW_RES_X) * 360 - 11;
            const lonRad = lon * (Math.PI / 180);
            

            const sinAlt = Math.sin(latRad) * Math.sin(sunLatRad) + 
                           Math.cos(latRad) * Math.cos(sunLatRad) * Math.cos(lonRad - sunLonRad);
            
            const i = (y * SHADOW_RES_X + x) * 4;
            
     
            data[i] = 10;     
            data[i + 1] = 20; 
            data[i + 2] = 60; 
            
          
            let alpha = 0;
            if (sinAlt > 0.05) {
            
                alpha = 0; 
            } else if (sinAlt < -0.1) {
        
                alpha = 205; 
            } else {
               
                alpha = ((0.05 - sinAlt) / 0.15) * 210;
            }
            
            data[i + 3] = alpha;
        }
    }
    shadowCtx.putImageData(imgData, 0, 0);
    

    ctx.drawImage(shadowCanvas, 0, 0, MAP_WIDTH, MAP_HEIGHT);
}

function latLonToXY(lat, lon) {

    let shiftedLon = lon - 11; 
    
    if (shiftedLon < 0) shiftedLon += 360;
    if (shiftedLon > 360) shiftedLon -= 360;

    const x = (shiftedLon / 360) * MAP_WIDTH;
    const y = ((90 - lat) / 180) * MAP_HEIGHT;
    
    return { x, y };
}

function drawGrid() {
    ctx.strokeStyle = 'rgba(100, 115, 130, 0.3)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    
    for (let i = -180; i <= 180; i += 30) {
        const x = ((i + 180) / 360) * MAP_WIDTH;
        ctx.moveTo(x, 0); ctx.lineTo(x, MAP_HEIGHT);
    }
    for (let i = -90; i <= 90; i += 30) {
        const y = ((90 - i) / 180) * MAP_HEIGHT;
        ctx.moveTo(0, y); ctx.lineTo(MAP_WIDTH, y);
    }
    ctx.stroke();
    
    // Resaltar el Ecuador con un poco más de fuerza
    ctx.strokeStyle = 'rgba(100, 115, 130, 0.5)';
    ctx.beginPath();
    ctx.moveTo(0, MAP_HEIGHT/2); ctx.lineTo(MAP_WIDTH, MAP_HEIGHT/2);
    ctx.stroke();
}


function drawPropagationLines() {
    const zacReceiver = STATIONS.receivers.find(r => r.id === 'UAZ');
    
    if (zacReceiver) {
        const rx = latLonToXY(zacReceiver.lat, zacReceiver.lon);
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
}

// Función para dibujar placas
function drawTectonicPlates() {
    TECTONIC_LINES.forEach(path => {
        ctx.strokeStyle = 'rgba(255, 69, 0, 0.3)'; // Naranja rojizo transparente
        ctx.lineWidth = 15;
        ctx.lineJoin = 'round';
        ctx.beginPath();
        drawPath(path);
        ctx.stroke();

        ctx.strokeStyle = '#ff4500';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]); 
        ctx.beginPath();
        drawPath(path);
        ctx.stroke();
        ctx.setLineDash([]);
    });
}

// Función auxiliar
function drawPath(path) {
    let first = true;
    path.forEach(point => {
        const p = latLonToXY(point.lat, point.lon);
        if (first) { ctx.moveTo(p.x, p.y); first = false; }
        else { ctx.lineTo(p.x, p.y); }
    });
}

function drawStations() {
    // Dibujar Transmisores
    STATIONS.transmitters.forEach(tx => {
        const p = latLonToXY(tx.lat, tx.lon);
        
        // El punto rojo
        ctx.fillStyle = '#ff5252'; 
        ctx.beginPath(); 
        ctx.arc(p.x, p.y, 6, 0, Math.PI*2); 
        ctx.fill();

        // Configuración de la fuente
        ctx.font = 'bold 11px Arial'; 
        ctx.textAlign = 'center'; 

        ctx.strokeStyle = 'black'; 
        ctx.lineWidth = 3; 
        ctx.strokeText(tx.name, p.x, p.y - 12);


        ctx.fillStyle = 'white'; 
        ctx.fillText(tx.name, p.x, p.y - 12);
    });
    

    STATIONS.receivers.forEach(rx => {
        const r = latLonToXY(rx.lat, rx.lon);
        ctx.fillStyle = '#00e676'; ctx.beginPath(); ctx.arc(r.x, r.y, 8, 0, Math.PI*2); ctx.fill();
        ctx.lineWidth = 2; ctx.strokeStyle = 'white'; ctx.stroke();
        
        ctx.font = 'bold 12px Arial';

        ctx.strokeStyle = 'black';
        ctx.lineWidth = 3;
        ctx.strokeText(rx.name, r.x, r.y - 15);
        
        ctx.fillStyle = 'white'; 
        ctx.fillText(rx.name, r.x, r.y - 15);
    });
}

function drawSunPosition(sunPos) {
    const p = latLonToXY(sunPos.lat, sunPos.lon);
    
    const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, 30);
    g.addColorStop(0, 'rgba(255, 255, 0, 0.8)');
    g.addColorStop(1, 'rgba(255, 255, 0, 0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, 30, 0, Math.PI*2); ctx.fill();
    
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

    const zacReceiver = STATIONS.receivers.find(r => r.id === 'UAZ');
    const label = zacReceiver ? `UTC-6 (${zacReceiver.location})` : 'UTC-6 (Zacatecas, MX)';

    ctx.save();
    ctx.font = 'bold 14px Arial';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.textAlign = 'left';
    ctx.fillText(label, 15, 25);
    
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    const textWidth = ctx.measureText(label).width;
    ctx.fillRect(10, 10, textWidth + 10, 25);
    
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillText(label, 15, 25);
    ctx.restore();
}

function updateInfo(sunPos) {
    document.getElementById('timeUTC').textContent = currentTime.toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
    
    // Local 
    const localMs = currentTime.getTime() - (6 * 60 * 60 * 1000); 
    const localDate = new Date(localMs);
    document.getElementById('timeLocal').textContent = localDate.toISOString().slice(0, 19).replace('T', ' ');
    document.getElementById('sunPosition').textContent = `${sunPos.lat.toFixed(2)}°, ${sunPos.lon.toFixed(2)}°`;
    

    const zac = STATIONS.receivers.find(r => r.id === 'UAZ');
    if (zac) {
        const rLat = zac.lat * (Math.PI/180);
        const sLat = sunPos.lat * (Math.PI/180);
        const dLon = (sunPos.lon - zac.lon) * (Math.PI/180);
        const alt = Math.asin(Math.sin(rLat)*Math.sin(sLat) + Math.cos(rLat)*Math.cos(sLat)*Math.cos(dLon)) * (180/Math.PI);
    }
}

function drawWorldMapVector() {
    ctx.fillStyle = '#3a5a40';
    ctx.fillRect(200, 150, 300, 200);
    ctx.fillRect(350, 400, 150, 250);
    ctx.fillRect(700, 150, 100, 100);
    ctx.fillRect(700, 300, 200, 200);
    ctx.fillRect(1100, 450, 150, 100);
}