import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from app.core.config import settings

logger = logging.getLogger(__name__)


def send_email(
    email_to: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
) -> bool:
    """
    Send an email using SMTP.
    """
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.EMAIL_FROM
        message["To"] = email_to

        # Add text content if provided
        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)

        # Add HTML content
        part2 = MIMEText(html_content, "html")
        message.attach(part2)

        # Connect to SMTP server
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, email_to, message.as_string())
        
        logger.info(f"Email sent successfully to {email_to}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {email_to}: {str(e)}")
        return False


def send_registration_email(email_to: str, token: str) -> bool:
    """
    Send registration verification email with token.
    """
    subject = "Vérifiez votre adresse email - Plateforme d'Évaluation du Profil d'Apprentissage"
    
    # Create verification link (this should be your frontend URL)
    verification_link = f"http://localhost:3000/verify?token={token}"
    
    html_content = f"""
    <html>
    <body>
        <h2>Bienvenue sur la Plateforme d'Évaluation du Profil d'Apprentissage</h2>
        <p>Merci de vous être inscrit(e). Pour compléter votre inscription, veuillez cliquer sur le lien ci-dessous :</p>
        <p><a href="{verification_link}">Vérifier mon adresse email</a></p>
        <p>Ou copiez ce jeton d'accès et utilisez-le sur la page de vérification :</p>
        <p><strong>{token}</strong></p>
        <p>Ce lien est valable pendant {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes.</p>
        <p>Si vous n'avez pas demandé cette inscription, veuillez ignorer cet email.</p>
    </body>
    </html>
    """
    
    text_content = f"""
    Bienvenue sur la Plateforme d'Évaluation du Profil d'Apprentissage

    Merci de vous être inscrit(e). Pour compléter votre inscription, veuillez utiliser le jeton d'accès suivant :

    {token}

    Ce jeton est valable pendant {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes.

    Si vous n'avez pas demandé cette inscription, veuillez ignorer cet email.
    """
    
    return send_email(
        email_to=email_to,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    ) 