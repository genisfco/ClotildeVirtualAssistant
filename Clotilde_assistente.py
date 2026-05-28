import pyttsx3
import speech_recognition as sr
import random
import datetime
import webbrowser as wb
import urllib.request
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import scrolledtext
import threading

# Configurações iniciais de data/hora
hour = datetime.datetime.now().strftime('%H:%M')
date = datetime.date.today().strftime('%d/%B/%Y').split('/')

# Importações dos seus módulos personalizados (mantidos)
from modules import carrega_agenda, comandos_respostas

comandos = comandos_respostas.comandos
respostas = comandos_respostas.respostas

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
meu_nome = 'clotilde'


# --- FUNÇÃO DA NOVA FUNCIONALIDADE: NOTÍCIAS ---
def buscar_noticias():
    try:
        # Mudamos para o feed oficial e estável "Em cima da hora" da Folha de S.Paulo
        url = "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()

            # Se o servidor responder em branco por algum motivo, evitamos o crash
            if not xml_data.strip():
                print("[AVISO]: O servidor retornou uma resposta vazia.")
                return []

            root = ET.fromstring(xml_data)

            noticias = []
            # Procuramos pelas tags <item> dentro do XML
            for item in root.findall('.//item')[:3]:  # Pega as 3 primeiras
                title = item.find('title').text
                if title:
                    noticias.append(title.strip())

            return noticias

    except Exception as e:
        print(f"\n[ERRO DETALHADO NAS NOTÍCIAS]: {e}\n")
        return []


# --- FUNÇÕES CORE DA ASSISTENTE ---
def search(frase):
    wb.get(chrome_path).open('https://www.google.com/search?q=' + frase)


def speak(audio):
    atualizar_status("Falando...")
    engine = pyttsx3.init()
    engine.setProperty('rate', 140)
    engine.setProperty('volume', 1)
    engine.say(audio)
    engine.runAndWait()


def listen_microphone():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.adjust_for_ambient_noise(source, duration=0.7)
        atualizar_status("Ouvindo...")
        try:
            audio = microfone.listen(source, timeout=5, phrase_time_limit=5)
            atualizar_status("Processando voz...")
            frase = microfone.recognize_google(audio, language='pt-BR')
            log_conversa(f"Você: {frase}")
            return frase
        except sr.UnknownValueError:
            log_conversa("Clotilde: Não entendi o que você disse.")
            return ''
        except Exception as e:
            return ''


# --- LOGICA DE PROCESSAMENTO DOS COMANDOS ---
def processar_comandos():
    result = listen_microphone()
    result_lower = result.lower()

    if meu_nome in result_lower:
        # Remove o nome "Clotilde" da frase
        try:
            partes = result_lower.split(meu_nome, 1)
            comando_puro = partes[1].strip() if len(partes) > 1 else ""
        except:
            comando_puro = result_lower

        log_conversa(f"Clotilde: Ativada! Comando: {comando_puro}")

        # 1. Ajuda/Funções
        if any(cmd in comando_puro for cmd in comandos[0]):
            speak('Até agora minhas funções são: ' + respostas[0])

        # 2. Lembrete/Anotação
        elif any(cmd in comando_puro for cmd in comandos[1]):
            speak('Pode falar o que quer anotar!')
            anotacao_texto = listen_microphone()
            if anotacao_texto:
                with open('anotacao.txt', mode='a+', encoding='utf-8') as f:
                    f.write(anotacao_texto + '\n')
                speak('Anotado com sucesso!')

        # 3. Pesquisa no Google
        elif any(cmd in comando_puro for cmd in comandos[2]):
            speak('O que você quer pesquisar?')
            termo_pesquisa = listen_microphone()
            if termo_pesquisa:
                search(termo_pesquisa)

        # 4. Horas
        elif any(cmd in comando_puro for cmd in comandos[3]):
            speak('Agora são ' + datetime.datetime.now().strftime('%H:%M'))

        # 5. Data
        elif any(cmd in comando_puro for cmd in comandos[4]):
            speak('Hoje é dia ' + date[0] + ' de ' + date[1])

        # NOVA FUNCIONALIDADE: Notícias (Assumindo que comandos[5] possa ser usado ou adicionado)
        elif "notícia" in comando_puro or "notícias" in comando_puro:
            speak("Buscando as últimas notícias no G1, aguarde.")
            lista_noticias = buscar_noticias()
            if lista_noticias:
                speak("Aqui estão as três principais manchetes de hoje:")
                for i, noticia in enumerate(lista_noticias, 1):
                    log_conversa(f"Notícia {i}: {noticia}")
                    speak(noticia)
            else:
                speak("Desculpe, não consegui acessar o portal de notícias no momento.")

        # 6. Agenda (Excel)
        elif any(cmd in comando_puro for cmd in comandos[6]):
            agenda = carrega_agenda.carrega_agenda()
            if agenda:
                speak('Estes são os eventos agendados para hoje:')
                for i in range(len(agenda[1])):
                    speak(f"{agenda[1][i]} {agenda[0][i]} agendada para as {str(agenda[2][i])}")
            else:
                speak('Não há eventos agendados para hoje!')

        else:
            speak("Desculpe, não entendi esse comando.")

    atualizar_status("Pronta")


# --- INTERFACE GRÁFICA (TKINTER) ---
def IniciarThread():
    # Executa a assistente em segundo plano para não travar a janela
    threading.Thread(target=processar_comandos, daemon=True).start()


def atualizar_status(texto):
    lbl_status.config(text=f"Status: {texto}")


def log_conversa(texto):
    txt_historico.config(state=tk.NORMAL)
    txt_historico.insert(tk.END, texto + "\n")
    txt_historico.see(tk.END)
    txt_historico.config(state=tk.DISABLED)


# Configuração da Janela Principal
root = tk.Tk()
root.title("Assistente Virtual Clotilde")
root.geometry("450x550")
root.configure(bg="#2c3e50")

# Título
lbl_titulo = tk.Label(root, text="Clotilde", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="#ecf0f1")
lbl_titulo.pack(pady=15)

# Status
lbl_status = tk.Label(root, text="Status: Pronta", font=("Helvetica", 12, "italic"), bg="#2c3e50", fg="#2ecc71")
lbl_status.pack(pady=5)

# Caixa de Histórico de Conversa
txt_historico = scrolledtext.ScrolledText(root, width=50, height=18, font=("Courier New", 10), state=tk.DISABLED,
                                          bg="#34495e", fg="#ecf0f1")
txt_historico.pack(pady=15)

# Botão para Acionar
btn_falar = tk.Button(root, text="Falar com Clotilde", font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="white",
                      width=20, height=2, command=IniciarThread)
btn_falar.pack(pady=10)

log_conversa("[INFO] Sistema inicializado com sucesso!")
root.mainloop()