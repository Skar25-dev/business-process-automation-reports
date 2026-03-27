import pandas as pd
from datetime import datetime
from pathlib import Path

def generate_excel_report(df: pd.DataFrame, report_name: str, sheet_name: str = "Reporte") -> str:
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"{report_name}_{timestamp}.xlsx"
    filepath = output_dir/filename

    with pd.ExcelWriter(filepath, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)

        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except: pass
            worksheet.column_dimensions[column_letter].width = max_length + 2
    
    return str(filepath)
