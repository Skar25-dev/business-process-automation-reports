from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Sale, Inventory
from faker import Faker
from faker_commerce import Provider as CommerceProvider
import random

Base.metadata.create_all(bind=engine)
fake = Faker()
fake.add_provider(CommerceProvider)
db = SessionLocal()

def seed_data(num_productos=20, num_ventas=50):
    categories = ['Electrónica', 'Ropa', 'Hogar', 'Alimentos']
    
    # 1. Limpiar datos previos
    db.query(Sale).delete()
    db.query(Inventory).delete()

    # 2. Crear un catálogo de productos únicos en el Inventario
    productos_creados = []
    print(f"📦 Generando {num_productos} productos únicos en inventario...")
    
    for _ in range(num_productos):
        p_name = fake.unique.ecommerce_name() # .unique asegura que no se repita
        p_cat = random.choice(categories)
        
        item_inv = Inventory(
            product_name=p_name,
            category=p_cat,
            stock_quantity=random.randint(5, 100),
            min_stock_level=random.randint(5, 15),
            unit_cost=round(random.uniform(10.0, 100.0), 2),
            last_restock_date=fake.date_time_between(start_date='-30d', end_date='now')
        )
        db.add(item_inv)
        productos_creados.append({"name": p_name, "cat": p_cat})

    db.commit() # Guardamos los productos primero

    # 3. Crear ventas aleatorias usando SOLO los productos del inventario
    print(f"💰 Generando {num_ventas} ventas aleatorias...")
    for _ in range(num_ventas):
        # Elegimos un producto al azar de los que acabamos de crear
        prod = random.choice(productos_creados)
        
        nueva_venta = Sale(
            product_name=prod["name"],
            category=prod["cat"],
            amount=round(random.uniform(120.0, 500.0), 2),
            customer_name=fake.name(),
            date=fake.date_time_between(start_date='-15d', end_date='now')
        )
        db.add(nueva_venta)
    
    db.commit()
    print(f"✅ ¡Hecho! {num_productos} productos en almacén y {num_ventas} ventas registradas.")

if __name__ == "__main__":
    seed_data()