"""
File gui.py
Contiene la definizione dell'interfaccia grafica (Tkinter) e la logica di controllo
per raccogliere i dati e invocare la funzione di invio email.
"""

import tkinter as tk
from tkinter import ttk, filedialog

from email_service import invia_email

# Variabili globali
attachments = []
body_format = None

def avvia_gui():
    root = tk.Tk()
    root.title("Tester Invio Email via SMTP/API - Opzione Token per API")
    root.geometry("800x600")
    root.resizable(True, True)

    # Variabili controllate da Tk
    var_token_required = tk.BooleanVar(value=False)
    var_starttls_25 = tk.BooleanVar(value=False)
    var_starttls_587 = tk.BooleanVar(value=False)
    var_smtps_465 = tk.BooleanVar(value=False)
    var_auth_method = tk.StringVar(value="none")
    global body_format
    body_format = tk.StringVar(value="plain")

    # Funzioni per la GUI
    def update_port_and_mode():
        """Aggiorna la porta e la modalità in base alla selezione dell'utente."""
        starttls_25 = var_starttls_25.get()
        starttls_587 = var_starttls_587.get()
        smtps_465 = var_smtps_465.get()

        if starttls_25:
            var_starttls_587.set(False)
            var_smtps_465.set(False)
            entry_port.config(state="normal")
            entry_port.delete(0, tk.END)
            entry_port.insert(0, "25")
            entry_port.config(state="disabled")
        elif starttls_587:
            var_starttls_25.set(False)
            var_smtps_465.set(False)
            entry_port.config(state="normal")
            entry_port.delete(0, tk.END)
            entry_port.insert(0, "587")
            entry_port.config(state="disabled")
        elif smtps_465:
            var_starttls_25.set(False)
            var_starttls_587.set(False)
            entry_port.config(state="normal")
            entry_port.delete(0, tk.END)
            entry_port.insert(0, "465")
            entry_port.config(state="disabled")
        else:
            entry_port.config(state="normal")
            entry_port.delete(0, tk.END)

    def on_auth_method_change():
        """Modifica lo stato dei campi in base al metodo di autenticazione selezionato."""
        auth_method = var_auth_method.get()
        token_required = var_token_required.get()

        if auth_method == "none":
            entry_username.config(state="disabled")
            entry_password.config(state="disabled")
            entry_url_token.config(state="disabled")
            entry_url_send.config(state="disabled")
            entry_api_key.config(state="disabled")
            entry_api_secret.config(state="disabled")
            check_token_req.config(state="disabled")

        elif auth_method == "smtp":
            entry_username.config(state="normal")
            entry_password.config(state="normal")
            entry_url_token.config(state="disabled")
            entry_url_send.config(state="disabled")
            entry_api_key.config(state="disabled")
            entry_api_secret.config(state="disabled")
            check_token_req.config(state="disabled")

        elif auth_method == "api":
            entry_username.config(state="disabled")
            entry_password.config(state="disabled")
            entry_api_key.config(state="normal")
            entry_api_secret.config(state="normal")
            check_token_req.config(state="normal")

            if token_required:
                entry_url_token.config(state="normal")
                entry_url_send.config(state="normal")
            else:
                entry_url_token.config(state="disabled")
                entry_url_send.config(state="disabled")

    def attach_file():
        """Permette all'utente di selezionare e allegare un file."""
        file_path = filedialog.askopenfilename()
        if file_path:
            attachments.append(file_path)
            lbl_attachments.config(text=f"Allegati: {', '.join(attachments)}")

    def remove_attachments():
        """Rimuove tutti gli allegati."""
        attachments.clear()
        lbl_attachments.config(text="Allegati: Nessuno")

    def test_connection():
        """Testa la connessione al server SMTP."""
        smtp_server = entry_smtp_server.get().strip()
        smtp_port = entry_port.get().strip()
        try:
            with smtplib.SMTP(smtp_server, int(smtp_port), timeout=10) as server:
                server.ehlo()
            lbl_result.config(text="Connessione al server SMTP riuscita!", foreground="green")
        except Exception as e:
            lbl_result.config(text=f"Errore di connessione: {e}", foreground="red")

    def send_email():
        """Invoca la funzione di invio email con i dati raccolti dalla GUI."""
        sender = entry_from.get().strip()
        recipient = entry_to.get().strip()
        cc = entry_cc.get().strip()
        bcc = entry_bcc.get().strip()
        subject = entry_subject.get().strip()
        body = text_body.get("1.0", tk.END).strip()
        nickname = entry_nickname.get().strip()
        smtp_server = entry_smtp_server.get().strip()
        smtp_port = entry_port.get().strip()
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        url_token = entry_url_token.get().strip()
        url_send = entry_url_send.get().strip()
        api_key = entry_api_key.get().strip()
        api_secret = entry_api_secret.get().strip()
        token_required = var_token_required.get()

        starttls_25 = var_starttls_25.get()
        starttls_587 = var_starttls_587.get()
        smtps_465 = var_smtps_465.get()

        auth_method = var_auth_method.get()

        # Chiamata alla funzione di invio
        risultato = invia_email(
            sender=sender,
            recipient=recipient,
            cc=cc,
            bcc=bcc,
            subject=subject,
            body=body,
            nickname=nickname,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            username=username,
            password=password,
            url_token=url_token,
            url_send=url_send,
            api_key=api_key,
            api_secret=api_secret,
            starttls_25=starttls_25,
            starttls_587=starttls_587,
            smtps_465=smtps_465,
            auth_method=auth_method,
            token_required=token_required,
            body_format=body_format.get(),
            attachments=attachments
        )

        lbl_result.config(text=risultato, foreground="green" if "successo" in risultato else "red")

    # Creazione del layout scorrevole
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    main_frame = ttk.Frame(scrollable_frame, padding="10")
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Sezione campi email
    ttk.Label(main_frame, text="Mittente (From):").grid(row=0, column=0, sticky="e")
    entry_from = ttk.Entry(main_frame, width=30)
    entry_from.grid(row=0, column=1, pady=5)

    ttk.Label(main_frame, text="Nickname (opzionale):").grid(row=1, column=0, sticky="e")
    entry_nickname = ttk.Entry(main_frame, width=30)
    entry_nickname.grid(row=1, column=1, pady=5)

    ttk.Label(main_frame, text="Destinatario (To):").grid(row=2, column=0, sticky="e")
    entry_to = ttk.Entry(main_frame, width=30)
    entry_to.grid(row=2, column=1, pady=5)

    ttk.Label(main_frame, text="Cc:").grid(row=3, column=0, sticky="e")
    entry_cc = ttk.Entry(main_frame, width=30)
    entry_cc.grid(row=3, column=1, pady=5)

    ttk.Label(main_frame, text="Bcc:").grid(row=4, column=0, sticky="e")
    entry_bcc = ttk.Entry(main_frame, width=30)
    entry_bcc.grid(row=4, column=1, pady=5)

    ttk.Label(main_frame, text="Oggetto (Subject):").grid(row=5, column=0, sticky="e")
    entry_subject = ttk.Entry(main_frame, width=30)
    entry_subject.grid(row=5, column=1, pady=5)

    # Scelta formato corpo email
    ttk.Label(main_frame, text="Formato Corpo:").grid(row=6, column=0, sticky="e")
    radio_plain = ttk.Radiobutton(main_frame, text="Testo", value="plain", variable=body_format)
    radio_plain.grid(row=6, column=1, sticky="w")
    radio_html = ttk.Radiobutton(main_frame, text="HTML", value="html", variable=body_format)
    radio_html.grid(row=7, column=1, sticky="w")

    # Corpo email (Text widget)
    ttk.Label(main_frame, text="Corpo (Body):").grid(row=8, column=0, sticky="ne")
    text_body = tk.Text(main_frame, width=40, height=10)
    text_body.grid(row=8, column=1, pady=5)

    # Sezione server
    ttk.Label(main_frame, text="Server SMTP:").grid(row=9, column=0, sticky="e")
    entry_smtp_server = ttk.Entry(main_frame, width=30)
    entry_smtp_server.grid(row=9, column=1, pady=5)

    ttk.Label(main_frame, text="Porta:").grid(row=10, column=0, sticky="e")
    entry_port = ttk.Entry(main_frame, width=30)
    entry_port.grid(row=10, column=1, pady=5)

    # Check di protocollo
    check_starttls_25 = ttk.Checkbutton(
        main_frame, text="Usa STARTTLS (porta 25)",
        variable=var_starttls_25, command=update_port_and_mode
    )
    check_starttls_25.grid(row=11, column=0, columnspan=2, sticky="w", pady=5)

    check_starttls_587 = ttk.Checkbutton(
        main_frame, text="Usa STARTTLS (porta 587)",
        variable=var_starttls_587, command=update_port_and_mode
    )
    check_starttls_587.grid(row=12, column=0, columnspan=2, sticky="w", pady=5)

    check_smtps_465 = ttk.Checkbutton(
        main_frame, text="Usa SMTPS (porta 465)",
        variable=var_smtps_465, command=update_port_and_mode
    )
    check_smtps_465.grid(row=13, column=0, columnspan=2, sticky="w", pady=5)

    # Metodo di autenticazione
    ttk.Label(main_frame, text="Metodo Autenticazione:").grid(row=14, column=0, sticky="e")
    radio_none = ttk.Radiobutton(
        main_frame, text="Nessuna", variable=var_auth_method, value="none",
        command=on_auth_method_change
    )
    radio_none.grid(row=14, column=1, sticky="w")

    radio_smtp = ttk.Radiobutton(
        main_frame, text="Username/Password via SMTP", variable=var_auth_method, value="smtp",
        command=on_auth_method_change
    )
    radio_smtp.grid(row=15, column=1, sticky="w")

    radio_api = ttk.Radiobutton(
        main_frame, text="API Token", variable=var_auth_method, value="api",
        command=on_auth_method_change
    )
    radio_api.grid(row=16, column=1, sticky="w")

    # Credenziali
    ttk.Label(main_frame, text="Username:").grid(row=17, column=0, sticky="e")
    entry_username = ttk.Entry(main_frame, width=30)
    entry_username.grid(row=17, column=1, pady=5)

    ttk.Label(main_frame, text="Password:").grid(row=18, column=0, sticky="e")
    entry_password = ttk.Entry(main_frame, width=30, show="*")
    entry_password.grid(row=18, column=1, pady=5)

    ttk.Label(main_frame, text="URL Token:").grid(row=19, column=0, sticky="e")
    entry_url_token = ttk.Entry(main_frame, width=30)
    entry_url_token.grid(row=19, column=1, pady=5)

    ttk.Label(main_frame, text="URL Send:").grid(row=20, column=0, sticky="e")
    entry_url_send = ttk.Entry(main_frame, width=30)
    entry_url_send.grid(row=20, column=1, pady=5)

    ttk.Label(main_frame, text="API Key (client_id):").grid(row=21, column=0, sticky="e")
    entry_api_key = ttk.Entry(main_frame, width=30)
    entry_api_key.grid(row=21, column=1, pady=5)

    ttk.Label(main_frame, text="API Secret (client_secret):").grid(row=22, column=0, sticky="e")
    entry_api_secret = ttk.Entry(main_frame, width=30, show="*")
    entry_api_secret.grid(row=22, column=1, pady=5)

    check_token_req = ttk.Checkbutton(
        main_frame, text="Richiede Token", variable=var_token_required,
        command=on_auth_method_change
    )
    check_token_req.grid(row=23, column=0, columnspan=2, sticky="w", pady=5)

    # Gestione allegati
    btn_attach = ttk.Button(main_frame, text="Allega File", command=attach_file)
    btn_attach.grid(row=24, column=0, columnspan=2, pady=5)

    btn_remove_attachments = ttk.Button(main_frame, text="Rimuovi Allegati", command=remove_attachments)
    btn_remove_attachments.grid(row=25, column=0, columnspan=2, pady=5)

    lbl_attachments = ttk.Label(main_frame, text="Allegati: Nessuno", foreground="blue")
    lbl_attachments.grid(row=26, column=0, columnspan=2, pady=5)

    # Test connessione SMTP
    btn_test_connection = ttk.Button(main_frame, text="Test Connessione", command=test_connection)
    btn_test_connection.grid(row=27, column=0, columnspan=2, pady=5)

    # Invio email
    btn_send = ttk.Button(main_frame, text="Invia", command=send_email)
    btn_send.grid(row=28, column=0, columnspan=2, pady=10)

    lbl_result = ttk.Label(main_frame, text="", foreground="blue")
    lbl_result.grid(row=29, column=0, columnspan=2, pady=5)

    # Inizializzazione
    on_auth_method_change()

    root.mainloop()
