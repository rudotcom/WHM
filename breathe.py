import sys
import time
import pymorphy2
import pyglet
import pyttsx3
import threading
import warnings

warnings.filterwarnings("ignore")

""" Количество раундов, вдохов в раунде, задержка дыхания на вдохе"""
rounds, breaths, hold = 4, 30, 15


def play_wav(src):
    wav = pyglet.media.load(sys.path[0] + '\\src\\wav\\' + src + '.wav')
    wav.play()
    time.sleep(wav.duration)


def play_wav_inline(src):
    wav = pyglet.media.load(sys.path[0] + '\\src\\wav\\' + src + '.wav')
    wav.play()


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
    speech_voice = 3  # голосовой движок
    rate = 120
    tts = pyttsx3.init()
    voices = tts.getProperty("voices")
    tts.setProperty('rate', rate)
    tts.setProperty("voice", voices[speech_voice].id)
    print('🔊', what)
    tts.say(what)
    tts.runAndWait()
    # tts.stop()


class Workout:

    def __init__(self, rounds=3, breaths=30, hold=15):
        self.rounds = rounds
        self.breaths = breaths
        self.hold = hold
        self.round_times = []
        self.lock = threading.Lock()  # взаимоблокировка отдельных голосовых потоков

    def __str__(self):
        return '\n♻{} 🗣{} ⏱{}'.format(self.rounds, self.breaths, self.hold)

    def __hold_breath(self):
        start_time = time.time()
        input()
        seconds = int(time.time() - start_time)
        mins = seconds // 60
        secs = seconds % 60
        self.round_times.append('{:02}:{:02}'.format(mins, secs))
        play_wav_inline('inhale')
        self.say('Глубокий вдох. ' + nums("{} минута {} секунда".format(mins, secs)))

    def __clock_tick(self):
        for i in range(self.hold):
            # self.say(hold - i)
            play_wav('clock')

    def __breathe_round(self, round):
        self.say('Раунд ' + str(round))
        for i in range(self.breaths):
            if i % 10 == 0:
                play_wav_inline('gong')
            print(i + 1, end=' ')
            play_wav('inhale')
            play_wav('exhale')
        print()
        self.say('Задерживаем дыхание на выдохе')
        self.__hold_breath()
        # self.say('Держим ' + nums(str(self.hold) + ' секунда'))
        self.__clock_tick()
        play_wav_inline('exhale')
        self.say('Выдох')
        time.sleep(1)

    def breathe(self):
        self.say('Выполняем ' + nums(str(self.rounds) + ' раунд по ' + str(self.breaths) + ' глубокий вдох и ' +
                                     str(self.breaths) + ' спокойный выдох'))
        self.say('Приготовились. Начали')
        for i in range(self.rounds):
            self.__breathe_round(i + 1)
        self.say('Восстанавливаем дыхание. Начинаем шевелиться с пальцев рук и ног')

    def statistics(self):
        print('=============')
        for i in range(len(self.round_times)):
            print('Раунд', i, self.round_times[i])
        print('=============')

    def say(self, what):
        self.lock.acquire()
        thread = threading.Thread(target=speak, kwargs={'what': what})
        thread.start()
        thread.join()
        self.lock.release()


workout = Workout(rounds, breaths, hold)
workout.breathe()

workout.statistics()
