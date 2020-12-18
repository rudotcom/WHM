import sys
import time
import pymorphy2
import pyglet
import pyttsx3
import threading
import warnings
warnings.filterwarnings("ignore")

speech_voice = 3  # голосовой движок
rate = 120
tts = pyttsx3.init()
voices = tts.getProperty("voices")
tts.setProperty('rate', rate)
tts.setProperty("voice", voices[speech_voice].id)
# lock = threading.Lock()  # взаимоблокировка отдельных голосовых потоков


def nums(what, morph=pymorphy2.MorphAnalyzer()):
    """ согласование существительных с числительными, стоящими перед ними """
    what = what.replace('  ', ' ').replace(',', ' ,')
    phrase = what.split(' ')
    for i in range(1, len(phrase)):
        if 'NUMB' in morph.parse(phrase[i - 1])[0].tag:
            phrase[i] = str(morph.parse(phrase[i])[0].make_agree_with_number(abs(int(phrase[i - 1]))).word)
        if 'NUMB' in morph.parse(phrase[i - 2])[0].tag:
            phrase[i] = str(morph.parse(phrase[i])[0].make_agree_with_number(abs(int(phrase[i - 2]))).word)
    return ' '.join(phrase).replace(' ,', ',')


def speak(what):
    print('🔊 ', what)
    tts.say(what)
    tts.runAndWait()
    # tts.stop()


def say(what):
    # lock.acquire()
    thread1 = threading.Thread(target=speak, kwargs={'what': what})
    thread1.start()
    # thread1.join()
    # lock.release()


def play_wav(src):
    wav = pyglet.media.load(sys.path[0] + '\\src\\wav\\' + src + '.wav')
    wav.play()
    time.sleep(wav.duration)


def play_wav_inline(src):
    wav = pyglet.media.load(sys.path[0] + '\\src\\wav\\' + src + '.wav')
    wav.play()


def breathe(number):
    for i in range(number):
        print('Вдох', str(i + 1))
        play_wav('inhale')
        play_wav('exhale')


def stopwatch(seconds: int):
    min = seconds // 60
    sec = seconds % 60
    return '{:02}:{:02}'.format(min, sec)


def clock_tick(hold):
    for i in range(hold):
        play_wav('clock')


def breathing(rounds=3, breaths=30, hold=15):
    speak(nums('Выполняем ' + str(rounds) + ' раунд дыхания'))
    speak('В каждом раунде ' + nums(str(breaths) + ' глубокий вдох и ' + str(breaths) + ' спокойный выдох'))
    for i in range(rounds):
        play_wav_inline('reinsamba__gong')
        speak('Раунд ' + str(i + 1))
        breathe(breaths)
        speak('Задержали дыхание на выдохе')
        start_time = time.time()
        input()
        print(stopwatch(int(time.time() - start_time)))
        play_wav_inline('inhale')
        speak('Глубокий вдох.\nЗадерживаем дыхание на ' + nums(str(hold) + ' секунда'))
        clock_tick(hold)
        play_wav_inline('exhale')
        speak('Выдохнули')
        time.sleep(1)


print('\n♻4 🗣30 ⏱12')
rounds, breaths, hold = 4, 2, 12
breathing(rounds, breaths, hold)
speak('Теперь отдыхаем, восстанавливаем дыхание')
