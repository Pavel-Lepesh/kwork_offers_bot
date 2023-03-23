import json
from itertools import chain

with open('kwork_categories.json', encoding='utf-8') as file:
    LEXICON_CATEGORIES = json.load(file)


HIGH_CATEGORIES = [cat for cat in LEXICON_CATEGORIES.keys()]
MID_CATEGORIES = list(chain(*[cat.keys() for cat in LEXICON_CATEGORIES.values()]))  # используется для проверки в хэндлере
LOW_CATEGORIES = list(chain(*chain(*[cat.values() for cat in LEXICON_CATEGORIES.values()])))  # используется для проверки в хэндлере


LEXICON_COMMANDS = {'/start': 'Приветствие',
                    '/beginning': 'Запуск',
                    '/cancel': 'Остановка работы',
                    '/help': 'Справка по работе бота'}


LEXICON_RU = {'start': 'Давай уже начнем поиск заказов для вас! 🧑‍💻\n\n'
                       'Для запуска работы бота используйте команду /beginning 💰\n\n'
                       'Для получения справочной информации используйте команду /help ❓',
              'help': 'Все очень просто! 😄\n'
                      'Вы можете выбрать любую из представленных категорий '
                      'после ввода команды /beginning\n'
                      'Спустя некоторое время бот начнет присылать вам предложения по заказам 🤩\n\n'
                      'Если вы захотите остановить работу бота, используйте команду /cansel ❌\n\n'
                      'Удачи на просторах фриланса! 🌟',
              'none': 'У меня нет полномочий обрабатывать такие команды 😵‍💫',
              'cancel': 'Завершаю работу.',
              'start_process': 'Класс 👍\n\n'
                               'Начинаю поиск 🔍',
              'no_results': 'К сожалению, сейчас в этой категории нет заказов 😞\n\n'
                            'Я продолжу искать заказы здесь, пока они не появятся.\n'
                            'Если вы хотите остановить поиск, используйте команду /cancel'
              }
