import os
from pathlib import Path
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import SessionLocal
from app.services.report_service import ReportService
from app.services.email_service import EmailService
from app.services.scheduler_service import start_scheduler
from contextlib import asynccontextmanager
import json
from app.config import settings, load_settings


BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="BPAR Dashboard", lifespan=lifespan)

if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# --- RUTAS DE LA INTERFAZ WEB ---

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not REPORTS_DIR.exists():
        REPORTS_DIR.mkdir(exist_ok=True)
        
    report_files = sorted(
        [f for f in os.listdir(REPORTS_DIR) if f.endswith('.xlsx')],
        reverse=True
    )
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "reports": report_files,
        "app_name": "BPAR Dashboard"
    })

@app.get("/download/{filename}")
async def download_report(filename: str):
    file_path = REPORTS_DIR / filename
    
    print(f"🔍 DEBUG: Intentando descargar {file_path}")
    
    if file_path.exists():
        return FileResponse(
            path=str(file_path), 
            filename=filename,
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    print(f"ERROR: El archivo no existe en {file_path}")
    raise HTTPException(status_code=404, detail="Archivo no encontrado")

# --- RUTAS DE ACCIÓN (API) ---

@app.post("/run-report")
async def run_report_manual(background_tasks: BackgroundTasks):
    async def task():
        print("🚀 Iniciando reporte manual desde la web...")
        db = SessionLocal()
        try:
            report_service = ReportService(db)
            email_service = EmailService()
            path = report_service.get_report(report_type="ventas")
            if path:
                await email_service.send_report_email(file_path=path)
                print(f"Reporte manual enviado con éxito.")
        except Exception as e:
            print(f"Error en reporte manual: {e}")
        finally:
            db.close()
    
    background_tasks.add_task(task)
    return {"status": "Proceso de reporte iniciado en segundo plano"}

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "settings": settings,
        "app_name": settings.app_name
    })

@app.post("/settings")
async def update_settings(
    app_name: str = Form(...),
    company_name: str = Form(...),
    contact_email: str = Form(...),
    report_schedule: str = Form(...),
    db_type: str = Form(...)
):
    # Crear el nuevo diccionario para el JSON
    new_config = {
        "app_name": app_name,
        "company_name": company_name,
        "contact_email": contact_email,
        "report_schedule": report_schedule,
        "db_type": db_type,
        "report_settings": settings.report_settings # Mantenemos los internos
    }

    # Guardar físicamente
    with open("config/settings.json", "w") as f:
        json.dump(new_config, f, indent=4)

    # Respuesta con alerta y redirección
    html_content = """
    <script>
        alert('✅ ¡Configuración guardada! El sistema se está reiniciando para aplicar los cambios.');
        window.location.href = '/settings';
    </script>
    """
    return HTMLResponse(content=html_content)
