from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import json

class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "database"

    MAIL_PASSWORD: str = ""

    app_name: str = "BPA Reports System"
    company_name: str = "Daniel Sánchez"
    db_type: str = "sqlite" # este valor puede ser 'sqlite' o 'postgresql'
    contact_email: str = "alusan9143@ieselcaminas.org"

    report_settings: dict = {
        "default_days": 30,
        "included_columns": ["product_name", "category", "amount", "date"],
        "sheet_name": "Reporte de Ventas"
    }

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    mail_username: str = ""
    mail_password: str = ""
    mail_from: str = ""
    mail_port: int = 587
    mail_server: str = ""
    mail_starttls: bool = True
    mail_ssl_tls: bool = False
    
def load_settings():
    settings = Settings()

    json_path = Path("config/settings.json")
    if json_path.exists():
        with open(json_path, "r") as f:
            config_data = json.load(f)
            for key, value in config_data.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)
    
    return settings

settings = load_settings()