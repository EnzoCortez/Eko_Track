
# Eko Track

Eko Track es una aplicación web desarrollada en Flask para la gestión y reporte de problemas ambientales en la ciudad de Quito. Permite a los ciudadanos reportar incidentes y ayuda a la administración municipal a priorizar intervenciones basándose en la criticidad del problema y el presupuesto disponible.

## 📋 Características Principales

*   **Sistema de Reportes Ciudadanos**: Los usuarios pueden reportar problemas ambientales clasificándolos por categoría (Agua, Aire, Residuos, Ruido), nivel de criticidad y ubicación (sectores de Quito).
*   **Panel de Administración**: Interfaz completa para gestionar usuarios, reportes, categorías y configuraciones municipales.
*   **Gestión Presupuestaria Inteligente**:
    *   Configuración de presupuesto municipal total.
    *   **Matriz de Prioridad-Presupuesto**: Asignación automática de presupuestos sugeridos basada en la categoría y el nivel de prioridad del reporte.
    *   Cálculo automático de intervenciones sugeridas según el presupuesto disponible.
*   **Autenticación y Roles**: Sistema de registro e inicio de sesión con roles diferenciados (Usuario y Administrador).

## 🛠️ Tecnologías Utilizadas

*   **Backend**: Python 3, Flask
*   **Base de Datos**: SQLAlchemy ORM (SQLite por defecto, compatible con PostgreSQL)
*   **Admin Interface**: Flask-Admin
*   **Autenticación**: Flask-Login, Werkzeug Security
*   **Formularios**: Flask-WTF
*   **Servidor**: Gunicorn (listo para producción)

## 🚀 Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1.  **Clonar el repositorio**
    ```bash
    git clone <(https://github.com/EnzoCortez/Eko_Track.git)>
    cd eko_track
    ```

2.  **Crear un entorno virtual**
    ```bash
    python -m venv venv
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación**
    ```bash
    python app.py
    ```
    La aplicación estará disponible en `http://127.0.0.1:5000`.

## 👤 Usuarios por Defecto

Al ejecutar la aplicación por primera vez, se crea automáticamente un usuario administrador:

*   **Usuario**: `admin`
*   **Contraseña**: `admin`

## 📂 Estructura del Proyecto

*   `app.py`: Punto de entrada de la aplicación, configuración y rutas principales.
*   `models.py`: Definición de modelos de base de datos (User, Report, ReportCategory, MunicipalitySettings, PriorityBudgetMatrix).
*   `admin_config.py`: Configuración y vistas personalizadas del panel de administración.
*   `templates/`: Plantillas HTML para el frontend.
*   `requirements.txt`: Lista de dependencias del proyecto.

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para mejoras y correcciones.

