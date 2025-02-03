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
        self.corner_radius = 50

        ctk.CTkLabel(self, text="LOTOGREEN", font=("Arial", 20)).pack(pady=(20, 10))

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Digite seu email", width=200)
        self.entry_email.pack(pady=5)

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Digite sua senha", show="*", width=200)
        self.entry_senha.pack(pady=5)

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

        self.entry_cliques = ctk.CTkEntry(self, placeholder_text="Quantidade de X da fichas")
        self.entry_cliques.pack(pady=(10, 0))

        ctk.CTkLabel(self, text="Selecione a fichas de empate").pack(pady=(10, 0))
        self.ficha_empate_values = {
            "Ficha 5": "ficha_5.png",
            "Ficha 10": "ficha_10.png",
            "Ficha 25": "ficha_25.png",
            "Ficha 125": "ficha_125.png",
        }
        self.selected_ficha_empate = ctk.StringVar(value="Ficha 5")
        self.dropdown_ficha_empate = ctk.CTkOptionMenu(self, variable=self.selected_ficha_empate, values=list(self.ficha_empate_values.keys()))
        self.dropdown_ficha_empate.pack(pady=(10, 0))

        ctk.CTkLabel(self, text="Stop Win").pack(pady=(10, 0))
        self.entry_stop_win = ctk.CTkEntry(self, placeholder_text="Digite numero")
        self.entry_stop_win.pack(pady=(5, 0))

        ctk.CTkLabel(self, text="Stop Loss").pack(pady=(10, 0))
        self.entry_stop_loss = ctk.CTkEntry(self, placeholder_text="Digite numero")
        self.entry_stop_loss.pack(pady=(5, 0))

        ctk.CTkLabel(self, text="Martingale").pack(pady=(10, 0))
        self.entry_martingale = ctk.CTkEntry(self, placeholder_text="Digite numero")
        self.entry_martingale.pack(pady=(5, 0))

        self.button_start = ctk.CTkButton(self, text="Iniciar Bot", command=self.start_bot_thread)
        self.button_start.pack(pady=(20, 5))

        self.button_stop = ctk.CTkButton(self, text="Parar Bot", command=self.stop_bot)
        self.button_stop.pack(pady=(5, 5))

        self.label_status = ctk.CTkLabel(self, text="Status: Parado")
        self.label_status.pack(pady=(10, 0))

        self.bot_running = False
        self.vitorias = 0
        self.derrotas = 0

    def start_bot_thread(self):
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
        ficha_empate = self.selected_ficha_empate.get()
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

        try:
            martingale_limit = int(self.entry_martingale.get())  # Máximo de Martingales
            stop_win = int(self.entry_stop_win.get())  # Limite de ganhos
            stop_loss = int(self.entry_stop_loss.get())  # Limite de perdas
            martingale_count = 0  # Contador de tentativas
            wins = 0  # Contador de vitórias

            while martingale_count <= martingale_limit and wins < stop_win:
                if not self.bot_running:
                    break  # Sai do loop se o bot for interrompido

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

                # Clica na ficha novamente a cada tentativa de Martingale
                for _ in range(martingale_count + 1):
                    self.clicar_ficha(self.ficha_values[self.selected_ficha.get()])
                    time.sleep(1)

                cor = self.realizar_acao()  # Obtém a cor detectada

                if cor == "vermelho":
                    self.clicar_cor("apostar_vermelho.png")
                elif cor == "azul":
                    self.clicar_cor("apostar_azul.png")
                else:
                    messagebox.showerror("Erro", "Cor inválida.")
                    break

                self.clicar_ficha_empate(self.ficha_empate_values[self.selected_ficha_empate.get()])
                self.clicar_empate("empate.png")  

                resultado = self.verificar_imagem(cor)  # Verifica o resultado

                if resultado:  
                    wins += 1  # Aumenta a contagem de vitórias
                    if wins >= stop_win:
                        messagebox.showinfo("Parabéns!", "Stop Win atingido. O bot será encerrado.")
                        break  # Sai do loop se atingir o Stop Win
                else:
                    martingale_count += 1  # Aumenta a contagem de Martingale

                    if martingale_count >= stop_loss:
                        messagebox.showwarning("Aviso", "Stop Loss atingido. O bot será encerrado.")
                        break  # Sai do loop se atingir o Stop Loss

            self.label_status.configure(text="Status: Finalizado")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao interagir com a página: {e}")
            self.label_status.configure(text="Status: Parado")

    def stop_bot(self):
        self.bot_running = False
        self.label_status.configure(text="Status: Parado")

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
        else:
            raise Exception("Ficha não encontrada.")

    def clicar_ficha_empate(self, imagem_ficha_empate, tolerancia=0.8):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        ficha = cv2.imread(imagem_ficha_empate, cv2.IMREAD_GRAYSCALE)

        resultado = cv2.matchTemplate(screenshot_gray, ficha, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= tolerancia:
            centro_x = max_loc[0] + ficha.shape[1] // 2
            centro_y = max_loc[1] + ficha.shape[0] // 2
            
            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()
        else:
            raise Exception("Ficha não encontrada.")

    def clicar_cor(self, imagem_cor):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        cor = cv2.imread(imagem_cor, cv2.IMREAD_GRAYSCALE)

        resultado = cv2.matchTemplate(screenshot_gray, cor, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= 0.8:
            centro_x = max_loc[0] + cor.shape[1] // 2
            centro_y = max_loc[1] + cor.shape[0] // 2

            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()
        else:
            raise Exception(f"Imagem {imagem_cor} não encontrada.")

    def clicar_empate(self, imagem_empate):
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

        cor = cv2.imread(imagem_empate, cv2.IMREAD_GRAYSCALE)

        resultado = cv2.matchTemplate(screenshot_gray, cor, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(resultado)

        if max_val >= 0.8:
            centro_x = max_loc[0] + cor.shape[1] // 2
            centro_y = max_loc[1] + cor.shape[0] // 2

            pyautogui.moveTo(centro_x, centro_y, duration=0.3)
            pyautogui.click()
        else:
            raise Exception(f"Imagem {imagem_empate} não encontrada.")

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
