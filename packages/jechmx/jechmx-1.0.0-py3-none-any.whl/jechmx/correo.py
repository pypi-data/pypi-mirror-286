import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Correo:
    """
    envio de correo electronico
    """

    def __init__(self, correo, mensaje):
        self.correo = correo
        self.mensaje = mensaje

    def enviar_correo(self):
        mensaje = MIMEMultipart()
        mensaje["to"] = self.correo
        mensaje["from"] = "Jechmx"
        mensaje["subject"] = "Notificaciones Jechmx"
        cuerpo = MIMEText(self.mensaje)
        mensaje.attach(cuerpo)
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(user="funerariaelremanso@gmail.com",
                       password="qgriwfyckcxyucla")
            smtp.send_message(mensaje)


mensaje = MIMEMultipart()
mensaje["from"] = "Notificaciones JECHMX"
mensaje["to"] = "jechmx"
