# Email Tester via SMTP/API

Applicazione Python (Tkinter) per testare l'invio di email tramite varie modalità:
- **Nessuna autenticazione** (per server SMTP aperti in locale o reti interne)
- **Autenticazione via SMTP** (username/password)
- **Autenticazione via API** (con eventuale token)

## Funzionalità Principali
1. **Invio di email** a uno o più destinatari (To, Cc, Bcc).
2. **Allegati** multipli selezionabili direttamente dall'interfaccia.
3. **Scelta del formato** del corpo email: testo semplice (plain) o HTML.
4. **Supporto per vari protocolli SMTP**:
   - STARTTLS (porta 25)
   - STARTTLS (porta 587)
   - SMTPS (porta 465)
5. **Test connessione** al server SMTP.
6. **Possibilità di gestire un token API** (esempio: OAuth, custom token, ecc.).

## Struttura del Progetto
- **main.py**  
  Avvia l'interfaccia grafica definita in `gui.py`.

- **gui.py**  
  Contiene l'interfaccia grafica basata su Tkinter; gestisce l'input
  dell'utente (es. destinatari, server, allegati) e invoca la funzione `invia_email`.

- **email_service.py**  
  Incapsula la logica di invio email (SMTP o API). Riceve i parametri
  (mittente, destinatari, server, credenziali) e gestisce la composizione
  del messaggio (inclusi allegati) e l'invio vero e proprio.

- **requirements.txt** (opzionale)  
  Da usare se presenti dipendenze aggiuntive. Tkinter, smtplib e altre
  librerie usate in questo progetto sono tipicamente incluse nella
  distribuzione standard di Python.

## Requisiti
- Python 3.x (consigliato 3.7 o superiore).
- **Tkinter** (incluso nella maggior parte delle installazioni Python
  su Windows, macOS e Linux, ma potresti doverlo installare manualmente
  su alcune distribuzioni Linux).

## Installazione
1. Clona il repository:
   ```bash
   git clone https://github.com/tuo-username/email_tester.git
   cd email_tester
