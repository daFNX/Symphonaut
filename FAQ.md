# ❓ Preguntas Frecuentes (FAQ) - Symphonaut

## 📱 General

### ¿Qué es Symphonaut?
Symphonaut es un sistema de recomendaciones musicales inteligentes que utiliza la API de Spotify para sugerir canciones basadas en tus géneros favoritos, estado de ánimo y nivel de energía preferido.

### ¿Es gratis?
Sí, Symphonaut es completamente gratuito. Sin embargo, necesitas una cuenta de Spotify (gratuita o Premium) para usarlo.

### ¿Necesito Spotify Premium?
- **Para recomendaciones**: No, cualquier cuenta de Spotify funciona
- **Para reproducir música**: Sí, necesitas Spotify Premium para reproducir canciones directamente desde Symphonaut

### ¿Funciona en móviles?
Sí, Symphonaut es responsive y funciona en:
- 📱 Teléfonos móviles (iOS y Android)
- 💻 Computadoras de escritorio
- 📱 Tablets

## 🔐 Autenticación y Seguridad

### ¿Por qué necesito iniciar sesión con Spotify?
Necesitamos autenticación para:
- Acceder a tus preferencias musicales
- Guardar canciones en tu biblioteca
- Controlar la reproducción en tus dispositivos
- Obtener recomendaciones personalizadas

### ¿Es seguro conectar mi cuenta de Spotify?
Sí, completamente seguro:
- ✅ Usamos OAuth 2.0 (estándar de industria)
- ✅ No almacenamos tu contraseña
- ✅ Solo pedimos los permisos necesarios
- ✅ Puedes revocar el acceso en cualquier momento

### ¿Cómo revoco el acceso de Symphonaut?
1. Ve a [Spotify Account](https://www.spotify.com/account/apps/)
2. Encuentra "Symphonaut" en la lista
3. Click en "REMOVE ACCESS"

### ¿Symphonaut puede ver mi contraseña?
No. Nunca vemos ni almacenamos tu contraseña. La autenticación la maneja directamente Spotify.

## 🎵 Recomendaciones

### ¿Cómo funcionan las recomendaciones?
Symphonaut analiza:
1. **Géneros seleccionados**: Los géneros que eliges en tu perfil
2. **Tus artistas favoritos**: Obtenidos de tu historial de Spotify
3. **Mood y energía**: Los parámetros que configuras
4. **Popularidad**: Priorizamos canciones que otros usuarios disfrutan

### ¿Por qué no obtengo recomendaciones?
Posibles causas:
- ❌ No seleccionaste ningún género
- ❌ La combinación de géneros es muy específica
- ❌ Tu sesión expiró (intenta cerrar sesión y volver a entrar)
- ❌ Problemas de conexión con Spotify API

**Solución:** Intenta con géneros más populares como "pop", "rock" o "electronic"

### ¿Puedo obtener más de 20 recomendaciones?
Actualmente el límite es 20 canciones por búsqueda para mantener tiempos de respuesta rápidos. Puedes hacer múltiples búsquedas con diferentes parámetros.

### ¿Las recomendaciones se actualizan en tiempo real?
Sí, cada vez que haces click en "Buscar Música", obtienes recomendaciones frescas basadas en tu perfil actual.

## 🎮 Funcionalidad

### ¿Cómo reproduzco una canción?
1. Click en el botón de play ▶️ en la tarjeta de la canción
2. O hover sobre la imagen del álbum y click en el botón grande de play

**Nota:** Necesitas tener Spotify abierto en algún dispositivo

### ¿Por qué no puedo reproducir canciones?
Causas comunes:
- ❌ No tienes Spotify Premium
- ❌ No tienes Spotify abierto en ningún dispositivo
- ❌ Tu dispositivo no está siendo detectado

**Solución:**
1. Abre Spotify en tu computadora, teléfono o navegador
2. Reproduce cualquier canción (para activar el dispositivo)
3. Intenta de nuevo en Symphonaut

### ¿Cómo guardo una canción en "Me gusta"?
Click en el ícono de corazón ❤️ en la tarjeta de la canción. La canción se añadirá automáticamente a tu biblioteca de Spotify.

### ¿Puedo crear playlists?
Actualmente no, pero puedes:
- Guardar canciones individualmente con "Me gusta"
- Reproducirlas en Spotify
- Crear playlists manualmente en Spotify con las canciones que descubras

## 🔧 Problemas Técnicos

### La página no carga / aparece en blanco
**Soluciones:**
1. Limpia la caché del navegador
2. Intenta en modo incógnito
3. Verifica tu conexión a internet
4. Prueba con otro navegador

### Error: "Tu sesión ha expirado"
**Solución:**
1. Click en cerrar sesión (si está disponible)
2. Borra el localStorage: 
   - Abre DevTools (F12)
   - Consola → `localStorage.clear()`
3. Recarga la página
4. Vuelve a iniciar sesión

### Error: "No se pudo conectar con el servidor"
Esto significa que el backend está apagado o no responde.

**Si eres el desarrollador:**
- Verifica que el backend esté corriendo en Render
- Revisa los logs en Render Dashboard
- Asegúrate de que la URL del backend en `app.js` sea correcta

### El backend tarda mucho en responder
Los servicios gratuitos de Render se "duermen" después de 15 minutos de inactividad. El primer request puede tardar 30-60 segundos en "despertar" el servidor.

**Solución:**
- Espera pacientemente en el primer request
- Considera implementar el keep-alive script (ver DEPLOYMENT.md)

### Error de CORS
```
Access to fetch at 'https://backend.com' from origin 'https://frontend.com' has been blocked by CORS policy
```

**Solución:**
- Verifica que `FRONTEND_URL` esté configurado correctamente en Render
- Asegúrate de que coincida exactamente con tu URL de frontend

## 💻 Para Desarrolladores

### ¿Puedo usar este código para mi proyecto?
Sí, el proyecto está bajo licencia MIT. Puedes:
- ✅ Usarlo comercialmente
- ✅ Modificarlo
- ✅ Distribuirlo
- ✅ Usar partes del código

**Solo debes:** Mantener el aviso de copyright original

### ¿Cómo contribuyo al proyecto?
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz tus cambios
4. Envía un Pull Request

Ver detalles en `README.md`

### ¿Cómo corro el proyecto localmente?
Ver la sección "Configuración Local" en `README.md`

### ¿Puedo añadir más features?
¡Absolutamente! Algunas ideas:
- Sistema de playlists personalizadas
- Compartir recomendaciones en redes sociales
- Historial de búsquedas
- Filtros avanzados (BPM, año, etc.)
- Modo oscuro
- Multi-idioma

### ¿Qué tecnologías usa?
**Backend:**
- Python 3.11
- Flask
- Spotipy

**Frontend:**
- Vue.js 2
- Vuetify 2
- Axios

### ¿Por qué Vue 2 y no Vue 3?
Para mantener compatibilidad con Vuetify 2, que es más estable y tiene mejor documentación. Puedes migrar a Vue 3 + Vuetify 3 si lo prefieres.

## 🌐 Deployment

### ¿Cuánto cuesta hostear en Render?
**Gratis** si usas el plan Free, que incluye:
- ✅ 750 horas de compute por mes
- ✅ HTTPS automático
- ✅ Deployment automático desde GitHub
- ❌ El servicio se duerme después de 15 min de inactividad

### ¿Puedo usar otro servicio de hosting?
Sí, Symphonaut puede desplegarse en:
- Heroku
- Railway
- Vercel (frontend)
- Netlify (frontend)
- AWS / Google Cloud / Azure
- Cualquier servidor con Python

### ¿Necesito un dominio personalizado?
No, Render proporciona subdominios gratuitos:
- `tu-app.onrender.com`

Pero puedes conectar tu propio dominio si lo prefieres (ver documentación de Render)

### ¿Cómo actualizo la aplicación en producción?
Simplemente haz push a GitHub:
```bash
git add .
git commit -m "Mis cambios"
git push
```

Render detectará los cambios y redesplegará automáticamente.

## 📊 Límites y Restricciones

### Límites de la API de Spotify
- Rate limit: 180 requests por minuto
- Este proyecto maneja estos límites automáticamente

### Límites de Render (Free Tier)
- 750 horas de compute/mes (suficiente para un proyecto personal)
- 100GB de ancho de banda/mes
- El servicio se duerme después de 15 minutos de inactividad

### ¿Qué pasa si supero los límites?
- **Spotify:** Recibirás un error 429. El backend lo maneja automáticamente
- **Render:** Tu aplicación dejará de funcionar hasta el siguiente mes (o puedes upgradear al plan pago)

## 🐛 Reportar Bugs

### Encontré un bug, ¿qué hago?
1. Ve al repositorio de GitHub
2. Click en "Issues"
3. "New Issue"
4. Describe:
   - Qué hiciste
   - Qué esperabas que pasara
   - Qué pasó en realidad
   - Capturas de pantalla (si es posible)
   - Navegador y versión

### ¿Hay un roadmap del proyecto?
Puedes ver features planeados en:
- GitHub Issues (etiquetados como "enhancement")
- GitHub Projects (si está configurado)

## 💡 Tips y Trucos

### Mejores prácticas para recomendaciones
- 🎯 Selecciona 2-4 géneros (no demasiados)
- 🎭 Prueba diferentes moods
- ⚡ Ajusta la energía según tu actividad (estudio = baja, ejercicio = alta)
- 🔄 Haz múltiples búsquedas con pequeñas variaciones

### Atajos de teclado
Actualmente no hay atajos, pero puedes contribuir añadiéndolos!

### Mejora la experiencia
- Usa Spotify en tu dispositivo mientras navegas
- Crea una cuenta Premium para reproducción
- Dale like a las canciones que te gusten para mejorar tu perfil de Spotify

## 📧 Contacto

### ¿Cómo te contacto?
- 📧 Email: fabianicorporation@gmail.com
- 🐙 GitHub: [@daFNX](https://github.com/daFNX)
- 📸 Twitter: [@da_fnx](https://www.instagram.com/da_fnx)

### ¿Ofrecen soporte?
Este es un proyecto open-source mantenido en el tiempo libre. Haremos nuestro mejor esfuerzo para responder preguntas, pero no hay garantías de soporte 24/7.

---

## 🔄 Actualizaciones de este FAQ

**Última actualización:** Octubre 2025

¿No encontraste tu pregunta? [Abre un issue en GitHub](https://github.com/daFNX/symphonaut/issues)