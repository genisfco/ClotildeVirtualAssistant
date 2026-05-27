from gtts import gTTS
from playsound import playsound
playsound('n2.mp3')

def criar_audio(audio):
    tts = gTTS(audio, lang='pt-br')
    tts.save('bem_vindo.mp3')
    playsound('bem_vindo.mp3') # WINDONS
    criar_audio('Oi, eu sou a Denise.')

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