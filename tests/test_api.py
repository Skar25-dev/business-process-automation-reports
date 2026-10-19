import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture
def client(reports_dir, monkeypatch):
    monkeypatch.setattr(main, "REPORTS_DIR", reports_dir)
    # Sin "with": no se ejecuta el lifespan (no arranca el scheduler ni toca la BD)
    return TestClient(main.app)


def test_dashboard_lists_generated_reports(client, reports_dir):
    (reports_dir / "Reporte_ventas_20260101_0800.xlsx").write_bytes(b"x")
    (reports_dir / "notas.txt").write_text("no es un reporte")

    response = client.get("/")

    assert response.status_code == 200
    assert "Reporte_ventas_20260101_0800.xlsx" in response.text
    assert "notas.txt" not in response.text


def test_download_existing_report(client, reports_dir):
    (reports_dir / "Reporte_ventas.xlsx").write_bytes(b"contenido")

    response = client.get("/download/Reporte_ventas.xlsx")

    assert response.status_code == 200
    assert response.content == b"contenido"


def test_download_missing_report_returns_404(client):
    assert client.get("/download/no_existe.xlsx").status_code == 404
