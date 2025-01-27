import datetime
import customtkinter as ctk
from tkinter import messagebox
import pyautogui
import cv2
import numpy as np
import threading
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BotApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("LOTOGREN V1.0")
        self.geometry("400x660")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="LOTOGREEN", font=("Arial", 20)).pack(pady=(20, 10))

        # Entrada de Email
        self.entry_email = ctk.CTkEntry(self, placeholder_text="Digite seu email", width=200)
        self.entry_email.pack(pady=5)

        # Entrada de Senha
        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*", width=200)
        self.entry_senha.pack(pady=5)

        # Seleção de Fichas
        ctk.CTkLabel(self, text="Selecione a ficha e a quantidade de X").pack(pady=(10, 0))
        self.ficha_values = {
            "Ficha 5": "ficha_5.png",
            "Ficha 10": "ficha_10.png",
            "Ficha 25": "ficha_25.png",
            "Ficha 125": "ficha_125.png",
        }

        self.selected_ficha = ctk.StringVar(value="Ficha 5")
        self.dropdown_ficha = ctk.CTkOptionMenu(self, variable=self.selected_ficha, values=list(self.ficha_values.keys()))
        self.dropdown_ficha.pack(pady=(10, 0))

        # Quantidade de Cliques
        ctk.CTkLabel(self, text="Quantidade de X").pack(pady=(10, 0))
        self.entry_cliques = ctk.CTkEntry(self, placeholder_text="Digite a quantidade")
        self.entry_cliques.pack(pady=(10, 0))

        # Inputs de Stop Win, Stop Loss e Martingale
        ctk.CTkLabel(self, text="Stop Win").pack(pady=(10, 0))
        self.entry_stop_win = ctk.CTkEntry(self, placeholder_text="Digite numero")
        self.entry_stop_win.pack(pady=(5, 0))

        ctk.CTkLabel(self, text="Stop Loss").pack(pady=(10, 0))
        self.entry_stop_loss = ctk.CTkEntry(self, placeholder_text="Digite numero")
        self.entry_stop_loss.pack(pady=(5, 0))

        ctk.CTkLabel(self, text="Martingale").pack(pady=(10, 0))
        self.entry_martingale = ctk.CTkEntry(self, placeholder_text="Digite numero")
        self.entry_martingale.pack(pady=(10, 0))

        self.button_start = ctk.CTkButton(self, text="Iniciar Bot", command=self.start_bot_thread)
        self.button_start.pack(pady=(10, 10))

        self.button_stop = ctk.CTkButton(self, text="Parar Bot", command=self.stop_bot)
        self.button_stop.pack(pady=(10, 10))

        self.label_status = ctk.CTkLabel(self, text="Status: Parado")
        self.label_status.pack(pady=(10, 0))

        self.bot_running = False
        self.vitorias = 0
        self.derrotas = 0

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
            self.label_status.configure(text="Status: Parado")
            self.bot_running = False
            return

        ficha = self.selected_ficha.get()
        quantidade = self.entry_cliques.get()

        if not quantidade.isdigit() or int(quantidade) <= 0:
            messagebox.showerror("Erro", "Por favor, insira uma quantidade válida.")
            self.label_status.configure(text="Status: Parado")
            self.bot_running = False
            return

        quantidade = int(quantidade)

        self.driver = uc.Chrome()
        self.driver.set_window_size(1624, 968)
        self.driver.set_window_position(0, 0) 

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

        self.driver.get("https://web.telegram.org/a/#-1001386141380")

        time.sleep(20)

        self.monitor_telegram()

        self.driver.get("https://lotogreen.com/play/6286")

        time.sleep(3)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[class='ml-3 fill-bzMenuText hover:scale-110 md:block'] svg")
            )
        ).click()

        time.sleep(4)                  

        try:
            for _ in range(quantidade):
                if not self.bot_running:
                    break
                self.clicar_ficha(self.ficha_values[ficha])
                time.sleep(1)

                # Após clicar na ficha, clicar na cor correspondente (vermelho ou azul)
                cor = self.realizar_acao()

                if cor == "vermelho":
                    self.clicar_cor("apostar_vermelho.png")
                elif cor == "azul":
                    self.clicar_cor("apostar_azul.png")
                else:
                    messagebox.showerror("Erro", "Cor inválida.")
                    break
                
                # Esperar pela aparição da cor na tela
                self.verificar_imagem(cor)

            self.label_status.configure(text="Status: Finalizado")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao interagir com a página: {e}")
            self.label_status.configure(text="Status: Parado")

    def stop_bot(self):
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")

    def clicar_ficha(self, imagem_ficha, tolerancia=0.8):
        # Tirar um screenshot da tela
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        # Carregar a imagem da ficha
        ficha = cv2.imread(imagem_ficha, cv2.IMREAD_GRAYSCALE)

        # Encontrar correspondência
        resultado = cv2.matchTemplate(screenshot_gray, ficha, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= tolerancia:
            centro_x = max_loc[0] + ficha.shape[1] // 2
            centro_y = max_loc[1] + ficha.shape[0] // 2

            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()
        else:
            raise Exception("Ficha não encontrada.")

    # def verificar_cor_telegram(self):
        # Aqui você pode obter a cor do Telegram. Exemplo:
        # A cor pode ser lida via código que interage com o Telegram ou outra lógica
        # Por enquanto, apenas retornando um valor fixo
    #   return "vermelho"  # ou "azul", dependendo da cor indicada

    def clicar_cor(self, imagem_cor):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        cor = cv2.imread(imagem_cor, cv2.IMREAD_GRAYSCALE)

        resultado = cv2.matchTemplate(screenshot_gray, cor, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= 0.8:  # Ajuste a tolerância conforme necessário
            centro_x = max_loc[0] + cor.shape[1] // 2
            centro_y = max_loc[1] + cor.shape[0] // 2

            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()
        else:
            raise Exception(f"Imagem {imagem_cor} não encontrada.")

    def verificar_imagem(self, cor, timeout=30):
        imagem = "azul.png" if cor == "azul" else "vermelho.png"
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

            cor_image = cv2.imread(imagem, cv2.IMREAD_GRAYSCALE)
            resultado = cv2.matchTemplate(screenshot_gray, cor_image, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

            if max_val >= 0.8:
                return True

            time.sleep(1)

        raise Exception(f"{imagem} não apareceu na tela dentro do tempo limite.")
    
    def monitor_telegram(self):
        try:
            print("Monitorando mensagens no Telegram...")
            while self.bot_running:
                # Captura todas as mensagens na interface do Telegram
                all_messages = self.driver.find_elements(By.CSS_SELECTOR, "[id^='message-']")
                if not all_messages:
                    print("Nenhuma mensagem encontrada. Aguardando...")
                    time.sleep(5)
                    continue

                # Obtém a última mensagem
                last_message = all_messages[-2]
                message_text = last_message.text.strip()
                print(f"Mensagem capturada: {message_text}")

                # Determina a cor com base no texto da mensagem
                if "azul" in message_text.lower():
                    self.cor_atual = "azul"
                    print(f"Cor detectada: {self.cor_atual}")
                    break  # Sai do loop ao detectar a cor
                elif "vermelho" in message_text.lower():
                    self.cor_atual = "vermelho"
                    print(f"Cor detectada: {self.cor_atual}")
                    break  # Sai do loop ao detectar a cor
                else:
                    print("Mensagem não contém informações de cor. Aguardando...")
                
                time.sleep(1)

        except Exception as e:
            print(f"Erro no monitoramento do Telegram: {e}")
            self.bot_running = False

    def realizar_acao(self):
        # Este método apenas retorna a cor atual capturada pelo `monitor_telegram`
        if not self.cor_atual:
            raise Exception("Nenhuma cor foi capturada do Telegram.")
        return self.cor_atual

if __name__ == "__main__":
    app = BotApp()
    app.mainloop()
