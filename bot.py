import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils import formatting
from aiogram.utils.formatting import Text, Bold
from config import cfg

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
# Для записей с типом Secret* необходимо
# вызывать метод get_secret_value(),
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=cfg.bot_token.get_secret_value(),
          default=DefaultBotProperties(parse_mode=ParseMode.HTML)
          )

# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!")


# Хэндлер на команду /test1
@dp.message(F.text, Command("test1"))
async def cmd_test1(message: Message):
    await message.reply("<b>Test 1</b>", parse_mode=ParseMode.HTML)


# Хэндлер на команду /test2
async def cmd_test2(message: Message):
    await message.reply("<u>Test 2</u>")


# Запуск процесса поллинга новых апдейтов
async def main():
    # Регистрация хендлера на команду /test2:
    dp.message.register(cmd_test2, Command("test2"))

    await dp.start_polling(bot)


@dp.message(Command("hello"))
async def cmd_hello(message: Message):
    # await message.answer(
    #     f"Hello, <b>{message.from_user.full_name}</b>",
    #     parse_mode=ParseMode.HTML
    # )
    content = Text(
        "Hello, ",
        Bold(message.from_user.full_name),
        ",\nid = ",
        Bold(message.from_user.id),
        ",\nusername = ",
        formatting.Underline(message.from_user.username)
    )
    print(content.as_kwargs())
    await message.answer(**content.as_kwargs()
    )

if __name__ == "__main__":
    asyncio.run(main())
