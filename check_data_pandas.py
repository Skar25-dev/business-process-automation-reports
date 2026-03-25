import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///./data/business_data.db")

try:
    df = pd.read_sql("SELECT * FROM sales", engine)

    print("--- VISTA PREVIA DE LOS DAOTS ---")
    print(df.head())

    print("\n--- RESUMEN EJECUTIVO ---")
    print(f"Total de registros: {len(df)}")
    print(f"Ingresos totales:   {df['amount'].sum():,.2f}€")
    print(f"Venta promedio:     {df['amount'].mean():,.2f}€")

    print("\n--- VENTAS POR CATEGORÍA ---")
    print(df.groupby('category')['amount'].sum())

except Exception as e:
    print(f"Error al leer la base de datos: {e}")