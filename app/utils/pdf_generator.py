from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from pathlib import Path
import pandas as pd

# Rutas absolutas
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = BASE_DIR / "reports"

def generate_pdf_report(df: pd.DataFrame, report_name: str) -> str:
    REPORTS_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{report_name}_{timestamp}.pdf"
    filepath = REPORTS_DIR / filename

    # Documento en horizontal para que quepan bien las columnas
    doc = SimpleDocTemplate(str(filepath), pagesize=landscape(A4), 
                            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # 1. Título del Reporte
    title_style = styles["Title"]
    title_style.textColor = colors.HexColor("#141b41") # Deep Navy
    elements.append(Paragraph(f"REPORTE: {report_name.replace('_', ' ').upper()}", title_style))
    
    # 2. Fecha de generación
    elements.append(Paragraph(f"Fecha de emisión: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # 3. Preparación de datos (Convertimos TODO a string para evitar errores)
    headers = [str(col).replace('_', ' ').upper() for col in df.columns]
    data_rows = df.values.tolist()
    # Aseguramos que cada celda sea un string
    clean_data = [headers] + [[str(cell) for cell in row] for row in data_rows]

    # 4. Configuración de la Tabla
    t = Table(clean_data, hAlign='LEFT')
    
    style = TableStyle([
        # --- ESTILO DEL ENCABEZADO (Fila 0) ---
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#306bac")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        # --- ESTILO DEL CUERPO (Filas 1 en adelante) ---
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#ffffff")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#1a1f36")),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
        
        # --- LÍNEAS Y CUADRÍCULA ---
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")])
    ])
    
    t.setStyle(style)

    elements.append(t)
    doc.build(elements)
    
    return str(filepath)