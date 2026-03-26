# 📊 Business Process Automation Reports (BPAR)

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-05998b.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema integral de automatización para la generación y distribución de reportes empresariales. Transforma datos crudos en informes profesionales (Excel/PDF) y los distribuye automáticamente, eliminando la carga operativa manual y reduciendo errores humanos.

---

## 🚀 Descripción

BPAR es una solución diseñada para empresas que requieren reportes recurrentes. El sistema automatiza el ciclo de vida completo del dato:
- **Extracción:** Consulta flexible a bases de datos relacionales.
- **Procesamiento:** Limpieza y cálculo de métricas mediante el motor de Pandas.
- **Generación:** Creación de archivos profesionales con formato avanzado.
- **Distribución:** Envío automático por Email y gestión mediante una interfaz Web.

---

## 💡 Caso de Uso Real
Ideal para departamentos de Finanzas, Ventas u Operaciones que actualmente dedican horas diarias a exportar datos de un ERP/CRM, darles formato en Excel y enviarlos por correo. **BPAR automatiza este proceso en segundos**, garantizando estandarización y puntualidad.

---

## ✨ Funcionalidades

✅ **Generación Automática:** Reportes listos sin intervención manual.  
✅ **Dashboard Web:** Interfaz visual para gestionar, disparar y descargar reportes.  
✅ **Arquitectura Multi-DB:** Soporte nativo para **SQLite** (desarrollo) y **PostgreSQL** (producción).  
✅ **Configuración Segura:** Gestión híbrida mediante archivos `.env` (secretos) y `settings.json` (ajustes de usuario).  
✅ **Validación Robusta:** Uso de **Pydantic** para garantizar la integridad de las configuraciones.  
✅ **Programación Inteligente:** Tareas programadas totalmente configurables.  

---

## 🏗️ Arquitectura del Sistema

El sistema sigue un diseño modular por capas, permitiendo que la lógica de negocio sea independiente de la infraestructura de base de datos o la interfaz.

### 🔵 Flujo de Datos
```text
[ Usuario ] <───► [ Dashboard Web (Jinja2) ] <───► [ FastAPI API ]
                                                        │
      ┌─────────────────────────────────────────────────┤
      ▼                                                 ▼
[ Config Layer ] ◄── (.env / JSON)            [ Service Layer ]
      │                                                 │
      ▼                                         ┌───────┴───────┐
[ Base de Datos ] ◄── (SQLAlchemy)              ▼               ▼
(SQLite / Postgres)                     [ Pandas Engine ] ──► [ Excel/PDF ]
```
### 🛠️ Componentes Principales
- Configuración (Pydantic): Valida y centraliza todos los parámetros del sistema.
- Acceso a Datos (DAL): Abstracción de base de datos mediante SQLAlchemy ORM.
- Procesamiento (Utils): Transformación de datos y diseño de archivos con Pandas y Openpyxl.
- Servicios: Gestión de lógica de envío (Email), históricos y agenda (APScheduler).

### 🛠️-  Tecnologías Utilizadas
- Backend: Python 3.12+, FastAPI, SQLAlchemy.
- Análisis de Datos: Pandas, Openpyxl.
- Validación: Pydantic Settings.
- Frontend: Jinja2, Bootstrap (Próximamente).
- Seguridad: Python-dotenv.

### 📂 Estructura del Proyecto
```
├── app/
│   ├── main.py            # Entrada de la API y Scheduler
│   ├── config.py          # Cerebro de configuración y validación (Día 2)
│   ├── database.py        # Conector flexible SQLite/Postgres
│   ├── models.py          # Modelos de datos (SQLAlchemy)
│   ├── services/          # Lógica (Email, Reportes, Scheduler)
│   ├── utils/             # Generadores (Excel, PDF)
│   ├── templates/         # Vistas HTML para el Dashboard
│   └── static/            # Estilos CSS y activos visuales
├── config/                # Ajustes de usuario (settings.json)
├── data/                  # Almacenamiento local de base de datos
├── reports/               # Histórico de reportes generados
├── .env                   # Secretos y passwords (Excluido de Git)
├── .env.example           # Plantilla de secretos para nuevos entornos
├── .gitignore             # Filtro de archivos sensibles
├── seed_data.py           # Generador de datos iniciales (Día 1)
├── test_config.py         # Script de verificación de sistema (Día 2)
├── requirements.txt
└── README.md
```
### ⚙️ Instalación y Configuración
Clonar y preparar entorno:

```
Bash
git clone https://github.com/tu-usuario/bpa-reports.git
cd bpa-reports
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Configurar Secretos:
- Copia el archivo de ejemplo: **cp .env.example .env**
- Edita el archivo .env con tus credenciales reales (DB, Email).
- Poblar Base de Datos:
```
python seed_data.py
```
- Verificar Sistema:
```
python test_config.py
```
Si todo es correcto, verás el mensaje: **"Sistema configurado para: DESARROLLO (SQLite)"**