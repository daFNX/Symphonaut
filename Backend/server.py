import os
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import logging
import random
import requests
from functools import wraps
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURACIÓN SEGURA ---
# Usa variables de entorno para credenciales sensibles
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5000/callback")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://127.0.0.1:5500")

# Validación de variables de entorno críticas
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Las variables de entorno SPOTIFY_CLIENT_ID y SPOTIFY_CLIENT_SECRET son requeridas")

# CORS configurado para producción
CORS(app, 
     origins=[FRONTEND_URL, "http://localhost:5500", "http://127.0.0.1:5500"],
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"])

SCOPE = "user-read-private user-read-email user-library-read user-library-modify streaming user-modify-playback-state user-top-read user-follow-read"

# Logging mejorado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
    requests_timeout=30
)

# --- DECORADOR PARA AUTENTICACIÓN ---
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            sp = get_spotify_client_from_request()
            return f(sp, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error de autenticación: {e}")
            return jsonify({"error": "No autorizado", "message": str(e)}), 401
    return decorated_function

# --- FUNCIÓN DE AYUDA MEJORADA ---
def get_spotify_client_from_request():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise Exception("Authorization header is missing")
    
    parts = auth_header.split(" ")
    if len(parts) != 2 or parts[0] != "Bearer":
        raise Exception("Invalid Authorization header format")
    
    access_token = parts[1]
    session = requests.Session()
    session.proxies = {}
    
    return spotipy.Spotify(
        auth=access_token,
        requests_timeout=30,
        retries=3,
        requests_session=session
    )

# --- RUTAS DE AUTENTICACIÓN ---
@app.route('/login')
def login():
    auth_url = auth_manager.get_authorize_url()
    logger.info("Usuario redirigido a login de Spotify")
    return redirect(auth_url)

@app.route('/callback')
def callback():
    try:
        code = request.args.get("code")
        if not code:
            error = request.args.get("error", "unknown_error")
            logger.error(f"Error en callback: {error}")
            return redirect(f"{FRONTEND_URL}#error={error}")
        
        token_info = auth_manager.get_access_token(code)
        access_token = token_info['access_token']
        logger.info("Token obtenido exitosamente")
        return redirect(f"{FRONTEND_URL}#{access_token}")
    except Exception as e:
        logger.error(f"Error en callback: {e}")
        return redirect(f"{FRONTEND_URL}#error=authentication_failed")

# --- RUTA DE PERFIL DE USUARIO ---
@app.route('/me')
@require_auth
def get_current_user(sp):
    try:
        user_data = sp.current_user()
        return jsonify({
            "name": user_data.get('display_name', 'Usuario'),
            "email": user_data.get('email'),
            "id": user_data.get('id')
        })
    except Exception as e:
        logger.error(f"Error obteniendo perfil: {e}")
        return jsonify({"error": str(e)}), 500

# --- RUTA DE RECOMENDACIONES MEJORADA ---
@app.route('/recomendar', methods=['POST'])
@require_auth
def recomendar(sp):
    logger.info("=== Iniciando solicitud de recomendaciones ===")
    
    try:
        user_profile = request.get_json()
        
        # Validación de entrada
        if not user_profile:
            return jsonify({"error": "No se proporcionó perfil de usuario"}), 400
        
        genres = user_profile.get('genres', [])
        if not genres:
            return jsonify({"error": "Selecciona al menos un género musical"}), 400
        
        mood = user_profile.get('mood')
        energy = user_profile.get('energy', 50)
        
        logger.info(f"Perfil recibido - Géneros: {genres}, Mood: {mood}, Energy: {energy}")
        
        # Construir query de búsqueda
        query_parts = []
        
        # Usar los primeros 3 géneros para no sobrecargar la query
        for genre in genres[:3]:
            query_parts.append(f'genre:"{genre.lower().strip()}"')
        
        # Intentar obtener artistas top del usuario
        try:
            top_artists = sp.current_user_top_artists(limit=2, time_range='short_term')
            if top_artists.get('items'):
                for artist in top_artists['items'][:2]:
                    query_parts.append(f'artist:"{artist["name"]}"')
                logger.info(f"Artistas top incluidos: {[a['name'] for a in top_artists['items'][:2]]}")
        except Exception as e:
            logger.warning(f"No se pudieron obtener artistas top: {e}")
        
        search_query = " OR ".join(query_parts)
        logger.info(f"Query de búsqueda: {search_query}")
        
        # Realizar búsqueda
        results = sp.search(q=search_query, type='track', limit=50, market=None)
        tracks = results.get('tracks', {}).get('items', [])
        logger.info(f"Búsqueda encontró {len(tracks)} canciones")
        
        # Procesar recomendaciones
        recommendations = []
        for track in tracks:
            if not track or not track.get('album') or not track['album'].get('images'):
                continue
            
            # Calcular score de coincidencia basado en popularidad y características
            popularity = track.get('popularity', 0)
            score = min(100, popularity + random.randint(-10, 10))
            
            recommendations.append({
                "id": track['id'],
                "title": track['name'],
                "artist": ", ".join([artist['name'] for artist in track['artists']]),
                "artists": [artist['name'] for artist in track['artists']],
                "album": track['album']['name'],
                "cover": track['album']['images'][0]['url'] if track['album']['images'] else None,
                "albumArt": track['album']['images'][0]['url'] if track['album']['images'] else None,
                "spotify_uri": track['uri'],
                "popularity": popularity,
                "score": score,
                "matchPercent": score,
                "genres": genres[:3],
                "energy": energy,
                "liked": False
            })
        
        # Ordenar por score y randomizar un poco
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        top_recommendations = recommendations[:20]
        random.shuffle(top_recommendations)
        
        logger.info(f"Devolviendo {len(top_recommendations)} recomendaciones")
        return jsonify(top_recommendations)
        
    except Exception as e:
        logger.error(f"Error en /recomendar: {e}", exc_info=True)
        return jsonify({"error": "Error al obtener recomendaciones", "message": str(e)}), 500

# --- RUTA PARA DAR LIKE ---
@app.route('/like', methods=['POST'])
@require_auth
def like_song(sp):
    try:
        data = request.get_json()
        track_id = data.get('track_id')
        
        if not track_id:
            return jsonify({"status": "error", "message": "track_id es requerido"}), 400
        
        sp.current_user_saved_tracks_add(tracks=[track_id])
        logger.info(f"Canción {track_id} añadida a Me gusta")
        return jsonify({"status": "success", "message": "Canción guardada en 'Me gusta'"})
        
    except SpotifyException as e:
        logger.error(f"Error de Spotify al dar like: {e}")
        return jsonify({"status": "error", "message": str(e.msg)}), e.http_status
    except Exception as e:
        logger.error(f"Error al dar like: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- RUTA PARA REPRODUCIR ---
@app.route('/play', methods=['POST'])
@require_auth
def play_song(sp):
    try:
        data = request.get_json()
        track_uri = data.get('track_uri')
        
        if not track_uri:
            return jsonify({"error": "track_uri es requerido"}), 400
        
        sp.start_playback(uris=[track_uri])
        logger.info(f"Reproduciendo canción: {track_uri}")
        return jsonify({"status": "success", "message": "Reproduciendo canción"})
        
    except SpotifyException as e:
        if e.http_status == 404:
            return jsonify({
                "status": "error",
                "message": "No se encontró un dispositivo activo. Abre Spotify en tu dispositivo."
            }), 404
        if e.http_status == 403:
            return jsonify({
                "status": "error",
                "message": "La reproducción requiere Spotify Premium."
            }), 403
        logger.error(f"Error de Spotify al reproducir: {e}")
        return jsonify({"status": "error", "message": str(e.msg)}), e.http_status
    except Exception as e:
        logger.error(f"Error al reproducir: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- RUTA DE HEALTH CHECK (útil para Render) ---
@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })

# --- MANEJO DE ERRORES GLOBAL ---
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Error interno del servidor: {error}")
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)