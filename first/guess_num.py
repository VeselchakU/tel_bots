import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Токен бота Telegram
BOT_TOKEN = ''

# Создаём объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Количество попыток дотупных пользователю в игре
ATTEMPTS = 5

# Словарь, хранящий данные пользователя
users = {}

# Функция, возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

# Хэндлер, обрабатывающий команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }


# Хэндлер, обрабатывающий команду "/help"
@dp.message(Command(commands='help'))
async def process_help_comand(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а тебе нужно его угадать\nУ тебя есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?\n'
        f'Просто ответь - да или нет'
    )

# Хэндлер, обрабатывающий команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: '
        f'{users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )

# Хэндлер, обрабатывающий команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Ты вышел из игры. Если захочешь сыграть '
            'снова - напиши об этом'
        )
    else:
        await message.answer(
            'А мы и так с тобой не играем. '
            'Может, сыграем разок?'
        )

# Хэндлер, срабатывающий на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра', 'играть', 'хочу играть', 'yes', 'y', 'ok']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )

# Хэндлер, срабатывающий на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду', 'no', 'n']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захочешь поиграть - просто '
            'напиши об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с тобой играем. Присылай, '
            'пожалуйста, числа от 1 до 100'
        )

# Хэндлер, срабатывающий на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Ты угадал число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у тебя больше не осталось '
                f'попыток. Ты проиграл :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n\nДавай '
                f'сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хочешь сыграть?')

# Хэндлер, срабатывающий на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с тобой играем. '
            'Присылай, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давай '
            'просто сыграем в игру?'
        )


if __name__ == '__main__':
    dp.run_polling(bot)
