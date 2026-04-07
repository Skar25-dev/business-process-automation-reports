import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Sale, Inventory
from app.utils.excel_generator import generate_excel_report
from app.config import settings

REPORT_MODELS = {
    "ventas": Sale,
    "inventario": Inventory
}

def get_columns_for_model(report_type: str):
    model = REPORT_MODELS.get(report_type)
    
    if not model:
        return []
    
    return [column.key for column in model.__table__.columns if column.key != "id"]

class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def get_report(self, report_type: str = "ventas", category: str = None, days: int = None):
        model = REPORT_MODELS.get(report_type)
        
        if not model:
            raise ValueError(f"El tipo de reporte '{report_type}' no existe.")

        if days is None:
            days = settings.report_settings.get("default_days", 30)

        query = self.db.query(model)
        
        if category and category != "Todas":
            query = query.filter(model.category == category)
        
        if days:
            date_limit = datetime.now() - timedelta(days=days)

            if hasattr(model, 'date'):
                query = query.filter(model.date >= date_limit)
            elif hasattr(model, 'last_restock_date'):
                query = query.filter(model.last_restock_date >= date_limit)

        df = pd.read_sql(query.statement, self.db.bind)
        
        if df.empty: return None

        columns_to_include = settings.report_settings.get("included_columns")
        if columns_to_include:
            df = df[[col for col in columns_to_include if col in df.columns]]

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M')

        sheet = settings.report_settings.get("sheet_name", "Reporte")
        return generate_excel_report(df, f"Reporte_{report_type}", sheet_name=sheet)