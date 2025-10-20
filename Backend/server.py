# --- PASO 1: INSTALAR LAS LIBRERÍAS NECESARIAS ---
# pip install Flask Flask-Cors spotipy requests

from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import os
import logging
import random
import requests
from dotenv import load_dotenv

app = Flask(__name__)
# --- CONFIGURACIÓN DE LA APP ---
CORS(app, origins=["http://localhost:5500", "http://127.0.0.1:5500"], supports_credentials=True)

# --- CONFIGURACIÓN DE SPOTIPY (API DE SPOTIFY) ---
# Load secrets from environment/.env. Add your .env to .gitignore to avoid committing credentials.
try:
    load_dotenv()
except Exception:
    # python-dotenv is optional; fall back to environment variables
    pass

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
    missing = [name for name, val in (("SPOTIPY_CLIENT_ID", SPOTIPY_CLIENT_ID),
                                      ("SPOTIPY_CLIENT_SECRET", SPOTIPY_CLIENT_SECRET),
                                      ("SPOTIPY_REDIRECT_URI", SPOTIPY_REDIRECT_URI)) if not val]
    raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

SCOPE = "user-read-private user-read-email user-library-read user-library-modify streaming user-modify-playback-state user-top-read user-follow-read"

# Configuración de logging más detallada
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
    requests_timeout=30
)

# --- RUTAS DE AUTENTICACIÓN (SIN CAMBIOS) ---
@app.route('/login')
def login():
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    try:
        token_info = auth_manager.get_access_token(code=request.args.get("code"))
        access_token = token_info['access_token']
        return redirect(f"http://127.0.0.1:5500/#{access_token}")
    except Exception as e:
        error_description = request.args.get("error", "un error desconocido.")
        return redirect(f"http://1.27.0.0.1:5500/#error={error_description}")

# --- FUNCIÓN DE AYUDA CON LOGGING ADICIONAL ---
def get_spotify_client_from_request():
    # LOG: Revisar si existen variables de entorno de proxy
    http_proxy = os.environ.get('HTTP_PROXY')
    https_proxy = os.environ.get('HTTPS_PROXY')
    logging.info(f"Variable de entorno HTTP_PROXY: {http_proxy}")
    logging.info(f"Variable de entorno HTTPS_PROXY: {https_proxy}")

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logging.error("Header 'Authorization' no encontrado en la petición.")
        raise Exception("Authorization header is missing")
    
    # LOG: Confirmar que el token se está recibiendo
    logging.info(f"Header 'Authorization' recibido, comienza con: {auth_header[:15]}...")
    
    try:
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0] != "Bearer":
            raise Exception("Invalid Authorization header format. Expected 'Bearer <token>'")
        access_token = parts[1]
        
        session = requests.Session()
        session.proxies = {}
        
        return spotipy.Spotify(
            auth=access_token, 
            requests_timeout=30, 
            retries=3, 
            requests_session=session
        )
    
    except Exception as e:
        logging.error(f"Error al procesar el header de autorización: {e}")
        raise Exception(str(e))

# --- RUTA DE RECOMENDACIONES (VERSIÓN DE PRUEBA FINAL) ---
@app.route('/recomendar', methods=['POST'])
def recomendar():
    logging.info("==========================================================")
    logging.info("==== INICIANDO PETICIÓN /recomendar (PRUEBA GLOBAL) ====")
    logging.info("==========================================================")
    
    try:
        sp = get_spotify_client_from_request()
    except Exception as e:
        return jsonify({"error": str(e)}), 401

    user_profile = request.json
    if not user_profile or 'genres' not in user_profile or not user_profile['genres']:
        return jsonify({"error": "Selecciona al menos un género musical"}), 400

    query_parts = []
    genres = user_profile.get('genres', [])
    
    # --- CAMBIO 1: USAMOS SOLO EL PRIMER GÉNERO PARA SIMPLIFICAR LA PRUEBA ---
    if genres:
        first_genre = genres[0].lower().strip()
        query_parts.append(f'genre:"{first_genre}"')
        logging.info(f"Simplificando la búsqueda para probar solo con el género: {first_genre}")
    else:
        return jsonify([])

    # --- TEMPORALMENTE DESACTIVADO PARA LA PRUEBA ---
    # try:
    #     top_artists = sp.current_user_top_artists(limit=3, time_range='short_term')
    #     if top_artists['items']:
    #         for artist in top_artists['items']:
    #             query_parts.append(f'artist:"{artist["name"]}"')
    # except Exception as e:
    #     logging.warning(f"No se pudieron obtener artistas top (continuando solo con géneros): {e}")

    search_query = " ".join(query_parts)
    logging.info(f"Query de búsqueda de prueba construida: {search_query}")

    try:
        logging.info("Ejecutando búsqueda simple y global...")
        
        # --- CAMBIO 2: AÑADIMOS market=None PARA BUSCAR EN EL CATÁLOGO GLOBAL ---
        results = sp.search(q=search_query, type='track', limit=50, market=None)
        
        tracks = results.get('tracks', {}).get('items', [])
        logging.info(f"Búsqueda global encontró {len(tracks)} canciones.")

    except Exception as e:
        logging.error(f"FALLÓ la llamada de búsqueda. Error: {e}")
        return jsonify([])

    recommendations = []
    for track in tracks:
        if not track or not track.get('album') or not track['album']['images']:
            continue
        
        recommendations.append({
            "id": track['id'], "title": track['name'], "artist": ", ".join([artist['name'] for artist in track['artists']]),
            "cover": track['album']['images'][0]['url'], "spotify_uri": track['uri']
        })
    
    random.shuffle(recommendations)
    logging.info(f"Proceso finalizado. Devolviendo {len(recommendations)} recomendaciones.")
    logging.info("==========================================================")
    return jsonify(recommendations)

# --- OTRAS RUTAS (SIN CAMBIOS) ---
@app.route('/me')
def get_current_user():
    try:
        sp = get_spotify_client_from_request()
        user_data = sp.current_user()
        return jsonify({"name": user_data.get('display_name', 'Usuario')})
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/like', methods=['POST'])
def like_song():
    track_id = request.json.get('track_id')
    if not track_id:
        return jsonify({"status": "error", "message": "track_id es requerido"}), 400
    try:
        sp = get_spotify_client_from_request()
        sp.current_user_saved_tracks_add(tracks=[track_id])
        return jsonify({"status": "success", "message": "Canción guardada en 'Me gusta'"})
    except spotipy.exceptions.SpotifyException as e:
        return jsonify({"status": "error", "message": str(e.msg)}), e.http_status
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 401


@app.route('/play', methods=['POST'])
def play_song():
    track_uri = request.json.get('track_uri')
    if not track_uri:
        return jsonify({"error": "track_uri es requerido"}), 400
    try:
        sp = get_spotify_client_from_request()
        sp.start_playback(uris=[track_uri])
        return jsonify({"status": "success", "message": "Reproduciendo canción"})
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 404:
            return jsonify({"status": "error", "message": "No se encontró un dispositivo activo. Abre Spotify en tu teléfono, web o computadora."}), 404
        if e.http_status == 403:
            return jsonify({"status": "error", "message": "La reproducción requiere una cuenta de Spotify Premium."}), 403
        return jsonify({"status": "error", "message": str(e.msg)}), e.http_status
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)