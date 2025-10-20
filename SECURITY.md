# 🔒 Guía de Seguridad - Symphonaut

## Mejores Prácticas Implementadas

### ✅ Variables de Entorno
- ✅ Todas las credenciales sensibles están en variables de entorno
- ✅ Nunca se hardcodean en el código
- ✅ `.env` está en `.gitignore`
- ✅ Se proporciona `.env.example` sin datos reales

### ✅ Autenticación
- ✅ OAuth 2.0 con Spotify (estándar de industria)
- ✅ Tokens de acceso manejados de forma segura
- ✅ Validación de headers en cada request
- ✅ Manejo de expiración de tokens

### ✅ Backend
- ✅ CORS configurado apropiadamente
- ✅ Validación de entrada en todas las rutas
- ✅ Manejo de errores robusto
- ✅ Logging para auditoría
- ✅ Rate limiting (por implementar en producción)
- ✅ Decoradores de autenticación reutilizables
- ✅ Sin exposición de información sensible en logs

### ✅ Frontend
- ✅ Tokens almacenados en localStorage (no en cookies accesibles por JS)
- ✅ Validación de formularios
- ✅ Manejo apropiado de errores de API
- ✅ URLs de API configurables por entorno
- ✅ No se exponen credenciales en el código del cliente

## 🚨 Checklist de Seguridad Antes de Deploy

### Pre-Deployment
- [ ] Revisar que `.env` esté en `.gitignore`
- [ ] Verificar que no hay credenciales en el código
- [ ] Confirmar que todas las variables de entorno están configuradas en Render
- [ ] Validar que las Redirect URIs en Spotify sean correctas
- [ ] Probar el flujo completo de autenticación
- [ ] Verificar que CORS esté configurado correctamente

### Post-Deployment
- [ ] Cambiar las credenciales de desarrollo si se usaron en testing
- [ ] Verificar los logs en busca de información sensible
- [ ] Probar todos los endpoints desde el frontend en producción
- [ ] Monitorear el primer día en busca de errores
- [ ] Configurar alertas de errores (opcional)

## 🔐 Manejo de Credenciales

### Spotify API Keys

**NUNCA HACER:**
```python
# ❌ MAL - Credenciales hardcodeadas
SPOTIPY_CLIENT_ID = "abc123xyz789"
SPOTIPY_CLIENT_SECRET = "secret123"
```

**SIEMPRE HACER:**
```python
# ✅ BIEN - Usar variables de entorno
SPOTIPY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
```

### Tokens de Acceso

**NUNCA HACER:**
```javascript
// ❌ MAL - Token en el código
const token = "BQDc7x5y..."
```

**SIEMPRE HACER:**
```javascript
// ✅ BIEN - Token desde localStorage o header
const token = localStorage.getItem('spotify_access_token')
```

## 🛡️ Mejoras de Seguridad Recomendadas

### Nivel 1 - Básico (Implementado)
- ✅ Variables de entorno
- ✅ HTTPS en producción (Render lo proporciona)
- ✅ Validación de entrada
- ✅ Manejo de errores

### Nivel 2 - Intermedio (Recomendado)
```python
# Implementar rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/recomendar', methods=['POST'])
@limiter.limit("10 per minute")
def recomendar():
    # ... tu código
```

### Nivel 3 - Avanzado (Opcional)
```python
# Implementar CSRF protection
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Implementar Content Security Policy
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

## 🚫 Vulnerabilidades Comunes y Cómo Evitarlas

### 1. Exposición de Credenciales

**Riesgo:** Subir credenciales a GitHub
**Solución:** 
```bash
# Añadir a .gitignore
.env
.env.local
.env.*.local
*.env
```

### 2. Cross-Site Scripting (XSS)

**Riesgo:** Inyección de código malicioso
**Solución:** Vue.js escapa automáticamente el contenido, pero nunca uses `v-html` con datos del usuario

```javascript
// ❌ MAL
<div v-html="userInput"></div>

// ✅ BIEN
<div>{{ userInput }}</div>
```

### 3. SQL Injection

**Riesgo:** N/A en este proyecto (no usamos SQL directamente)
**Nota:** Spotipy maneja esto internamente

### 4. CORS Misconfiguration

**Riesgo:** Permitir orígenes no autorizados
**Solución Implementada:**
```python
CORS(app, 
     origins=[FRONTEND_URL],  # Solo tu frontend
     supports_credentials=True)
```

### 5. Sensitive Data Exposure

**Riesgo:** Logs con información sensible
**Solución:**
```python
# ❌ MAL
logger.info(f"Token: {access_token}")

# ✅ BIEN
logger.info(f"Token recibido, comienza con: {access_token[:10]}...")
```

## 🔍 Auditoría de Seguridad

### Revisar Logs Regularmente

```bash
# En Render Dashboard > Logs
# Buscar por:
- Errores 401/403 (intentos de acceso no autorizado)
- Errores 500 (problemas del servidor)
- Patrones inusuales de requests
```

### Monitorear Uso de API

```python
# Añadir contador de requests en el backend
request_count = {}

@app.before_request
def count_requests():
    ip = request.remote_addr
    request_count[ip] = request_count.get(ip, 0) + 1
```

## 🚨 Qué Hacer si Hay una Brecha de Seguridad

### Pasos Inmediatos

1. **Si expusiste credenciales en GitHub:**
   ```bash
   # 1. Rotar credenciales inmediatamente en Spotify Dashboard
   # 2. Actualizar variables de entorno en Render
   # 3. Hacer git commit para eliminar las credenciales
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   ```

2. **Si detectas acceso no autorizado:**
   - Revocar todos los tokens activos
   - Cambiar todas las credenciales
   - Revisar logs para entender el alcance
   - Notificar a los usuarios si es necesario

3. **Si encuentras una vulnerabilidad:**
   - No la hagas pública inmediatamente
   - Corrígela primero
   - Luego documenta qué pasó y cómo se solucionó

## 📋 Checklist de Mantenimiento de Seguridad

### Mensual
- [ ] Revisar logs en busca de anomalías
- [ ] Verificar que las dependencias estén actualizadas
- [ ] Comprobar que las variables de entorno sigan configuradas

### Trimestral
- [ ] Actualizar dependencias (Flask, Spotipy, etc.)
- [ ] Revisar políticas de CORS
- [ ] Auditar código en busca de vulnerabilidades

### Anual
- [ ] Rotar credenciales de API
- [ ] Revisar permisos de Spotify OAuth
- [ ] Actualizar políticas de seguridad

## 🔄 Actualización de Dependencias

```bash
# Verificar dependencias desactualizadas
pip list --outdated

# Actualizar requirements.txt
pip install --upgrade Flask spotipy requests

# Generar nuevo requirements.txt
pip freeze > requirements.txt

# IMPORTANTE: Probar todo antes de deployar
```

## 📚 Recursos de Seguridad

### Documentación Oficial
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Spotify API Security Best Practices](https://developer.spotify.com/documentation/web-api/concepts/security)
- [Flask Security](https://flask.palletsprojects.com/en/3.0.x/security/)

### Herramientas de Auditoría
- [Safety](https://pyup.io/safety/) - Escaneo de vulnerabilidades en dependencias Python
- [Bandit](https://bandit.readthedocs.io/) - Análisis de seguridad para Python
- [npm audit](https://docs.npmjs.com/cli/v8/commands/npm-audit) - Para dependencias de JavaScript

### Ejemplo de Uso de Safety

```bash
# Instalar
pip install safety

# Escanear vulnerabilidades
safety check

# Generar reporte
safety check --json > security-report.json
```

## 🎓 Mejores Prácticas Generales

1. **Principio de Mínimo Privilegio**
   - Solo solicita los permisos de Spotify que realmente necesitas
   - Actualmente usamos todos estos scopes, considera si todos son necesarios

2. **Defensa en Profundidad**
   - Múltiples capas de seguridad (validación en frontend y backend)
   - No confíes solo en una medida de seguridad

3. **Fail Secure**
   - Si algo falla, debe fallar de forma segura
   - No exponer información sensible en mensajes de error

4. **Keep it Simple**
   - El código complejo es más difícil de asegurar
   - Mantén la arquitectura simple y clara

## 📞 Reportar Vulnerabilidades

Si encuentras una vulnerabilidad de seguridad en este proyecto:

1. **NO** la hagas pública
2. Envía un email privado a: fabianicorporation@gmail.com
3. Incluye:
   - Descripción detallada de la vulnerabilidad
   - Pasos para reproducirla
   - Impacto potencial
   - Sugerencias de solución (opcional)

## ✅ Certificación de Seguridad

Este proyecto implementa:
- ✅ Autenticación OAuth 2.0
- ✅ Encriptación en tránsito (HTTPS)
- ✅ Variables de entorno para secretos
- ✅ Validación de entrada
- ✅ Manejo seguro de errores
- ✅ Logging sin información sensible
- ✅ CORS configurado apropiadamente

---

**Última actualización:** Octubre 2025

**Versión de este documento:** 1.0

**Mantenedor:** Carlos Fabiani Jimenez Ceja