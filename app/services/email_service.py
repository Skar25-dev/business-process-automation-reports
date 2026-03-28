from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings
from pathlib import Path

class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_STARTTLS=settings.mail_starttls,
            MAIL_SSL_TLS=settings.mail_ssl_tls,
            USE_CREDENTIALS=True
        )
    
    async def send_report_email(self, file_path: str, recipient: str = None):
        recipient = recipient or settings.contact_email

        message = MessageSchema(
            subject=f"Reporte Automatizado - {settings.company_name}",
            recipients=[recipient],
            body="Hola,\n\nAdjunto a este correo encontrarás el reporte empresarial generado automáticamente por el sistema BPAR.\n\nSaludos.",
            subtype=MessageType.plain,
            attachments=[file_path]
        )

        fm = FastMail(self.conf)
        await fm.send_message(message)
        print(f"Email enviado con éxito a {recipient}")