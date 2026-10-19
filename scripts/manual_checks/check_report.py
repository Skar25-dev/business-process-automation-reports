from app.database import SessionLocal
from app.services.report_service import ReportService

def test():
    print("Iniciando generación de reporte...")
    db = SessionLocal()
    try:
        service = ReportService(db)
        path = service.get_report(report_type="ventas", category="Hogar")
        if path:
            print(f"¡Éxito! Reporte guardado en {path}")
        else:
            print("No hay datos para generar el reporte")
    finally:
        db.close()
    
if __name__ == "__main__":
    test()