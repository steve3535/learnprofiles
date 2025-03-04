from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENDGRID_API_KEY

async def send_access_code(email: str, access_code: str):
    """Envoie le code d'accès par email"""
    message = Mail(
        from_email='votre@email.com',
        to_emails=email,
        subject='Votre code d\'accès au questionnaire',
        html_content=f'''
            <h2>Bienvenue sur le questionnaire d'évaluation</h2>
            <p>Voici votre code d'accès : <strong>{access_code}</strong></p>
            <p>Utilisez ce code pour vous connecter et commencer le questionnaire.</p>
        '''
    )
    
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'email: {e}")
        return False 