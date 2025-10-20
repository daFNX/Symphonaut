# Symphonaut — Recomendaciones Inteligentes / Smart Music Recommender

deploy: (Work in progress)

ESPAÑOL
-------

Descripción
-----------
Symphonaut es una aplicación web ligera que ofrece recomendaciones musicales inteligentes y personalizadas basadas en el perfil del usuario (géneros, estado de ánimo y energía). La interfaz usa Vue + Vuetify y se integra con un backend minimalista (Python/Flask en `Backend/server.py`) para autenticación con Spotify, petición de recomendaciones y control de reproducción.

Estructura del proyecto
-----------------------
- `index.html` — Página principal y contenedor de la app Vue.
- `src/app.js` — Lógica de la aplicación Vue (autenticación, formularios, llamadas al backend, manejo de recomendaciones).
- `src/styles.css` — Estilos personalizados (si existen).
- `Backend/server.py` — Backend (servidor) que gestiona la autenticación con Spotify y expone endpoints como `/login`, `/me`, `/recomendar`, `/like` y `/play`.

Requisitos
----------
- Navegador moderno con soporte para ES Modules.
- Python 3.8+ para el backend (si se utiliza el servidor adjunto).
- Dependencias de Python para el backend (Flask, requests, dotenV o similares). Añadir `requirements.txt` más adelante.

Instalación y ejecución (desarrollo)
-----------------------------------
1. Clona el repositorio y abre el proyecto en tu editor.
2. Levanta el backend (ejemplo con virtualenv):

   ```powershell
   cd Backend
   python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
   python server.py
   ```

   Si aún no tienes `requirements.txt`, instala al menos Flask: `pip install flask requests`.

3. Abre `index.html` en tu navegador (o sirve la carpeta con un servidor estático).
4. Haz clic en "Iniciar Sesión con Spotify" para autenticarse y probar las recomendaciones.

Uso
---
- Completa tu perfil musical (selecciona géneros, estado de ánimo y nivel de energía) y pulsa "Obtener Recomendaciones".
- Desde la lista de recomendaciones puedes reproducir canciones, marcarlas como "Me gusta" y ver métricas básicas (energía, popularidad, match %).

Notas de integración
--------------------
- `src/app.js` espera que el backend esté corriendo en `http://127.0.0.1:5000` con endpoints REST específicos. Ajusta las URLs si ejecutas el backend en otra dirección o puerto.
- La app guarda el token de Spotify en `localStorage` y lo añade en la cabecera `Authorization: Bearer <token>` para las llamadas al backend.

Seguridad y privacidad
----------------------
- Evita subir el `client_secret` de Spotify a repositorios públicos. El flujo de OAuth debe manejarse en el backend.

Contribuciones y próximos pasos
-------------------------------
- Añadir `requirements.txt` y scripts en `package.json` para facilitar el arranque.
- Mejorar el manejo de errores en el backend y añadir tests básicos.
- Añadir un Dockerfile y despliegue (actualmente en progreso).

ENGLISH
-------

Description
-----------
Symphonaut is a lightweight web app that provides intelligent, personalized music recommendations based on a user's profile (genres, mood and energy). The UI is built with Vue + Vuetify and integrates with a minimal Python/Flask backend (`Backend/server.py`) for Spotify authentication, recommendation requests and playback control.

Project structure
-----------------
- `index.html` — Main page and Vue app container.
- `src/app.js` — Vue application logic (auth, forms, backend calls, recommendations handling).
- `src/styles.css` — Custom styles (if present).
- `Backend/server.py` — Backend server that handles Spotify auth and exposes endpoints like `/login`, `/me`, `/recomendar`, `/like` and `/play`.

Requirements
------------
- Modern browser with ES Modules support.
- Python 3.8+ for the backend (if you use the included server).
- Python dependencies for the backend (Flask, requests, dotenv or similar). Add a `requirements.txt` later.

Installation & Running (development)
------------------------------------
1. Clone the repo and open the project in your editor.
2. Start the backend (example with virtualenv):

   ```powershell
   cd Backend
   python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
   python server.py
   ```

   If `requirements.txt` is missing, install at least Flask: `pip install flask requests`.

3. Open `index.html` in your browser (or serve the folder with a static server).
4. Click "Login with Spotify" to authenticate and test recommendations.

Usage
-----
- Fill your musical profile (select genres, mood and energy) and click "Get Recommendations".
- From the recommendations list you can play tracks, like them and view basic metrics (energy, popularity, match %).

Integration notes
-----------------
- `src/app.js` assumes the backend runs at `http://127.0.0.1:5000` and exposes certain REST endpoints. Adjust the URLs if you run the backend somewhere else.
- The app stores the Spotify token in `localStorage` and includes it in the `Authorization: Bearer <token>` header for backend calls.

Security & Privacy
------------------
- Do not commit your Spotify `client_secret` to public repositories. OAuth flow should be handled on the backend.

Contributing & Next steps
-------------------------
- Add `requirements.txt` and `package.json` scripts to simplify startup.
- Improve backend error handling and add basic tests.
- Add a Dockerfile and deployment instructions (work in progress).

License
-------
Aún no se ha especificado una licencia. Añade una si deseas permitir contribuciones públicas.
