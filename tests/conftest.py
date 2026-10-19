from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import settings
from app.database import Base
from app.models import Inventory, Sale
from app.utils import excel_generator, pdf_generator


@pytest.fixture
def db_session():
    """Base de datos SQLite en memoria con datos conocidos y deterministas."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    now = datetime.now()
    session.add_all(
        [
            Sale(product_name="Lámpara", category="Hogar", amount=150.0,
                 customer_name="Ana", date=now - timedelta(days=2)),
            Sale(product_name="Sofá", category="Hogar", amount=400.0,
                 customer_name="Luis", date=now - timedelta(days=5)),
            Sale(product_name="Pan", category="Alimentos", amount=130.0,
                 customer_name="Eva", date=now - timedelta(days=1)),
            # Venta antigua: debe quedar fuera del filtro por defecto de 30 días
            Sale(product_name="Televisor", category="Electrónica", amount=499.0,
                 customer_name="Pablo", date=now - timedelta(days=40)),
            Inventory(product_name="Lámpara", category="Hogar", stock_quantity=10,
                      min_stock_level=5, unit_cost=20.0,
                      last_restock_date=now - timedelta(days=3)),
            Inventory(product_name="Pan", category="Alimentos", stock_quantity=50,
                      min_stock_level=10, unit_cost=1.5,
                      last_restock_date=now - timedelta(days=1)),
        ]
    )
    session.commit()

    yield session

    session.close()
    engine.dispose()


@pytest.fixture(autouse=True)
def reports_dir(tmp_path, monkeypatch):
    """Los reportes generados en los tests van a una carpeta temporal."""
    monkeypatch.setattr(excel_generator, "REPORTS_DIR", tmp_path)
    monkeypatch.setattr(pdf_generator, "REPORTS_DIR", tmp_path)
    return tmp_path


@pytest.fixture(autouse=True)
def report_settings(monkeypatch):
    """Configuración fija, independiente de config/settings.json."""
    monkeypatch.setattr(settings, "report_format", "xlsx")
    monkeypatch.setattr(
        settings,
        "report_settings",
        {
            "default_days": 30,
            "included_columns": ["product_name", "category", "amount", "date"],
            "sheet_name": "Reporte de Ventas",
        },
    )
