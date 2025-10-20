# 🎵 Symphonaut

**Sistema de Recomendaciones Musicales Inteligentes** que utiliza la API de Spotify para proporcionar sugerencias personalizadas basadas en tus géneros favoritos, estado de ánimo y nivel de energía.

![Symphonaut Banner](https://img.shields.io/badge/Spotify-API-1DB954?style=for-the-badge&logo=spotify&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-2.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)

## ✨ Características

- 🎯 **Recomendaciones Personalizadas**: Basadas en géneros, mood y energía
- 🎨 **Interfaz Moderna**: Diseño glass-morphism con animaciones suaves
- 🔐 **Autenticación Segura**: OAuth 2.0 con Spotify
- ▶️ **Control de Reproducción**: Reproduce canciones directamente desde la app
- ❤️ **Gestión de Me Gusta**: Guarda tus canciones favoritas
- 📊 **Estadísticas en Tiempo Real**: Visualiza tus métricas musicales

## 🚀 Demo en Vivo
[WORK IN PROGRESS]

- **Frontend**: [link aun no disponible](https://symphonaut.onrender.com)
- **Backend API**: [link aun no disponible](https://symphonaut-api.onrender.com)

## 📋 Requisitos Previos

- Python 3.11 o superior
- Cuenta de Spotify (Premium recomendado para reproducción)
- Cuenta en [Render.com](https://render.com) (para deployment)
- Cuenta de desarrollador de Spotify

## 🔧 Configuración Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/symphonaut.git
cd symphonaut
```

### 2. Configurar Credenciales de Spotify

1. Ve a [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Crea una nueva aplicación
3. Obtén tu `Client ID` y `Client Secret`
4. Añade estas Redirect URIs:
   - `http://127.0.0.1:5000/callback` (para desarrollo local)
   - `https://tu-backend.onrender.com/callback` (para producción)

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:

```env
SPOTIFY_CLIENT_ID=tu_client_id_aqui
SPOTIFY_CLIENT_SECRET=tu_client_secret_aqui
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
FRONTEND_URL=http://127.0.0.1:5500
```

### 4. Instalar Dependencias

```bash
# Backend
pip install -r requirements.txt
```

### 5. Ejecutar la Aplicación

**Backend:**
```bash
python Backend/server.py
```

El servidor estará disponible en `http://127.0.0.1:5000`

**Frontend:**
```bash
# Usando Python
cd Frontend
python -m http.server 5500

# O usando Live Server en VS Code
# Haz clic derecho en index.html > "Open with Live Server"
```

El frontend estará disponible en `http://127.0.0.1:5500`

## 🌐 Deployment en Render

### Opción 1: Deployment Automático con render.yaml

1. **Sube tu código a GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/tu-usuario/symphonaut.git
git push -u origin main
```

2. **Crea una cuenta en Render**
   - Ve a [render.com](https://render.com) y crea una cuenta
   - Conecta tu cuenta de GitHub

3. **Crea el servicio Backend**
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Configuración:
     - **Name**: `symphonaut-backend`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn server:app`
     - **Root Directory**: `Backend` (si tienes los archivos en una carpeta)

4. **Configura las Variables de Entorno en Render**
   
   En el dashboard del servicio, ve a "Environment" y añade:
   
   ```
   SPOTIFY_CLIENT_ID=tu_client_id
   SPOTIFY_CLIENT_SECRET=tu_client_secret
   SPOTIFY_REDIRECT_URI=https://symphonaut-backend.onrender.com/callback
   FRONTEND_URL=https://symphonaut-frontend.onrender.com
   ```

5. **Crea el servicio Frontend**
   - Click en "New +" → "Static Site"
   - Conecta el mismo repositorio
   - Configuración:
     - **Name**: `symphonaut-frontend`
     - **Build Command**: (déjalo vacío)
     - **Publish Directory**: `.` (o la carpeta donde está tu index.html)

6. **Actualiza la URL del Backend en el Frontend**
   
   Edita `app.js` y cambia:
   ```javascript
   const API_URL = 'https://symphonaut-backend.onrender.com';
   ```

7. **Actualiza las Redirect URIs en Spotify**
   - Ve a tu app en Spotify Developer Dashboard
   - Añade: `https://symphonaut-backend.onrender.com/callback`

### Opción 2: Deployment Manual

**Backend:**

```bash
# 1. Crea un nuevo Web Service en Render
# 2. Conecta tu repositorio
# 3. Configura:
#    - Build Command: pip install -r requirements.txt
#    - Start Command: gunicorn server:app
#    - Añade las variables de entorno
```

**Frontend:**

```bash
# 1. Crea un nuevo Static Site en Render
# 2. Conecta tu repositorio
# 3. Publica la carpeta con index.html
```

## 🔒 Seguridad

- ✅ Variables de entorno para credenciales sensibles
- ✅ CORS configurado apropiadamente
- ✅ Validación de entrada en todas las rutas
- ✅ Manejo de errores robusto
- ✅ Logging para auditoría
- ✅ Sin credenciales hardcodeadas en el código

## 🎨 Tecnologías Utilizadas

### Backend
- **Flask**: Framework web ligero
- **Spotipy**: Cliente Python para Spotify API
- **Flask-CORS**: Manejo de CORS
- **Gunicorn**: Servidor WSGI para producción

### Frontend
- **Vue.js 2**: Framework JavaScript progresivo
- **Vuetify 2**: Framework de componentes Material Design
- **Axios**: Cliente HTTP
- **CSS3**: Animaciones y glass-morphism

## 📁 Estructura del Proyecto

```
symphonaut/
├── Backend/
│   ├── server.py           # API Flask
│   └── requirements.txt    # Dependencias Python
├── Frontend/
│   ├── index.html         # Página principal
│   ├── src/
│   │   └── app.js        # Lógica Vue.js
│   └── assets/           # Imágenes y recursos
├── .env.example          # Ejemplo de variables de entorno
├── .gitignore           # Archivos a ignorar
├── render.yaml          # Configuración de Render
└── README.md            # Este archivo
```

## 🐛 Solución de Problemas

### Error: "No se encontró dispositivo activo"
- Abre Spotify en tu computadora, teléfono o navegador
- Asegúrate de tener Spotify Premium

### Error: "Authorization header is missing"
- Cierra sesión y vuelve a iniciar sesión
- Verifica que las variables de entorno estén configuradas

### Error: "CORS policy"
- Verifica que `FRONTEND_URL` esté correctamente configurada
- Asegúrate de que ambos servicios estén corriendo

### El backend no se conecta en Render
- Verifica que todas las variables de entorno estén configuradas
- Revisa los logs en el dashboard de Render
- Asegúrate de usar `gunicorn` como start command

## 📝 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `SPOTIFY_CLIENT_ID` | ID de tu app de Spotify | `abc123...` |
| `SPOTIFY_CLIENT_SECRET` | Secret de tu app | `xyz789...` |
| `SPOTIFY_REDIRECT_URI` | URI de callback | `https://tu-app.onrender.com/callback` |
| `FRONTEND_URL` | URL de tu frontend | `https://tu-frontend.onrender.com` |
| `PORT` | Puerto del servidor | `5000` (Render lo configura automáticamente) |

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Tu Nombre - [da_fnx](https://www.instagram.com/da_fnx)

## 🙏 Agradecimientos

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy](https://spotipy.readthedocs.io/)
- [Vue.js](https://vuejs.org/)
- [Vuetify](https://vuetifyjs.com/)
- [Render](https://render.com/)

---

⭐️ Si te gusta este proyecto, ¡dale una estrella en GitHub!