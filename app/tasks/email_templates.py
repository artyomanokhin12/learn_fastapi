from email.message import EmailMessage
from app.config import load_config
from pydantic import EmailStr

config = load_config()

def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = config.smtp_service.user
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}.
        """,
        subtype="html"
    )

    return email