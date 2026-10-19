import asyncio
from app.database import SessionLocal
from app.services.report_service import ReportService
from app.services.email_service import EmailService

async def main():
    print("Iniciando proceso completo...")
    db = SessionLocal()

    try:
        report_service = ReportService(db)
        path = report_service.get_report(report_type="ventas", category="Alimentos")

        if path:
            print(f"Excel creado en: {path}")

            email_service = EmailService()
            await email_service.send_report_email(file_path=path)
            print("¡Proceso terminado!")
        else:
            print("No hay datos para el reporte.")
    
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())