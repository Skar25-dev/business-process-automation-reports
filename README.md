# 📊 Business Process Automation Reports (BPAR)

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema integral de automatización para la generación y distribución de reportes empresariales. Transforma datos crudos en informes profesionales y los gestiona automáticamente mediante una interfaz web moderna.
---

## 🚀 Descripción

BPAR es una solución completa diseñada para eliminar la carga operativa manual en la gestión de datos. El sistema automatiza el ciclo de vida completo del reporte:
- **Extracción:** Consulta dinámica a bases de datos (SQLite/PostgreSQL).
- **Procesamiento:** Limpieza y cálculo de métricas mediante **Pandas**.
- **Generación:** Creación de archivos profesionales con **Openpyxl**.
- **Distribución:** Envío automático por **Email (SMTP)** con archivos adjuntos.
- **Gestión Web:** Panel de control para ejecución manual, historial y configuración.

---

## ✨ Funcionalidades

✅ **Dashboard Web:** Interfaz visual (Bootstrap 5) para monitorear y descargar reportes.  
✅ **Panel de Configuración:** Cambia emails, nombres de empresa y horarios desde el navegador.  
✅ **Automatización 24/7:** Robot programador (Scheduler) para envíos desatendidos.  
✅ **Ejecución On-Demand:** Botón manual para generar reportes al instante.  
✅ **Persistencia Dinámica:** Los cambios en la web actualizan el sistema en tiempo real.  
✅ **Arquitectura Multi-DB:** Soporte nativo para entornos de desarrollo y producción.  

---

## 🏗️ Arquitectura del Sistema

El sistema utiliza una arquitectura modular donde el Frontend, el Backend y el Robot de automatización trabajan en sincronía.

### 🔵 Flujo de Trabajo
```text
[ Usuario ] <───► [ Dashboard Web ] ◄───► [ Panel de Ajustes ]
                           │                      │
                           ▼                      ▼
[ FastAPI ] ◄───► [ Background Tasks ] ◄───► [ settings.json ]
      │                    │                      │
      ▼                    ▼                      ▼
[ DB SQL ] ───► [ Pandas Engine ] ───► [ Excel ] ───► [ Email SMTP ]
```

### 📂 Estructura del Proyecto
```
├── app/
│   ├── main.py            # Dashboard, API, Rutas de descarga y Ajustes
│   ├── config.py          # Cerebro de validación (Pydantic)
│   ├── database.py        # Conector flexible SQLite/Postgres
│   ├── models.py          # Modelos de datos de negocio
│   ├── services/          # 🧠 Lógica de Negocio
│   │   ├── report_service.py    # Procesamiento de datos
│   │   ├── email_service.py     # Envío de correos
│   │   └── scheduler_service.py # Robot programador
│   ├── templates/         # 📄 Vistas HTML (Jinja2)
│   └── static/            # 🎨 Estilos modulares (CSS)
├── config/                # Ajustes persistentes (settings.json)
├── data/                  # Almacenamiento de DB local
├── reports/               # Histórico de archivos generados (.xlsx)
├── tests/                 # 📂 Suite de Pruebas Automatizadas
├── .env                   # Secretos y Passwords (Privado)
├── .env.example           # Plantilla de secretos
├── seed_data.py           # Generador de datos iniciales
├── requirements.txt
└── README.md
```
### 🛠️ Tecnologías Utilizadas
- **Core:** Python 3.12+, FastAPI, SQLAlchemy.
- **Data Science:** Pandas, Openpyxl.
- **Automatización:** APScheduler.
- **Frontend:** FJinja2, Bootstrap5, JavaScript (Fetch API).
- **Seguridad:** Pydantic Settings, Dotenv, Watchfiles.

### ⚙️ Instalación y Configuración

**1. Preparar entorno:**
```Bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**2. Configurar Secretos:**

- Copia `.env.example` a `.env.`

- Rellena tus credenciales de Email (Password de aplicación) y Base de Datos.

**3. Poblar Base de Datos e iniciar:**

```Bash
python seed_data.py
uvicorn app.main:app --reload --reload-include "*.json" --reload-include "*.html" --reload-include "*.css" --port 8000
```

**4. Acceso:**

- **Dashboard:** `http://localhost:8000`
- **Ajustes:** `http://localhost:8000/settings` 