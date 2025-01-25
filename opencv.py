import datetime
import customtkinter as ctk
from tkinter import messagebox
import pyautogui
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        self.geometry("400x550")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="LOTOGREEN").pack(pady=(10, 0))

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Digite seu email", width=200)
        self.entry_email.pack(pady=5)

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*", width=200)
        self.entry_senha.pack(pady=5)

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
        self.bot_running = True
        self.label_status.configure(text="Status: Rodando")

        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showerror("Erro", "Por favor, preencha o email e a senha.")
            self.bot_running = False
            return

        self.driver = uc.Chrome()
        self.driver.set_window_size(1624, 968)  # Exemplo de tamanho fixo
        self.driver.set_window_position(0, 0) 

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
            email_field.send_keys(email)

            time.sleep(2)

            # Campo de senha
            senha_field = WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Senha']"))
            )

            senha_field.send_keys(senha)

            time.sleep(2)

            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#legitimuz-action-send-analisys")
                )
            ).click()

            time.sleep(2)

            self.driver.get("https://lotogreen.com/play/6286")

            time.sleep(5)

            while self.bot_running:
                        
                try:
                    ficha = self.selected_ficha.get()
                    cliques = self.entry_cliques.get()

                    if not ficha or not cliques.isdigit():
                        messagebox.showerror("Erro", "Selecione uma ficha e informe uma quantidade válida de cliques.")
                        return
                    
                    time.sleep(2)

                    self.driver.get("https://web.telegram.org/a/#-1001386141380")

                    time.sleep(20)

                    self.monitor_telegram()

                    self.driver.get("https://lotogreen.com/play/6286")

                    time.sleep(2)

                    WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "button[class='ml-3 fill-bzMenuText hover:scale-110 md:block'] svg")
                        )
                    ).click()

                    time.sleep(1)

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
                    print(f"Erro ao executar o loop de cliques: {e}")
                    messagebox.showerror("Erro", f"Erro ao executar o loop de cliques: {e}")
                    self.label_status.configure(text="Status: Erro")
                    self.bot_running = False

        except Exception as e:
            print(f"Erro ao interagir com a página: {e}")
            messagebox.showerror("Erro", f"Erro ao interagir com a página: {e}")
            self.label_status.configure(text="Status: Erro")
            self.bot_running = False

    def stop_bot(self):
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")

    def clicar_imagem(self, imagem_ficha, tolerancia=0.8):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
        imagem = cv2.imread(imagem_ficha, cv2.IMREAD_GRAYSCALE)

        resultado = cv2.matchTemplate(screenshot_gray, imagem, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= tolerancia:
            centro_x = max_loc[0] + imagem.shape[1] // 2
            centro_y = max_loc[1] + imagem.shape[0] // 2
            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()

    def clicar_ficha(self, imagem_ficha, tolerancia=0.8):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
        ficha = cv2.imread(imagem_ficha, cv2.IMREAD_GRAYSCALE)

        resultado = cv2.matchTemplate(screenshot_gray, ficha, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= tolerancia:
            centro_x = max_loc[0] + ficha.shape[1] // 2
            centro_y = max_loc[1] + ficha.shape[0] // 2
            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()

        # Redireciona para o Telegram
        self.driver.execute_script("window.open('https://web.telegram.org/', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        # Inicia o monitoramento no Telegram em uma thread
        self.telegram_thread = threading.Thread(target=self.monitor_telegram)
        self.telegram_thread.start()

    def monitor_telegram(self):
        try:
            print("Monitorando mensagens no Telegram...")
            while self.bot_running:
                # Captura todas as mensagens da tela
                all_messages = self.driver.find_elements(By.CSS_SELECTOR, "[id^='message-']")
                if not all_messages:
                    print("Nenhuma mensagem encontrada. Aguardando...")
                    time.sleep(5)
                    continue

                # Obtém a última mensagem
                last_message = all_messages[-2]
                message_text = last_message.text.strip()
                print(f"Mensagem capturada: {message_text}")

                # Tenta capturar o horário da mensagem
                try:
                    post_time_element = last_message.find_element(By.CSS_SELECTOR, "[class*='time']")
                    post_time = post_time_element.text.strip()
                except Exception as e:
                    print("Horário não encontrado na mensagem. Ignorando...")
                    time.sleep(2)
                    continue

                # Captura o horário atual do sistema
                current_time = datetime.datetime.now().strftime("%H:%M")

                # Verifica se o horário do post coincide com o horário atual
                if post_time == current_time:
                    print(f"[{current_time}] Nova mensagem detectada: {message_text}")
                    self.realizar_acao(message_text)
                    print("Saindo do monitoramento...")
                    break  # Sai do loop após processar a mensagem
                else:
                    print(f"Aguardando nova mensagem no horário atual: {current_time}")
                    time.sleep(2)  # Aguarda antes de verificar novamente

        except Exception as e:
            print(f"Erro no monitoramento do Telegram: {e}")
            self.bot_running = False

    def realizar_acao(self, message_text):
        if "vermelho" in message_text.lower():
            print("Ação: Apostar no VERMELHO")
            self.clicar_postar_vermelho()
        elif "azul" in message_text.lower():
            print("Ação: Apostar no AZUL")
            self.clicar_postar_azul()
        else:
            print("Nenhuma ação necessária.")

    def clicar_postar_azul(self):
        self.clicar_imagem("postar_azul.png")

    def clicar_postar_vermelho(self):
        self.clicar_imagem("postar_vermelho.png")

    def stop_bot(self):
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")
        if hasattr(self, "driver"):
            self.driver.quit()
        print("Bot parado.")


if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
