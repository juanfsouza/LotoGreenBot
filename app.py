import customtkinter as ctk
from tkinter import messagebox
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class BotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login do Bot")
        self.geometry("300x250")
        self.resizable(False, False)

        # Elementos da GUI
        self.label_email = ctk.CTkLabel(self, text="Email:")
        self.label_email.pack(pady=(10, 0))

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Digite seu email", width=200)
        self.entry_email.pack(pady=5)

        self.label_senha = ctk.CTkLabel(self, text="Senha:")
        self.label_senha.pack(pady=(10, 0))

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*", width=200)
        self.entry_senha.pack(pady=5)

        self.button_next = ctk.CTkButton(self, text="Próximo", width=200, command=self.open_main_window)
        self.button_next.pack(pady=(20, 5))

    def open_main_window(self):
        self.destroy()

        # Nova janela
        main_window = ctk.CTk()
        main_window.title("Configurações do Bot")
        main_window.geometry("400x500")
        main_window.resizable(False, False)

        self.bot_running = False

        ctk.CTkLabel(main_window, text="Valor da aposta").pack(pady=(10, 0))
        self.entry_bet_value = ctk.CTkEntry(main_window, placeholder_text="Valor da aposta")
        self.entry_bet_value.pack(pady=(10, 0))

        ctk.CTkLabel(main_window, text="Stop Loss").pack(pady=(10, 0))
        self.entry_stop_loss = ctk.CTkEntry(main_window, placeholder_text="Stop Loss")
        self.entry_stop_loss.pack(pady=(10, 0))

        self.label_status = ctk.CTkLabel(main_window, text="Status: Parado")
        self.label_status.pack(pady=(10, 0))

        self.button_start = ctk.CTkButton(
            main_window,
            text="Iniciar Bot",
            command=self.start_bot,
            width=200
        )
        self.button_start.pack(pady=(10, 10))

        self.button_stop = ctk.CTkButton(
            main_window,
            text="Parar Bot",
            command=self.stop_bot,
            width=200
        )
        self.button_stop.pack(pady=(10, 10))

        main_window.mainloop()

    def start_bot(self):
        self.bot_running = True
        self.label_status.configure(text="Status: Rodando")

        # Inicializa o WebDriver
        self.driver = uc.Chrome()
        self.driver.get("https://web.telegram.org/")

        time.sleep(20)

        try:
            while self.bot_running:
                # Busca mensagens no grupo
                all_messages = self.driver.find_elements(By.CSS_SELECTOR, "[id^='message-']")
                last_messages = all_messages[-5:]  # Últimos 5 elementos

                for message in last_messages:
                    message_text = message.text.lower()  # Texto da mensagem em minúsculas
                    if "vermelho" in message_text:
                        print(f"Ação: Apostar no VERMELHO - Mensagem: {message_text}")
                    elif "azul" in message_text:
                        print(f"Ação: Apostar no AZUL - Mensagem: {message_text}")

                time.sleep(2)  # Espera antes de verificar novamente

        except Exception as e:
            print(f"Erro durante a execução: {e}")

    def stop_bot(self):
        """Para o bot e fecha o navegador."""
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")
        if hasattr(self, 'driver'):
            self.driver.quit()


if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
