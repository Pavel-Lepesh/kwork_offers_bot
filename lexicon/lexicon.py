import json
from itertools import chain

with open('kwork_categories.json', encoding='utf-8') as file:
    LEXICON_CATEGORIES = json.load(file)


HIGH_CATEGORIES = [cat for cat in LEXICON_CATEGORIES.keys()]
MID_CATEGORIES = list(chain(*[cat.keys() for cat in LEXICON_CATEGORIES.values()]))
LOW_CATEGORIES = list(chain(*chain(*[cat.values() for cat in LEXICON_CATEGORIES.values()])))


LEXICON_COMMANDS = {'/start': 'Приветствие',
                    '/beginning': 'Запуск',
                    '/cancel': 'Остановка работы',
                    '/help': 'Справка по работе бота'}


LEXICON_RU = {'start': 'Привет! Давай уже начнем поиск заказов для тебя!\n\n'
                       'Для запуска работы бота используйте команду /beginning\n'
                       'Для получения справочной информации используйте команду /help',
              'help': 'Здесь пока ничего нет.',
              'none': 'У меня нет полномочий обрабатывать такие команды😵‍💫',
              'cancel': 'Завершаю работу.'}
