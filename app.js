// Configuración de API URL (cambia según el entorno)
const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:5000'
  : 'https://tu-app-backend.onrender.com'; // Cambiar por tu URL de Render

// --- Componente SongCard Mejorado ---
Vue.component('song-card', {
  props: ['song'],
  data: () => ({
    isLiked: false,
    isPlaying: false,
  }),
  template: `
    <v-hover v-slot="{ hover }">
      <v-card 
        :elevation="hover ? 16 : 4" 
        class="song-card rounded-lg overflow-hidden"
        :class="{ 'playing': isPlaying }"
        style="transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);"
      >
        <div class="d-flex" style="min-height: 140px;">
          <!-- Album Art con efecto hover -->
          <div style="position: relative; width: 140px; flex-shrink: 0;">
            <v-img
              :src="song.cover || song.albumArt"
              width="140"
              height="140"
              class="grey darken-4"
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular indeterminate color="grey lighten-1"></v-progress-circular>
                </v-row>
              </template>
            </v-img>
            
            <!-- Play overlay con gradiente -->
            <div
              class="d-flex align-center justify-center"
              style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(0,0,0,0.1), rgba(0,0,0,0.7)); transition: opacity .25s ease;"
              :style="{ opacity: hover || isPlaying ? 1 : 0 }"
            >
              <v-btn 
                fab
                large 
                color="green accent-4" 
                @click.stop="playClicked"
                elevation="8"
              >
                <v-icon x-large>{{ isPlaying ? 'mdi-pause' : 'mdi-play' }}</v-icon>
              </v-btn>
            </div>
            
            <!-- Badge de score -->
            <v-chip
              v-if="song.score"
              x-small
              color="green accent-4"
              text-color="white"
              style="position: absolute; top: 8px; right: 8px; font-weight: 600;"
            >
              {{ Math.round(song.score) }}%
            </v-chip>
          </div>

          <!-- Información de la canción -->
          <v-card-text class="pa-4 d-flex flex-column" style="flex: 1; min-width: 0;">
            <div style="flex: 1;">
              <div class="text-h6 font-weight-bold mb-1" style="
                overflow: hidden;
                text-overflow: ellipsis;
                display: -webkit-box;
                -webkit-line-clamp: 2;
                -webkit-box-orient: vertical;
                line-height: 1.3;
              ">
                {{ song.title }}
              </div>
              
              <div class="text-subtitle-2 grey--text text--lighten-1 mb-3" style="
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
              ">
                {{ song.artist }}
              </div>

              <!-- Géneros -->
              <div class="mb-3" v-if="song.genres && song.genres.length">
                <v-chip
                  v-for="(genre, index) in song.genres.slice(0, 2)"
                  :key="index"
                  x-small
                  outlined
                  class="mr-1"
                >
                  {{ genre }}
                </v-chip>
              </div>

              <!-- Stats compactos -->
              <div class="d-flex align-center justify-space-between">
                <div style="flex: 1; max-width: 120px;">
                  <div class="caption grey--text mb-1">Popularidad</div>
                  <v-progress-linear
                    :value="song.popularity || 0"
                    height="6"
                    color="green accent-4"
                    rounded
                  ></v-progress-linear>
                </div>
                
                <div class="d-flex align-center ml-3">
                  <v-icon small color="amber darken-2" class="mr-1">mdi-flash</v-icon>
                  <span class="caption font-weight-bold">{{ song.energy || 50 }}</span>
                </div>
              </div>
            </div>

            <!-- Acciones -->
            <v-card-actions class="pa-0 mt-3">
              <v-btn 
                icon 
                small
                @click.stop="likeClicked"
                :title="isLiked ? 'Quitar de Me gusta' : 'Añadir a Me gusta'"
              >
                <v-icon :color="isLiked ? 'pink accent-3' : 'grey'">
                  {{ isLiked ? 'mdi-heart' : 'mdi-heart-outline' }}
                </v-icon>
              </v-btn>
              
              <v-btn 
                icon 
                small
                @click.stop="$emit('share', song)"
                title="Compartir"
              >
                <v-icon color="grey">mdi-share-variant</v-icon>
              </v-btn>
              
              <v-spacer></v-spacer>
              
              <v-btn
                text
                x-small
                color="grey"
                @click.stop="$emit('more', song)"
              >
                <v-icon small>mdi-dots-horizontal</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </div>
      </v-card>
    </v-hover>
  `,
  methods: {
    likeClicked() {
      this.isLiked = !this.isLiked;
      this.$emit('like', this.song.id);
    },
    playClicked() {
      this.isPlaying = !this.isPlaying;
      this.$emit('play', this.song.spotify_uri);
      // Simular que la canción deja de reproducirse después de un tiempo
      setTimeout(() => { this.isPlaying = false; }, 3000);
    }
  }
});

// --- Instancia Principal de Vue ---
new Vue({
  el: '#app',
  vuetify: new Vuetify({
    theme: {
      dark: false,
      themes: {
        light: {
          primary: '#3F51B5',
          secondary: '#00BCD4',
          accent: '#4CAF50',
          error: '#F44336',
          warning: '#FF9800',
          info: '#2196F3',
          success: '#4CAF50'
        }
      }
    }
  }),
  
  data: () => ({
    userProfile: {
      genres: [],
      mood: null,
      energy: 50
    },
    availableGenres: [
      'rock', 'pop', 'jazz', 'electronic', 'classical', 
      'hip-hop', 'reggae', 'metal', 'folk', 'r-n-b', 
      'funk', 'indie', 'country', 'blues', 'latin', 
      'soul', 'disco', 'house', 'techno', 'punk', 
      'edm', 'ambient', 'alternative', 'dance', 'reggaeton'
    ],
    moods: [
      'Feliz', 'Triste', 'Eufórico', 'Relajado', 
      'Nostálgico', 'Romántico', 'Energético', 'Concentrado'
    ],
    recommendations: [],
    loading: false,
    showEmptyState: true,
    isAuthenticated: false,
    user: { name: null, email: null },
    alert: {
      show: false,
      message: '',
      type: 'info'
    },
    statsVisible: false
  }),

  computed: {
    recommendationsCount() {
      return this.recommendations.length;
    },
    averageScore() {
      if (this.recommendations.length === 0) return 0;
      const sum = this.recommendations.reduce((acc, song) => acc + (song.score || 0), 0);
      return Math.round(sum / this.recommendations.length);
    }
  },

  created() {
    this.initializeAuth();
  },

  methods: {
    // --- Autenticación ---
    initializeAuth() {
      const hash = window.location.hash.substring(1);
      
      if (hash) {
        window.location.hash = '';
        
        if (hash.startsWith('error=')) {
          const error = hash.replace('error=', '');
          this.showAlert('Error de autenticación: ' + error, 'error');
          return;
        }
        
        this.handleToken(hash);
        return;
      }

      const token = localStorage.getItem('spotify_access_token');
      if (token) {
        this.handleToken(token);
      } else {
        this.showAlert('¡Bienvenido a Symphonaut! Inicia sesión para comenzar.', 'info');
      }
    },
    
    login() {
      window.location.href = `${API_URL}/login`;
    },
    
    handleToken(token) {
      localStorage.setItem('spotify_access_token', token);
      this.setupAxios(token);
      this.isAuthenticated = true;
      this.showAlert('¡Conexión exitosa con Spotify!', 'success');
      this.getUserProfile();
    },
    
    setupAxios(token) {
      axios.defaults.baseURL = API_URL;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios.defaults.headers.post['Content-Type'] = 'application/json';
      axios.defaults.timeout = 60000;
    },

    logout() {
      localStorage.removeItem('spotify_access_token');
      delete axios.defaults.headers.common['Authorization'];
      this.isAuthenticated = false;
      this.user = { name: null, email: null };
      this.recommendations = [];
      this.showEmptyState = true;
      this.showAlert('Sesión cerrada correctamente', 'info');
    },

    // --- API Calls ---
    async getUserProfile() {
      try {
        const response = await axios.get('/me');
        this.user.name = response.data.name;
        this.user.email = response.data.email;
      } catch (error) {
        console.error('Error al obtener perfil:', error);
        this.handleApiError(error);
      }
    },

    async getRecommendations() {
      if (this.userProfile.genres.length === 0) {
        this.showAlert('Por favor, selecciona al menos un género.', 'warning');
        return;
      }
      
      this.loading = true;
      this.showEmptyState = false;
      this.alert.show = false;
      
      try {
        const payload = {
          genres: Array.isArray(this.userProfile.genres) 
            ? this.userProfile.genres 
            : [this.userProfile.genres],
          mood: this.userProfile.mood,
          energy: this.userProfile.energy
        };
        
        console.log('Enviando solicitud:', payload);
        
        const response = await axios.post('/recomendar', payload);
        
        this.recommendations = response.data;
        this.statsVisible = true;
        
        if (response.data.length === 0) {
          this.showAlert('No se encontraron recomendaciones. ¡Intenta otra combinación!', 'info');
          this.showEmptyState = true;
        } else {
          this.showAlert(`¡Encontramos ${response.data.length} canciones para ti!`, 'success');
        }

      } catch (error) {
        console.error('Error al obtener recomendaciones:', error);
        this.handleApiError(error);
        this.showEmptyState = true;
      } finally {
        this.loading = false;
      }
    },
    
    async likeSong(trackId) {
      try {
        await axios.post('/like', { track_id: trackId });
        this.showAlert('¡Canción añadida a tus Me Gusta!', 'success');
      } catch (error) {
        console.error('Error al dar like:', error);
        this.handleApiError(error);
      }
    },

    async playSong(trackUri) {
      try {
        const response = await axios.post('/play', { track_uri: trackUri });
        this.showAlert(response.data.message, 'success');
      } catch (error) {
        console.error('Error al reproducir:', error);
        if (error.response && error.response.status === 404) {
          this.showAlert('Abre Spotify en tu dispositivo para reproducir música.', 'warning');
        } else {
          this.handleApiError(error);
        }
      }
    },

    // --- UI Helpers ---
    showAlert(message, type = 'info') {
      this.alert.message = message;
      this.alert.type = type;
      this.alert.show = true;
      setTimeout(() => { this.alert.show = false; }, 5000);
    },

    handleApiError(error) {
      let message = 'Ocurrió un error inesperado.';
      
      if (error.response) {
        if (error.response.status === 401) {
          this.logout();
          message = 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.';
        } else {
          message = error.response.data.message || error.response.data.error || `Error ${error.response.status}`;
        }
      } else if (error.code === 'ECONNABORTED') {
        message = 'La petición tardó demasiado. Verifica tu conexión.';
      } else if (!error.response) {
        message = 'No se pudo conectar con el servidor.';
      }
      
      this.showAlert(message, 'error');
      console.error('Error de API:', error);
    },

    clearRecommendations() {
      this.recommendations = [];
      this.showEmptyState = true;
      this.statsVisible = false;
    }
  }
});