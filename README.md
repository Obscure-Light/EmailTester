# Email Tester - SMTP/API con Token

Un'applicazione Python con interfaccia grafica per testare l'invio di email tramite SMTP o API REST con supporto per autenticazione OAuth2.

## Caratteristiche

### 🚀 Funzionalità Principali
- **Invio SMTP**: Supporto completo per SMTP con STARTTLS e SMTPS
- **Invio API**: Integrazione con API REST e autenticazione OAuth2
- **Allegati**: Gestione intelligente degli allegati con validazione dimensioni
- **Formati**: Supporto per email in testo semplice e HTML
- **Validazione**: Controlli di validazione completi prima dell'invio
- **Test Connessione**: Verifica della connettività SMTP

### 🛡️ Sicurezza
- Mascheramento password nell'interfaccia
- Validazione input per prevenire errori
- Gestione sicura delle credenziali API
- Supporto OAuth2 con token temporanei

### 🎨 Interfaccia Utente
- Layout moderno e intuitivo organizzato in sezioni
- Scroll verticale per form lunghi
- Feedback visivo per operazioni e errori
- Gestione allegati con drag & drop virtuale
- Validazione real-time dei campi

## Requisiti di Sistema

- Python 3.7 o superiore
- Tkinter (incluso nella maggior parte delle distribuzioni Python)
- Libreria `requests` per le chiamate API

## Installazione

1. **Clona o scarica i file**:
   ```bash
   git clone <repository-url>
   cd email-tester
   ```

2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvia l'applicazione**:
   ```bash
   python main.py
   ```

## Struttura del Progetto

```
email-tester/
├── main.py              # Punto di ingresso
├── gui.py               # Interfaccia grafica
├── email_service.py     # Logica invio email
├── requirements.txt     # Dipendenze
└── README.md           # Documentazione
```

## Guida all'Uso

### 1. Configurazione Email
- **Mittente**: Inserisci l'indirizzo email mittente
- **Nome Visualizzato**: Nome che apparirà come mittente (opzionale)
- **Destinatari**: Email principale, CC e BCC (separati da virgola)
- **Oggetto e Corpo**: Contenuto del messaggio

### 2. Configurazione Server SMTP

#### Provider Comuni:
- **Gmail**: `smtp.gmail.com:587` (STARTTLS)
- **Outlook**: `smtp-mail.outlook.com:587` (STARTTLS)
- **Yahoo**: `smtp.mail.yahoo.com:587` (STARTTLS)
- **Custom**: Configura server e porta personalizzati

#### Protocolli Supportati:
- **STARTTLS Porta 25**: Per server locali/aziendali
- **STARTTLS Porta 587**: Standard per la maggior parte dei provider
- **SMTPS Porta 465**: Connessione SSL diretta

### 3. Metodi di Autenticazione

#### Nessuna Autenticazione
Per server SMTP aperti (raro, principalmente per test locali).

#### SMTP Username/Password
- Inserisci username e password del tuo account email
- **Nota**: Gmail richiede "Password per le app" invece della password normale

#### API con Token OAuth2
Per servizi che supportano API REST:
1. Inserisci API Key e Secret
2. Abilita "Richiede Token OAuth"
3. Configura URL Token e Send secondo la documentazione del provider

### 4. Gestione Allegati
- **Aggiungi File**: Seleziona uno o più file da allegare
- **Rimuovi**: Elimina allegati selezionati o tutti
- **Validazione**: Controllo automatico dimensioni (limite 25MB per file)
- **Anteprima**: Visualizzazione nome file e dimensioni

### 5. Test e Invio
- **Test Connessione**: Verifica la connettività al server SMTP
- **Invia Email**: Esegue l'invio dopo validazione completa
- **Pulisci Form**: Resetta tutti i campi

## Configurazioni Provider Email

### Gmail
```
Server: smtp.gmail.com
Porta: 587
Protocollo: STARTTLS
Username: tuo-email@gmail.com
Password: password-per-app (non la password normale)
```
**Nota**: Abilita autenticazione a 2 fattori e genera una "Password per le app".

### Outlook/Hotmail
```
Server: smtp-mail.outlook.com
Porta: 587
Protocollo: STARTTLS
Username: tuo-email@outlook.com
Password: password-account
```

### Server Aziendale
```
Server: mail.azienda.com
Porta: 587 o 25
Protocollo: STARTTLS o nessuno
Credenziali: secondo configurazione aziendale
```

## Risoluzione Problemi

### Errori Comuni

#### "Autenticazione fallita"
- Verifica username e password
- Per Gmail: usa Password per le app
- Controlla se l'account richiede autenticazione a 2 fattori

#### "Connessione rifiutata"
- Verifica server SMTP e porta
- Controlla firewall/antivirus
- Prova protocolli diversi (STARTTLS vs SMTPS)

#### "Destinatario rifiutato"
- Verifica correttezza indirizzi email
- Controlla policy del server SMTP
- Il server potrebbe richiedere autenticazione

#### "File allegato troppo grande"
- Limite di 25MB per file singolo
- Comprimi i file o usa servizi cloud per file molto grandi
- Alcuni provider hanno limiti più bassi

### Debug e Log
L'applicazione mostra messaggi dettagliati per ogni operazione:
- ✅ Successo: operazione completata
- ❌ Errore: problema specifico con suggerimenti
- 🔄 In corso: operazione in esecuzione
- ⚠️ Avviso: attenzione richiesta

## Sicurezza e Privacy

### Dati Sensibili
- Le password non vengono salvate o registrate
- I token OAuth2 sono temporanei e non persistenti
- Le credenziali rimangono solo in memoria durante l'esecuzione

### Best Practices
- Non condividere le Password per le app
- Usa account dedicati per test automatici
- Mantieni aggiornate le dipendenze
- Testa sempre con account non produttivi

## Sviluppo e Personalizzazione

### Estendere l'Applicazione
Il codice è strutturato per facilitare estensioni:

- **`email_service.py`**: Aggiungi nuovi provider API
- **`gui.py`**: Modifica l'interfaccia utente
- **`main.py`**: Gestione configurazione globale

### API Personalizzate
Per integrare nuovi provider API, modifica la funzione `invia_email_api()` in `email_service.py` secondo le specifiche del provider.

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Sei libero di utilizzarlo, modificarlo e distribuirlo.

## Supporto

Per problemi o suggerimenti:
1. Controlla la documentazione
2. Verifica i log di errore nell'applicazione
3. Testa con configurazioni semplici prima di quelle complesse

---

**Versione**: 1.0  
**Ultimo Aggiornamento**: 2024