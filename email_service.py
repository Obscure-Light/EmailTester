"""
File email_service.py
Contiene la logica per l'invio dell'email, gestione degli allegati e dell'autenticazione.
"""

import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def invia_email(
    sender: str,
    recipient: str,
    cc: str,
    bcc: str,
    subject: str,
    body: str,
    nickname: str,
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    url_token: str,
    url_send: str,
    api_key: str,
    api_secret: str,
    starttls_25: bool,
    starttls_587: bool,
    smtps_465: bool,
    auth_method: str,
    token_required: bool,
    body_format: str,
    attachments: list
):
    """
    Funzione che si occupa di inviare l'email tramite SMTP o API.
    
    :param sender: Indirizzo email del mittente
    :param recipient: Indirizzo email del destinatario principale
    :param cc: Eventuali indirizzi in copia
    :param bcc: Eventuali indirizzi in copia nascosta
    :param subject: Oggetto dell'email
    :param body: Corpo dell'email
    :param nickname: Nickname o nome visualizzato del mittente
    :param smtp_server: Server SMTP
    :param smtp_port: Porta del server SMTP
    :param username: Username per autenticazione SMTP
    :param password: Password per autenticazione SMTP
    :param url_token: URL da cui eventualmente recuperare un token (se richiesto)
    :param url_send: URL per inviare la mail tramite API (se richiesto)
    :param api_key: API Key (client_id)
    :param api_secret: API Secret (client_secret)
    :param starttls_25: Flag per abilitare STARTTLS su porta 25
    :param starttls_587: Flag per abilitare STARTTLS su porta 587
    :param smtps_465: Flag per abilitare SMTP su porta 465
    :param auth_method: Metodo di autenticazione scelto (none, smtp, api)
    :param token_required: Flag che indica se è richiesto un token API
    :param body_format: Formato del corpo dell'email (plain o html)
    :param attachments: Lista di percorsi file da allegare
    :return: Messaggio di stato sull'esito dell'operazione
    """

    # Se l'utente ha selezionato API e non è richiesto il token,
    # allora usiamo l'autenticazione SMTP come fallback.
    if auth_method == "api" and not token_required:
        auth_method = "smtp"

    # In caso di invio via SMTP
    if auth_method == "smtp":
        if not sender or not recipient or not smtp_server or not smtp_port:
            return "Campi obbligatori mancanti (mittente, destinatario, server, porta)."
        try:
            smtp_port = int(smtp_port)
        except ValueError:
            return "La porta deve essere un numero intero."

        # Costruisce il messaggio
        msg = MIMEMultipart()
        msg['From'] = f"{nickname} <{sender}>"
        msg['To'] = recipient
        msg['Cc'] = cc
        msg['Subject'] = subject if subject else "(Nessun oggetto)"
        msg.attach(MIMEText(body, body_format))

        # Aggiunge gli allegati
        for file_path in attachments:
            try:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={file_path.split('/')[-1]}"
                )
                msg.attach(part)
            except Exception as e:
                return f"Errore durante l'allegato {file_path}: {e}"

        # Invio tramite SMTP
        try:
            if smtps_465:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
                server.ehlo()
            else:
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=10)
                server.ehlo()
                if starttls_25 or starttls_587:
                    server.starttls()
                    server.ehlo()

            if username and password:
                server.login(username, password)

            # Aggiunge destinatari Cc e Bcc
            recipients = [recipient] + cc.split(",") + bcc.split(",")
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
            return "Email inviata con successo!"
        except Exception as e:
            return f"Errore: {e}"

    # Se dovessi implementare l'invio via API con token, potresti
    # gestirlo qui, usando ad esempio requests.post(). 
    # In questo esempio, rimane focalizzato sullo scenario SMTP.
    return "Nessuna operazione di invio eseguita."
