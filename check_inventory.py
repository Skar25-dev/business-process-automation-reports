import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos
engine = create_engine("sqlite:///./data/business_data.db")

try:
    # 1. Realizamos la consulta SQL directamente al inventario
    df = pd.read_sql("SELECT * FROM inventory", engine)

    if df.empty:
        print("⚠️ La tabla de inventario está vacía.")
    else:
        print("\n--- 📦 LISTADO COMPLETO DE INVENTARIO ---")
        # Mostramos todas las filas (o las primeras 20 si es muy grande)
        print(df.to_string(index=False)) 

        print("\n--- 📊 RESUMEN DE STOCK ---")
        print(f"Total de productos únicos: {len(df)}")
        print(f"Cantidad total de artículos en almacén: {df['stock_quantity'].sum()}")
        
        # Mostrar productos bajo mínimos (Alerta de Stock)
        bajo_minimos = df[df['stock_quantity'] < df['min_stock_level']]
        if not bajo_minimos.empty:
            print("\n🚨 ALERTA: PRODUCTOS BAJO MÍNIMOS:")
            print(bajo_minimos[['product_name', 'stock_quantity', 'min_stock_level']])

except Exception as e:
    print(f"❌ Error al consultar la base de datos: {e}")