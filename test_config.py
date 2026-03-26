from app.config import settings

print("--- TEST DE CONFIGURACIÓN ---")
print(f"Nombre de la app:   {settings.app_name}")
print(f"Empresa:            {settings.company_name}")
print(f"Email destino:      {settings.contact_email}")
print(f"Tipo de DB:         {settings.db_type}")

print("\n--- VERIFICACIÓN DE SECRETOS (.env) ---")
if settings.POSTGRES_PASSWORD:
    print("Constraseña de Postgres cargada (oculta por seguridad)")
else:
    print("No hay contraseña de Postgres (normal si usamos SQLite)")

print("\n--- RESULTADO ---")
if settings.db_type == "sqlite":
    print("Sistema configurado para: DESARROLLO (SQLite)")
else:
    print("Sistema configurado para PRODUCCIÓN (Postgres)")