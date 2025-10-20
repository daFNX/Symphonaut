"""
Script opcional para mantener tu servicio de Render activo.
Los servicios gratuitos de Render se duermen después de 15 minutos de inactividad.

Opciones para usarlo:

1. Ejecutarlo localmente con cron (Linux/Mac):
   */14 * * * * python3 /ruta/a/keep_alive.py

2. Usar un servicio como GitHub Actions (recomendado)

3. Usar servicios de terceros como Uptime Robot o cron-job.org
"""

import requests
import time
import logging
from datetime import datetime

# Configura tu URL del backend aquí
BACKEND_URL = "https://tu-backend.onrender.com"

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ping_service():
    """Hace ping al endpoint de health check"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=30)
        if response.status_code == 200:
            logger.info(f"✅ Servicio activo - Status: {response.status_code}")
            return True
        else:
            logger.warning(f"⚠️ Respuesta inesperada - Status: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        logger.error("❌ Timeout - El servicio tardó demasiado en responder")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Error al hacer ping: {e}")
        return False

def main():
    """Función principal"""
    logger.info("🚀 Iniciando keep-alive script")
    logger.info(f"🎯 Target: {BACKEND_URL}")
    
    # Hacer ping una vez
    success = ping_service()
    
    if success:
        logger.info("✅ Keep-alive completado exitosamente")
    else:
        logger.error("❌ Keep-alive falló")
    
    return success

if __name__ == "__main__":
    main()