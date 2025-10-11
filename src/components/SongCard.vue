<template>
    <v-card class="song-card" :color="cardColor" dark elevation="4" @click="playSong">
        <div class="d-flex flex-no-wrap justify-space-between">
            <!-- Portada del álbum -->
            <v-avatar class="ma-3" size="100" tile>
                <v-img :src="song.cover || 'https://via.placeholder.com/100'"></v-img>
            </v-avatar>
            
            <!-- Detalles de la canción -->
            <div>
                <v-card-title class="text-h6">{{ song.title }}</v-card-title>
                <v-card-subtitle>{{ song.artist }}</v-card-subtitle>
                <v-card-text>
                    <div>
                        <v-chip small class="mr-2">{{ song.genre }}</v-chip>
                        <v-chip small>
                            <v-icon small left>mdi-metronome</v-icon>
                            {{ song.bpm }} BPM
                        </v-chip>
                    </div>
                    <div class="mt-2">
                        <v-rating
                            :value="song.energy / 20"
                            length="5"
                            color="amber"
                            dense
                            readonly
                            size="18"
                        ></v-rating>
                    </div>
                    <div class="caption mt-2">{{ song.reason }}</div>
                </v-card-text>
            </div>
        </div>
        
        <!-- Botón de reproducción -->
        <v-btn 
            absolute 
            bottom 
            right 
            fab 
            small 
            color="primary"
            @click.stop="playSong"
        >
            <v-icon>mdi-play</v-icon>
        </v-btn>
    </v-card>
</template>

<script>
export default {
    props: {
        song: Object
    },
    computed: {
        cardColor() {
            const colors = {
                Rock: 'red darken-2',
                Pop: 'blue darken-2',
                Jazz: 'amber darken-3',
                Electronic: 'purple darken-2',
                Clásica: 'teal darken-2',
                HipHop: 'orange darken-3'
            };
            return colors[this.song.genre] || 'indigo darken-2';
        }
    },
    methods: {
        playSong() {
            if (this.song.preview_url) {
                const audio = new Audio(this.song.preview_url);
                audio.play();
            } else {
                alert(`Reproduciendo: ${this.song.title}`);
            }
        }
    }
};
</script>

<style scoped>
.song-card {
    transition: transform 0.3s, box-shadow 0.3s;
    cursor: pointer;
}
.song-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 16px rgba(0,0,0,0.2) !important;
}
</style>