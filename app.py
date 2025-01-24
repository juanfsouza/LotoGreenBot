import customtkinter as ctk
from tkinter import messagebox
import pyautogui
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import customtkinter as ctk
from tkinter import messagebox
import pyautogui
import cv2
import numpy as np
import threading
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
        self.email = self.entry_email.get()
        self.senha = self.entry_senha.get()

        if not self.email or not self.senha:
            messagebox.showerror("Erro", "Por favor, preencha o email e a senha.")
            return

        self.destroy()

        # Nova janela
        main_window = ctk.CTk()
        main_window.title("Configurações do Bot")
        main_window.geometry("400x500")
        main_window.resizable(False, False)

        self.bot_running = False

        # Campo Stop Loss com seleção múltipla
        ctk.CTkLabel(main_window, text="LOTOGREEN").pack(pady=(10, 0))
        
        # Elementos da GUI
        ctk.CTkLabel(self, text="Selecione a ficha e a quantidade de cliques").pack(pady=(10, 0))

        self.ficha_values = {
            "Ficha 5": "ficha_5.png",
            "Ficha 10": "ficha_10.png",
            "Ficha 25": "ficha_25.png",
            "Ficha 125": "ficha_125.png",
        }

        self.selected_ficha = ctk.StringVar(value="Ficha 5")
        self.dropdown_ficha = ctk.CTkOptionMenu(self, variable=self.selected_ficha, values=list(self.ficha_values.keys()))
        self.dropdown_ficha.pack(pady=(10, 0))

        ctk.CTkLabel(self, text="Quantidade de cliques:").pack(pady=(10, 0))
        self.entry_cliques = ctk.CTkEntry(self, placeholder_text="Digite a quantidade")
        self.entry_cliques.pack(pady=(10, 0))

        self.button_start = ctk.CTkButton(self, text="Iniciar Bot", command=self.start_bot_thread)
        self.button_start.pack(pady=(20, 10))

        self.button_stop = ctk.CTkButton(self, text="Parar Bot", command=self.stop_bot)
        self.button_stop.pack(pady=(10, 10))

        self.label_status = ctk.CTkLabel(self, text="Status: Parado")
        self.label_status.pack(pady=(10, 0))

        self.bot_running = False

    def start_bot_thread(self):
        # Iniciar o bot em uma nova thread
        threading.Thread(target=self.start_bot, daemon=True).start()

    def start_bot(self):
        try:
            # Verificar entrada
            ficha = self.selected_ficha.get()
            cliques = self.entry_cliques.get()

            if not ficha or not cliques.isdigit():
                messagebox.showerror("Erro", "Selecione uma ficha e informe uma quantidade válida de cliques.")
                return

            cliques = int(cliques)
            imagem_ficha = self.ficha_values[ficha]

            self.bot_running = True
            self.label_status.configure(text="Status: Rodando")

            for _ in range(cliques):
                if not self.bot_running:
                    break
                self.clicar_ficha(imagem_ficha)

            self.label_status.configure(text="Status: Finalizado")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar o bot: {e}")

    def stop_bot(self):
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")

    def clicar_ficha(self, imagem_ficha, tolerancia=0.8):
        """
        Localiza e clica na ficha selecionada.

        :param imagem_ficha: Caminho para a imagem de referência da ficha.
        :param tolerancia: Similaridade mínima para considerar a correspondência.
        """
        # Tirar um screenshot da tela
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Carregar a imagem da ficha e convertê-la para escala de cinza
        ficha = cv2.imread(imagem_ficha, cv2.IMREAD_GRAYSCALE)

        # Encontrar correspondência entre a ficha e a tela
        resultado = cv2.matchTemplate(screenshot_gray, ficha, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(resultado)

        # Verificar se a correspondência é aceitável
        if max_val >= tolerancia:
            # Coordenadas da posição encontrada
            ficha_posicao = max_loc
            centro_x = ficha_posicao[0] + ficha.shape[1] // 2
            centro_y = ficha_posicao[1] + ficha.shape[0] // 2

            # Clicar na posição
            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()
            print(f"{imagem_ficha} clicada em: ({centro_x}, {centro_y})")
        else:
            print(f"{imagem_ficha} não encontrada. Verifique a imagem ou o layout da página.")

    def start_bot(self):
        self.bot_running = True
        self.label_status.configure(text="Status: Rodando")

        self.driver = uc.Chrome()

        self.driver.set_window_size(1624, 968)  # Exemplo de tamanho fixo
        self.driver.set_window_position(0, 0) 

        selected_values = []
        for value, var in self.checkboxes:
            if var.get():
                quantity = self.stop_loss_values[value].get()
                if not quantity.isdigit():
                    messagebox.showerror("Erro", f"Quantidade inválida para o valor {value}.")
                    return
                selected_values.append(f"{quantity}x de {value} fichas")

        if not selected_values:
            messagebox.showerror("Erro", "Por favor, selecione ao menos um valor de Stop Loss.")
            return

        stop_loss_summary = ", ".join(selected_values)
        messagebox.showinfo("Configurações de Stop Loss", f"Valores selecionados: {stop_loss_summary}")
        self.label_status.configure(text="Status: Rodando")
        # Aqui você pode iniciar a lógica do bot
        print(f"Stop Loss configurado: {stop_loss_summary}") 

        try:

            # Acessa o site do cassino
            self.driver.get("https://lotogreen.com/play/6286")
            time.sleep(5)

            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > button:nth-child(2)")
                )
            ).click()

            time.sleep(2)

            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "body > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(3)")
                )
            ).click()

            time.sleep(2)

            email_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Email ou CPF']"))
            )
            email_field.send_keys(self.email)

            time.sleep(2)

            # Campo de senha
            senha_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Senha']"))
            )

            senha_field.send_keys(self.senha)

            time.sleep(2)

            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#legitimuz-action-send-analisys")
                )
            ).click()

            time.sleep(2)

            self.driver.get("https://lotogreen.com/play/6286")
        
        except Exception as e:
            print(f"Erro ao interagir com a página: {e}")
            messagebox.showerror("Erro", f"Erro ao interagir com a página: {e}")
            self.label_status.configure(text="Status: Erro")
            self.bot_running = False

        # Redireciona para o Telegram
        self.driver.execute_script("window.open('https://web.telegram.org/', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Inicia o monitoramento no Telegram em uma thread
        self.telegram_thread = threading.Thread(target=self.monitor_telegram)
        self.telegram_thread.start()

    def monitor_telegram(self):
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
                time.sleep(1)
        except Exception as e:
            print(f"Erro no monitoramento do Telegram: {e}")

    def stop_bot(self):
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")
        if hasattr(self, "driver"):
            self.driver.quit()
        print("Bot parado.")


if __name__ == "__main__":
    app = BotApp()
    app.mainloop()