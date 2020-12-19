import pytils
import pymorphy2
morph=pymorphy2.MorphAnalyzer()


def correct_numerals(phrase, morph=pymorphy2.MorphAnalyzer()):
    new_phrase = []
    phrase = phrase.split(' ')
    while phrase:
        word = phrase.pop(-1)
        if 'NUMB' in morph.parse(word)[0].tag:
            new_phrase.append(pytils.numeral.sum_string(int(word), py_gen))
        else:
            new_phrase.append(word)
        py_gen = pytils.numeral.FEMALE if 'femn' in morph.parse(word)[0].tag else pytils.numeral.MALE
    return ' '.join(new_phrase[::-1])


def nums(phrase, morph=pymorphy2.MorphAnalyzer()):
    """ согласование существительных с числительными, стоящими перед ними """
    phrase = phrase.replace('  ', ' ').replace(',', ' ,')
    numeral = ''
    new_phrase = []
    for word in phrase.split(' '):
        if 'NUMB' in morph.parse(word)[0].tag:
            numeral = word
        if numeral:
            word = str(morph.parse(word)[0].make_agree_with_number(abs(int(numeral))).word)
        new_phrase.append(word)

    return ' '.join(new_phrase).replace(' ,', ',')


mins, secs = 0, 0
print(correct_numerals(nums("Вдох. {} минута {} секунда".format(mins, secs))))
