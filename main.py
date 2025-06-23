"""
File main.py
Punto di ingresso dell'applicazione. Inizializza e avvia la GUI con gestione errori.
"""

import sys
import tkinter as tk
from tkinter import messagebox
import traceback

def main():
    """Funzione principale che avvia l'applicazione con gestione errori."""
    try:
        # Importa la GUI solo quando necessario
        from gui import avvia_gui
        
        # Configura gestione errori globale per Tkinter
        def handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            print(f"Errore non gestito: {error_msg}")
            
            # Mostra messaggio di errore all'utente se possibile
            try:
                root = tk.Tk()
                root.withdraw()  # Nascondi la finestra principale
                messagebox.showerror(
                    "Errore Applicazione",
                    f"Si è verificato un errore imprevisto:\n\n{exc_value}\n\n"
                    "L'applicazione verrà chiusa. Controlla la console per maggiori dettagli."
                )
                root.destroy()
            except:
                pass
        
        sys.excepthook = handle_exception
        
        # Avvia l'interfaccia grafica
        avvia_gui()
        
    except ImportError as e:
        print(f"Errore durante l'importazione dei moduli: {e}")
        print("Assicurati che tutti i file necessari siano presenti nella stessa directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Errore durante l'avvio dell'applicazione: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()