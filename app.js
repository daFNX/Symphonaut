// --- Componente SongCard (Actualizado con score) ---
Vue.component('song-card', {
  props: ['song'],
  data: () => ({
    isLiked: false,
  }),
  template: `
    <v-card class="song-card" dark elevation="4">
      <div class="d-flex flex-no-wrap justify-space-between">
        <v-avatar class="ma-3" size="100" tile>
          <v-img :src="song.cover || 'https://via.placeholder.com/100'"></v-img>
        </v-avatar>
        <div style="flex: 1;">
          <v-card-title class="text-h6" style="word-break: break-word;">
            {{ song.title }}
            <v-chip v-if="song.score" x-small color="green" class="ml-2">
              {{ song.score }}% match
            </v-chip>
          </v-card-title>
          <v-card-subtitle>{{ song.artist }}</v-card-subtitle>
          <v-card-actions>
              <v-btn icon @click.stop="likeClicked">
                  <v-icon :color="isLiked ? 'pink' : 'white'">mdi-heart</v-icon>
              </v-btn>
              <v-btn icon @click.stop="playClicked">
                  <v-icon>mdi-play-circle</v-icon>
              </v-btn>
          </v-card-actions>
        </div>
      </div>
    </v-card>
  `,
  methods: {
    likeClicked() {
      this.isLiked = !this.isLiked;
      this.$emit('like', this.song.id);
    },
    playClicked() {
      this.$emit('play', this.song.spotify_uri);
    }
  }
});


// --- Instancia Principal de Vue Actualizada ---
new Vue({
  el: '#app',
  vuetify: new Vuetify(),
  data: () => ({
    userProfile: {
      genres: [],
      mood: null,
      energy: 50
    },
    availableGenres: ['rock', 'pop', 'jazz', 'electronic', 'classical', 'hip-hop', 'reggae', 'metal', 'folk', 'r-n-b', 'funk', 'indie', 'country', 'blues', 'latin', 'soul', 'disco', 'house', 'techno', 'punk', 'edm', 'ambient', 'alternative', 'dance'],
    moods: ['Feliz', 'Triste', 'Eufórico', 'Relajado', 'Nostálgico', 'Romántico', 'Energético', 'Concentrado'],
    recommendations: [],
    loading: false,
    showEmptyState: true,
    
    isAuthenticated: false,
    user: { name: null },
    alert: {
      show: false,
      message: '',
      type: 'info'
    }
  }),

  // Se ejecuta cuando la app se carga por primera vez.
  created() {
    // 1. Revisar si venimos de la redirección de Spotify (el token está en la URL)
    const hash = window.location.hash.substring(1);
    
    // Limpiamos la URL para que el token no se quede visible
    if (hash) {
      window.location.hash = '';
    }

    // Priorizamos el token nuevo de la URL, si no, usamos el que ya estaba guardado.
    const token = hash || localStorage.getItem('spotify_access_token');

    if (token) {
      // Si tenemos un token, lo manejamos.
      this.handleToken(token);
    } else {
      // Si no hay token en ningún lado, mostramos mensaje para iniciar sesión.
      this.showAlert('Por favor, inicia sesión con Spotify para comenzar.', 'info');
    }
  },

  methods: {
    // --- Lógica de Autenticación ---
    login() {
      // Redirige al usuario a la ruta de login del backend.
      window.location.href = 'http://127.0.0.1:5000/login';
    },
    
    handleToken(token) {
        // Guarda el token en el almacenamiento local para no perderlo al recargar
        localStorage.setItem('spotify_access_token', token);
        // Configura Axios para que envíe este token en TODAS las peticiones futuras
        this.setupAxios(token);
        this.isAuthenticated = true; // Marcamos como autenticado
        this.showAlert('¡Conexión exitosa!', 'success');
        this.getUserProfile(); // Obtenemos el nombre del usuario
    },
    
    setupAxios(token) {
        // Esta es la pieza clave: le decimos a Axios que incluya
        // la cabecera 'Authorization' en todas sus peticiones.
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        // CRÍTICO: Configuramos Axios para enviar JSON correctamente
        axios.defaults.headers.post['Content-Type'] = 'application/json';
        // Aumentar el timeout para peticiones de recomendaciones
        axios.defaults.timeout = 60000; // 60 segundos
    },

    // --- Lógica de API ---
    async getRecommendations() {
      if (this.userProfile.genres.length === 0) {
        this.showAlert('Por favor, selecciona al menos un género.', 'warning');
        return;
      }
      
      this.loading = true;
      this.showEmptyState = false;
      this.alert.show = false;
      
      try {
        // CRÍTICO: Aseguramos que genres sea un array
        const payload = {
          genres: Array.isArray(this.userProfile.genres) 
            ? this.userProfile.genres 
            : [this.userProfile.genres],
          mood: this.userProfile.mood,
          energy: this.userProfile.energy
        };
        
        console.log('Enviando payload:', JSON.stringify(payload));
        
        const response = await axios.post(
          'http://127.0.0.1:5000/recomendar', 
          payload,
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        
        this.recommendations = response.data;
        if(response.data.length === 0){
             this.showAlert('No se encontraron recomendaciones con esos criterios. ¡Intenta otra combinación!', 'info');
        }

      } catch (error) {
        console.error('Error al obtener recomendaciones:', error);
        console.error('Response data:', error.response?.data);
        this.handleApiError(error); // Centralizamos el manejo de errores
      } finally {
        this.loading = false;
        if (this.recommendations.length === 0) {
            this.showEmptyState = true;
        }
      }
    },
    
    async getUserProfile() {
        try {
            const response = await axios.get('http://127.0.0.1:5000/me');
            this.user.name = response.data.name;
        } catch(error) {
            console.error('Error al obtener perfil de usuario:', error);
            this.handleApiError(error);
        }
    },

    async likeSong(trackId) {
      try {
        await axios.post('http://127.0.0.1:5000/like', { track_id: trackId });
        this.showAlert('¡Canción añadida a tus Me Gusta!', 'success');
      } catch (error) {
        console.error('Error al dar like:', error);
        this.handleApiError(error);
      }
    },

    async playSong(trackUri) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/play', { track_uri: trackUri });
        this.showAlert(response.data.message, 'success');
      } catch (error) {
        console.error('Error al reproducir:', error);
        this.handleApiError(error);
      }
    },

    // --- Métodos de UI y Errores ---
    showAlert(message, type = 'info') {
      this.alert.message = message;
      this.alert.type = type;
      this.alert.show = true;
      setTimeout(() => { this.alert.show = false; }, 5000);
    },

    handleApiError(error) {
      let message = 'Ocurrió un error inesperado. Revisa la consola para más detalles.';
      if (error.response) {
          // Si el token es inválido (401), desautenticamos al usuario
          if (error.response.status === 401) {
            this.isAuthenticated = false;
            localStorage.removeItem('spotify_access_token'); // Limpiamos el token viejo
            axios.defaults.headers.common['Authorization'] = null;
            message = 'Tu sesión ha expirado. Por favor, inicia sesión de nuevo.';
          } else {
            // Usamos el mensaje específico que nos envía el backend
            message = error.response.data.message || error.response.data.error || `Error ${error.response.status}`;
          }
      } else if (error.code === 'ECONNABORTED') {
          message = 'La petición tardó demasiado en responder. Revisa tu conexión a internet.'
      } else if (!error.response) {
          message = 'No se pudo conectar con el servidor. ¿Está encendido?';
      }
      this.showAlert(message, 'error');
      console.error('Error de API:', error);
    }
  }
});