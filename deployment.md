# 🚀 Guía Completa de Deployment en Render

Esta guía te llevará paso a paso para deployar Symphonaut en Render.com de forma gratuita.

## 📋 Pre-requisitos

- [ ] Cuenta en [GitHub](https://github.com)
- [ ] Cuenta en [Render](https://render.com)
- [ ] Cuenta de desarrollador en [Spotify](https://developer.spotify.com)
- [ ] Tu código en un repositorio de GitHub

## 🎯 Paso 1: Preparar tu Repositorio

### 1.1 Estructura de Archivos

Asegúrate de que tu repositorio tenga esta estructura:

```
symphonaut/
├── server.py              # Backend Flask (en la raíz o en carpeta Backend/)
├── requirements.txt       # Dependencias Python
├── index.html            # Frontend (en la raíz o en carpeta Frontend/)
├── src/
│   └── app.js
├── .env.example
├── .gitignore
└── README.md
```

### 1.2 Verificar requirements.txt

Asegúrate de tener este contenido en `requirements.txt`:

```txt
Flask==3.0.0
Flask-Cors==4.0.0
spotipy==2.23.0
requests==2.31.0
gunicorn==21.2.0
```

### 1.3 Subir a GitHub

```bash
# Inicializar repositorio
git init
git add .
git commit -m "Initial commit - Symphonaut app"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/TU-USUARIO/symphonaut.git
git branch -M main
git push -u origin main
```

## 🎵 Paso 2: Configurar Spotify Developer

### 2.1 Crear Aplicación en Spotify

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Haz clic en "Create an App"
3. Llena los datos:
   - **App Name**: Symphonaut
   - **App Description**: Sistema de recomendaciones musicales
   - **Redirect URIs**: (los añadiremos después)
4. Acepta los términos y crea la app

### 2.2 Guardar Credenciales

Guarda estos datos (los necesitarás después):
- ✅ Client ID
- ✅ Client Secret

**⚠️ IMPORTANTE: Nunca subas estas credenciales a GitHub**

## 🔧 Paso 3: Deployar el Backend en Render

### 3.1 Crear Web Service

1. Ve a [Render Dashboard](https://dashboard.render.com)
2. Click en **"New +"** → **"Web Service"**
3. Conecta tu cuenta de GitHub (si es la primera vez)
4. Selecciona tu repositorio `symphonaut`

### 3.2 Configurar el Servicio

Llena los siguientes campos:

| Campo | Valor |
|-------|-------|
| **Name** | `symphonaut-backend` (o el nombre que prefieras) |
| **Region** | `Oregon (US West)` (el más cercano a tu ubicación) |
| **Branch** | `main` |
| **Root Directory** | (déjalo vacío si server.py está en la raíz, o pon `Backend` si está en una carpeta) |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn server:app` |
| **Instance Type** | `Free` |

### 3.3 Variables de Entorno

En la sección **"Environment Variables"**, añade:

```
SPOTIFY_CLIENT_ID=tu_client_id_de_spotify
SPOTIFY_CLIENT_SECRET=tu_client_secret_de_spotify
SPOTIFY_REDIRECT_URI=https://symphonaut-backend.onrender.com/callback
FRONTEND_URL=https://symphonaut-frontend.onrender.com
```

**⚠️ IMPORTANTE**: 
- Reemplaza `symphonaut-backend` con el nombre exacto que elegiste
- Reemplaza `symphonaut-frontend` con el nombre que usarás para el frontend
- NO pongas comillas en los valores

### 3.4 Deployar

1. Click en **"Create Web Service"**
2. Espera 5-10 minutos mientras Render construye y deploya tu backend
3. Verás logs en tiempo real del proceso
4. Cuando veas "Deploy succeeded", copia la URL (ejemplo: `https://symphonaut-backend.onrender.com`)

### 3.5 Verificar Backend

Visita: `https://tu-backend.onrender.com/health`

Deberías ver:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-20T..."
}
```

## 🎨 Paso 4: Deployar el Frontend en Render

### 4.1 Crear Static Site

1. En Render Dashboard, click en **"New +"** → **"Static Site"**
2. Selecciona el mismo repositorio `symphonaut`

### 4.2 Configurar el Static Site

| Campo | Valor |
|-------|-------|
| **Name** | `symphonaut-frontend` |
| **Branch** | `main` |
| **Root Directory** | (vacío si index.html está en la raíz, o `Frontend` si está en carpeta) |
| **Build Command** | (déjalo vacío) |
| **Publish Directory** | `.` (punto) |

### 4.3 Actualizar app.js

**ANTES DE DEPLOYAR**, actualiza el archivo `src/app.js`:

Cambia esta línea:
```javascript
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:5000'
  : 'https://tu-app-backend.onrender.com';
```

Por (reemplazando con tu URL real del backend):
```javascript
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:5000'
  : 'https://symphonaut-backend.onrender.com';
```

Guarda, commitea y pushea:
```bash
git add src/app.js
git commit -m "Update backend URL for production"
git push
```

### 4.4 Deployar Frontend

1. Click en **"Create Static Site"**
2. Espera 2-5 minutos
3. Copia la URL del frontend (ejemplo: `https://symphonaut-frontend.onrender.com`)

## 🔐 Paso 5: Actualizar Spotify Developer Dashboard

### 5.1 Añadir Redirect URI

1. Ve a tu app en [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click en **"Edit Settings"**
3. En **"Redirect URIs"**, añade:
   ```
   https://symphonaut-backend.onrender.com/callback
   ```
4. Click en **"Add"** y luego **"Save"**

### 5.2 Actualizar Variables de Entorno en Render

Si los nombres de tus servicios son diferentes, actualiza:

1. Ve a tu backend en Render
2. Click en "Environment"
3. Actualiza:
   - `SPOTIFY_REDIRECT_URI` con tu URL real del backend + `/callback`
   - `FRONTEND_URL` con tu URL real del frontend
4. Click en "Save Changes"
5. Render redesplegará automáticamente

## ✅ Paso 6: Verificar el Deployment

### 6.1 Pruebas

1. **Visita tu frontend**: `https://symphonaut-frontend.onrender.com`
2. Haz click en **"Conectar con Spotify"**
3. Autoriza la aplicación
4. Deberías ser redirigido de vuelta y ver tu nombre
5. Selecciona géneros y obtén recomendaciones

### 6.2 Si algo no funciona

**Error: "No se pudo conectar con el servidor"**
- Verifica que el backend esté corriendo en Render
- Revisa los logs del backend en Render Dashboard
- Verifica que la URL del backend en `app.js` sea correcta

**Error: "Authorization header is missing"**
- Limpia el localStorage del navegador
- Cierra sesión y vuelve a iniciar

**Error: "Redirect URI mismatch"**
- Verifica que la Redirect URI en Spotify coincida exactamente con tu backend URL + `/callback`
- No debe tener espacios o caracteres extra

## 🔄 Paso 7: Actualizaciones Futuras

Cuando hagas cambios:

```bash
git add .
git commit -m "Descripción de tus cambios"
git push
```

Render detectará los cambios y redesplegará automáticamente.

## 💡 Tips y Mejores Prácticas

### Performance

1. **Free Tier Limitations**:
   - Los servicios gratuitos se duermen después de 15 minutos de inactividad
   - El primer request después puede tardar 30-60 segundos
   - Considera mantener el servicio activo con un cron job

2. **Keep-Alive Service** (Opcional):
   Puedes usar servicios como [Uptime Robot](https://uptimerobot.com) para hacer ping a tu backend cada 14 minutos

### Seguridad

1. **Nunca hardcodees credenciales**
2. **Usa variables de entorno siempre**
3. **No subas el archivo `.env` a GitHub**
4. **Regenera las credenciales si las expones accidentalmente**

### Debugging

Para ver logs en Render:
1. Ve a tu servicio
2. Click en "Logs"
3. Verás todos los logs en tiempo real

### Dominios Personalizados

Si quieres usar tu propio dominio:
1. En Render, ve a "Settings"
2. Scroll a "Custom Domains"
3. Añade tu dominio
4. Configura los DNS records según las instrucciones

## 🆘 Solución de Problemas Comunes

| Error | Solución |
|-------|----------|
| Build failed | Verifica que `requirements.txt` esté correcto |
| Module not found | Asegúrate de que todas las dependencias estén en `requirements.txt` |
| Port already in use | Render maneja el puerto automáticamente, usa `os.environ.get('PORT', 5000)` |
| CORS error | Verifica que `FRONTEND_URL` esté configurado correctamente |
| 401 Unauthorized | Verifica las credenciales de Spotify y las variables de entorno |

## 📊 Monitoreo

Render proporciona métricas básicas gratuitas:
- CPU Usage
- Memory Usage
- Response Time
- Request Count

Accede a ellas desde el dashboard de tu servicio.

## 🎉 ¡Felicidades!

Tu aplicación Symphonaut ahora está en producción y accesible desde cualquier lugar del mundo.

**URLs Finales:**
- Frontend: `https://tu-frontend.onrender.com`
- Backend API: `https://tu-backend.onrender.com`
- Health Check: `https://tu-backend.onrender.com/health`

---

## 📚 Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Flask Deployment](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

## 🐛 Reportar Problemas

Si encuentras problemas, abre un issue en el repositorio de GitHub con:
- Descripción del error
- Logs del servidor
- Pasos para reproducir
- Capturas de pantalla si es posible