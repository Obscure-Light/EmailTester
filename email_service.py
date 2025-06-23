"""
File email_service.py
Contiene la logica completa per l'invio dell'email via SMTP e API,
gestione degli allegati, autenticazione e token OAuth.
"""

import smtplib
import requests
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from urllib.parse import urlencode
import base64
from typing import List, Dict, Any

def ottieni_token_oauth(url_token: str, api_key: str, api_secret: str) -> str:
    """
    Ottiene un token OAuth2 utilizzando le credenziali API.
    
    :param url_token: URL per ottenere il token
    :param api_key: API Key (client_id)
    :param api_secret: API Secret (client_secret)
    :return: Token di accesso
    """
    try:
        # Preparazione credenziali per OAuth2 Client Credentials
        credentials = base64.b64encode(f"{api_key}:{api_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "client_credentials",
            "scope": "send_email"  # Scope tipico per invio email
        }
        
        response = requests.post(url_token, headers=headers, data=data, timeout=30)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token", "")
        else:
            raise Exception(f"Errore nell'ottenere il token: {response.status_code} - {response.text}")
            
    except Exception as e:
        raise Exception(f"Errore durante l'autenticazione: {str(e)}")

def invia_email_api(
    url_send: str,
    token: str,
    sender: str,
    recipient: str,
    cc: str,
    bcc: str,
    subject: str,
    body: str,
    nickname: str,
    body_format: str,
    attachments: List[str]
) -> str:
    """
    Invia email utilizzando API REST.
    
    :param url_send: URL dell'API per l'invio
    :param token: Token di accesso
    :param sender: Mittente
    :param recipient: Destinatario
    :param cc: Destinatari in copia
    :param bcc: Destinatari in copia nascosta
    :param subject: Oggetto
    :param body: Corpo del messaggio
    :param nickname: Nome visualizzato
    :param body_format: Formato del corpo (plain/html)
    :param attachments: Lista file allegati
    :return: Messaggio di risultato
    """
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Preparazione destinatari
        recipients = [recipient.strip()]
        if cc:
            recipients.extend([email.strip() for email in cc.split(",") if email.strip()])
        
        bcc_recipients = []
        if bcc:
            bcc_recipients = [email.strip() for email in bcc.split(",") if email.strip()]
        
        # Preparazione allegati
        attachments_data = []
        for file_path in attachments:
            if not os.path.exists(file_path):
                continue
                
            try:
                with open(file_path, "rb") as file:
                    file_content = base64.b64encode(file.read()).decode()
                    attachments_data.append({
                        "filename": os.path.basename(file_path),
                        "content": file_content,
                        "content_type": "application/octet-stream"
                    })
            except Exception as e:
                return f"Errore durante la lettura dell'allegato {file_path}: {str(e)}"
        
        # Payload per l'API
        payload = {
            "from": {
                "email": sender,
                "name": nickname if nickname else sender
            },
            "to": [{"email": email} for email in recipients],
            "subject": subject if subject else "(Nessun oggetto)",
            "content": [
                {
                    "type": f"text/{body_format}",
                    "value": body
                }
            ]
        }
        
        # Aggiunta destinatari BCC se presenti
        if bcc_recipients:
            payload["bcc"] = [{"email": email} for email in bcc_recipients]
        
        # Aggiunta allegati se presenti
        if attachments_data:
            payload["attachments"] = attachments_data
        
        # Invio richiesta
        response = requests.post(url_send, headers=headers, json=payload, timeout=60)
        
        if response.status_code in [200, 201, 202]:
            return "Email inviata con successo tramite API!"
        else:
            error_msg = f"Errore API: {response.status_code}"
            try:
                error_data = response.json()
                if "message" in error_data:
                    error_msg += f" - {error_data['message']}"
                elif "error" in error_data:
                    error_msg += f" - {error_data['error']}"
            except:
                error_msg += f" - {response.text[:200]}"
            
            return error_msg
            
    except requests.exceptions.Timeout:
        return "Errore: Timeout durante l'invio tramite API"
    except requests.exceptions.ConnectionError:
        return "Errore: Impossibile connettersi al server API"
    except Exception as e:
        return f"Errore durante l'invio tramite API: {str(e)}"

def valida_allegati(attachments: List[str]) -> List[str]:
    """
    Valida gli allegati e restituisce solo quelli esistenti.
    
    :param attachments: Lista percorsi file
    :return: Lista file validi con eventuali errori
    """
    file_validi = []
    errori = []
    
    for file_path in attachments:
        if not os.path.exists(file_path):
            errori.append(f"File non trovato: {os.path.basename(file_path)}")
            continue
            
        try:
            size = os.path.getsize(file_path)
            if size > 25 * 1024 * 1024:  # 25 MB limite tipico
                errori.append(f"File troppo grande (>25MB): {os.path.basename(file_path)}")
                continue
                
            file_validi.append(file_path)
        except Exception as e:
            errori.append(f"Errore file {os.path.basename(file_path)}: {str(e)}")
    
    return file_validi, errori

def prepara_messaggio_smtp(
    sender: str,
    recipient: str,
    cc: str,
    bcc: str,
    subject: str,
    body: str,
    nickname: str,
    body_format: str,
    attachments: List[str]
) -> tuple:
    """
    Prepara il messaggio MIME per l'invio SMTP.
    
    :return: (messaggio_mime, lista_destinatari, lista_errori)
    """
    msg = MIMEMultipart()
    
    # Headers del messaggio
    msg['From'] = f"{nickname} <{sender}>" if nickname else sender
    msg['To'] = recipient
    if cc:
        msg['Cc'] = cc
    msg['Subject'] = subject if subject else "(Nessun oggetto)"
    
    # Corpo del messaggio
    msg.attach(MIMEText(body, body_format))
    
    # Preparazione lista destinatari completa
    destinatari = [recipient.strip()]
    if cc:
        destinatari.extend([email.strip() for email in cc.split(",") if email.strip()])
    if bcc:
        destinatari.extend([email.strip() for email in bcc.split(",") if email.strip()])
    
    # Validazione e aggiunta allegati
    allegati_validi, errori_allegati = valida_allegati(attachments)
    
    for file_path in allegati_validi:
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = os.path.basename(file_path)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}"
            )
            msg.attach(part)
            
        except Exception as e:
            errori_allegati.append(f"Errore allegato {os.path.basename(file_path)}: {str(e)}")
    
    return msg, destinatari, errori_allegati

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
    Funzione principale per l'invio email tramite SMTP o API.
    
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
    :param url_token: URL da cui eventualmente recuperare un token
    :param url_send: URL per inviare la mail tramite API
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
    
    # Validazione campi obbligatori
    if not sender or not recipient:
        return "Errore: Mittente e destinatario sono obbligatori"
    
    # Invio tramite API
    if auth_method == "api":
        if not api_key or not api_secret:
            return "Errore: API Key e Secret sono obbligatori per l'autenticazione API"
        
        try:
            if token_required:
                if not url_token or not url_send:
                    return "Errore: URL Token e Send sono obbligatori quando il token è richiesto"
                
                # Ottieni token OAuth
                token = ottieni_token_oauth(url_token, api_key, api_secret)
                if not token:
                    return "Errore: Impossibile ottenere il token di accesso"
                
                # Invia tramite API
                return invia_email_api(
                    url_send, token, sender, recipient, cc, bcc,
                    subject, body, nickname, body_format, attachments
                )
            else:
                return "Errore: Metodo API selezionato ma token non richiesto. Configurare correttamente."
                
        except Exception as e:
            return f"Errore durante l'invio tramite API: {str(e)}"
    
    # Invio tramite SMTP
    if auth_method in ["smtp", "none"]:
        if not smtp_server or not smtp_port:
            return "Errore: Server SMTP e porta sono obbligatori"
        
        try:
            smtp_port = int(smtp_port)
        except ValueError:
            return "Errore: La porta deve essere un numero intero"
        
        if smtp_port < 1 or smtp_port > 65535:
            return "Errore: La porta deve essere compresa tra 1 e 65535"
        
        # Preparazione messaggio
        try:
            msg, destinatari, errori_allegati = prepara_messaggio_smtp(
                sender, recipient, cc, bcc, subject, body, 
                nickname, body_format, attachments
            )
            
            if errori_allegati:
                return f"Errori con gli allegati: {'; '.join(errori_allegati)}"
            
        except Exception as e:
            return f"Errore durante la preparazione del messaggio: {str(e)}"
        
        # Connessione e invio SMTP
        try:
            # Stabilisci connessione
            if smtps_465:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
                server.ehlo()
            else:
                server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
                server.ehlo()
                
                # STARTTLS se richiesto
                if starttls_25 or starttls_587:
                    server.starttls()
                    server.ehlo()
            
            # Autenticazione se richiesta
            if auth_method == "smtp":
                if not username or not password:
                    server.quit()
                    return "Errore: Username e password sono obbligatori per l'autenticazione SMTP"
                
                server.login(username, password)
            
            # Invio del messaggio
            server.sendmail(sender, destinatari, msg.as_string())
            server.quit()
            
            # Messaggio di successo con dettagli
            num_destinatari = len(destinatari)
            num_allegati = len([f for f in attachments if os.path.exists(f)])
            
            dettagli = f"Email inviata con successo a {num_destinatari} destinatario/i"
            if num_allegati > 0:
                dettagli += f" con {num_allegati} allegato/i"
            
            return dettagli
            
        except smtplib.SMTPAuthenticationError:
            return "Errore: Autenticazione fallita. Verificare username e password"
        except smtplib.SMTPRecipientsRefused:
            return "Errore: Uno o più destinatari sono stati rifiutati dal server"
        except smtplib.SMTPSenderRefused:
            return "Errore: Il mittente è stato rifiutato dal server"
        except smtplib.SMTPDataError as e:
            return f"Errore durante l'invio dei dati: {str(e)}"
        except smtplib.SMTPConnectError:
            return f"Errore: Impossibile connettersi al server {smtp_server}:{smtp_port}"
        except smtplib.SMTPServerDisconnected:
            return "Errore: Il server ha chiuso la connessione inaspettatamente"
        except Exception as e:
            return f"Errore SMTP: {str(e)}"
    
    return "Errore: Metodo di autenticazione non riconosciuto"