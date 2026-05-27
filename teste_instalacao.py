from pathlib import Path

from gtts import gTTS
from playsound import playsound

def criar_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('bem_vindo.mp3')
    playsound('bem_vindo.mp3') # WINDOWS


def tocar_audio_se_existir(caminho_audio):
    caminho = Path(caminho_audio)
    if caminho.exists():
        playsound(str(caminho))
    else:
        print(f'Aviso: arquivo de áudio não encontrado: {caminho_audio}')

import speech_recognition
print('Speech Recognition: ', speech_recognition.__version__)
import pyttsx3
pyttsx3.speak('Testando a biblioteca')
#import tensorflow
#print('TensorFlow')
import librosa
print('Librosa:', librosa.version)
import matplotlib
print('Matplotlib: ', matplotlib._get_version())
import seaborn
print('Seaborn: ')
import pyaudio
print('Pyaudio ok!')

if __name__ == '__main__':
    tocar_audio_se_existir('n2.mp3')
    criar_audio('Oi, eu sou a Clotilde.')