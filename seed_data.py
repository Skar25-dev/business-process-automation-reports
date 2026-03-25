from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Sale
from faker import Faker
from faker_commerce import Provider as CommerceProvider
import random

Base.metadata.create_all(bind=engine)

fake = Faker()
fake.add_provider(CommerceProvider)

db = SessionLocal()

def seed_data(n=100):
    categories = ['Electrónica', 'Ropa', 'Hogar', 'Alimentos']

    for _ in range(n):
        new_sale = Sale(
            product_name=fake.ecommerce_name(),
            category=random.choice(categories),
            amount=round(random.uniform(10.0, 500.0), 2),
            customer_name=fake.name(),
            date=fake.date_time_between(start_date='-30d', end_date='now')
        )
        db.add(new_sale)
    
    db.commit()
    print(f"Se han insertado {n} registros con nombres de productos reales.")

if __name__ == "__main__":
    seed_data(50)