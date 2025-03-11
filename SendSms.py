from twilio.rest import Client
import datetime
import time

# Tes informations Twilio
account_sid = 'AC5c8683ccee0b6652d57ccf14e4abfd5d'  # Remplace par ton SID Twilio
auth_token = '0d573da1c31a6e0b5516e1cb8a044dbe'  # Remplace par ton Token Twilio

# Créer une instance de client Twilio
client = Client(account_sid, auth_token)

# Ton numéro Twilio WhatsApp
twilio_whatsapp_number = 'whatsapp:+14155238886'  # Exemple, remplace par le numéro Twilio

# Le numéro du destinataire
student_number = 'whatsapp:+2250172426087'  # Remplace par le numéro de l'étudiant

# Lien Google Meet
meet_link = 'https://meet.google.com/abc-defg-hij'  # Remplace par ton lien Meet

# Message à envoyer
def send_whatsapp_message():
    message = client.messages.create(
        body=f"Bonjour ! Voici le lien pour la réunion de ce week-end : {meet_link}",
        from_=twilio_whatsapp_number,
        to=student_number
    )
    print(f"Message envoyé : {message.sid}")

# Planifier l'envoi chaque Samedi et Dimanche à 15h25
def schedule_message():
    while True:
        now = datetime.datetime.now()
        
        # Vérifier si c'est un Samedi ou Dimanche à 15h25
        if (now.weekday() == 5 or now.weekday() == 6) and now.hour == 15 and now.minute == 25:
            send_whatsapp_message()
            # Attendre 60 secondes pour éviter plusieurs envois à la même minute
            time.sleep(60)
        else:
            # Attendre 30 secondes avant de vérifier à nouveau
            time.sleep(30)

# Lancer la fonction de planification
schedule_message()
