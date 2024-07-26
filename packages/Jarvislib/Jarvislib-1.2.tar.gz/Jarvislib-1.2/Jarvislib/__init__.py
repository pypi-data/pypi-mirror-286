import time
import pip
pip install simpleaudio
time.sleep(10)
pip install pydub
time.sleep(10)
pip install keyboard
time.sleep(10)
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import speech_recognition as sr
import webbrowser
import datetime
import requests
import tkinter as tk
from tkinter import *
import keyboard
hi = (["Привет","привет","Добрый вечер","Доброе утро","Доброй ночи","Здорово","Здарова","Здравстуй","Здравствуйте","Привет Джарвис","Джарвис Привет","Добрый вечер Джарвис","Доброе утро Джарвис","Доброй ночи Джарвис","Здорово Джарвис","Здарова Джарвис","Здравстуй Джарвис","Здравствуйте Джарвис"])


def pusk():
    global text
    text = "пусто"
    hour = int(datetime.datetime.now().hour)
    slushayu = 'slushayu.wav'
    wave_obj = sa.WaveObject.from_wave_file(slushayu)
    play = wave_obj.play()
    play.wait_done()
    play.stop()
    recording = sd.rec(int(5 * 44100), samplerate=44100, channels=2)
    sd.wait(2)
    write("recording.wav", 44100, recording)
    wv.write("recording.wav", recording, 44100, sampwidth=2)
    r = sr.Recognizer()
    with sr.AudioFile("recording.wav") as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="ru-RU")
        print("Text: "+text)
    except Exception as e:
        print("Exception: "+str(e))



    if hour>=0 and hour<12 and text in hi:
        hi = 'morning.wav'
        wave_obj = sa.WaveObject.from_wave_file(hi)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()

    elif hour>=12 and hour<18 and text in hi:
        hi = 'day.wav'
        wave_obj = sa.WaveObject.from_wave_file(hi)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()

    elif hour>=18 and hour<24 and text in hi:
        hi = 'evening.wav'
        wave_obj = sa.WaveObject.from_wave_file(hi)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pusk()


    elif "погода " in text:
        p = 'open.wav'
        wave_obj = sa.WaveObject.from_wave_file(p)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        pogoda_fact, city = text.split('погода ')
        webbrowser.open_new_tab('https://yandex.ru/pogoda/search?request=' +city)
        root.quit()


    elif "поиск" in text:
        poisk = 'poisk.wav'
        wave_obj = sa.WaveObject.from_wave_file(poisk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        poisk2, poisk = text.split('поиск ')
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' +poisk)
        root.quit()
    elif "Найди" in text:
        poisk = 'poisk.wav'
        wave_obj = sa.WaveObject.from_wave_file(poisk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        poisk_fact, fact_poisk = text.split('найди ')
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' +fact_poisk)
        root.quit()
    elif "найти" in text:
        poisk = 'poisk.wav'
        wave_obj = sa.WaveObject.from_wave_file(poisk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        poisk_fact, fact_poisk = text.split('найти ')
        webbrowser.open_new_tab('https://yandex.ru/search/?text=' +fact_poisk)
        root.quit()


    elif "Включи " in text:
        music_name = 'on.wav'
        wave_obj = sa.WaveObject.from_wave_file(music_name)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        music_fact, fact_music = text.split('Включи ')
        webbrowser.open_new_tab('https://music.yandex.ru/search?text=' + fact_music)
        root.quit()
    elif "Включи песню" in text:
        music = 'on.wav'
        wave_obj = sa.WaveObject.from_wave_file(music)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        music_fact, fact_music = text.split('Включи песню ')
        webbrowser.open_new_tab('https://music.yandex.ru/search?text=' + fact_music)
        root.quit()
    elif "песня" in text:
        music = 'on.wav'
        wave_obj = sa.WaveObject.from_wave_file(music)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        music_fact, fact_music = text.split('песня ')
        webbrowser.open_new_tab('https://music.yandex.ru/search?text=' + fact_music)
        root.quit()


    elif text == "отмена":
        zvuk = 'ponial.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        root.quit()


    elif text == "пока" or keyboard.is_pressed('Ctrl + Q'):
        zvuk = 'godbie.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        root.destroy()


    else:
        zvuk = 'neponial.wav'
        wave_obj = sa.WaveObject.from_wave_file(zvuk)
        play = wave_obj.play()
        play.wait_done()
        play.stop()
        root.quit()
        pusk()


root = Tk()
root.title("J.A.R.V.I.S.")
button = Button(root, text="Запуск", command=pusk)


def okno():
    button.pack()
    root.after(50, auto_click)
    root.mainloop()
def auto_click():
    button.invoke()


def start():
    while True:
    if keyboard.is_pressed('Ctrl + Alt'):
        okno()
        if text == "пока":
            time.sleep(3)
            break
    if keyboard.is_pressed('Ctrl + Q'):
        time.sleep(3)
        break