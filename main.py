import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated, Message

logging.basicConfig(level=logging.INFO)

TOKEN = ""

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.new_chat_members)
async def welcome_handler(message: Message):
    for user in message.new_chat_members:
        chat = message.chat

        logging.info(f"Новый участник {user.full_name} ({user.id}) присоединился к чату {chat.title} ({chat.id})")

        try:
            await bot.ban_chat_member(chat_id=chat.id, user_id=user.id)
            logging.info(f"Пользователь {user.full_name} ({user.id}) забанен в чате {chat.title} ({chat.id})")

            await bot.unban_chat_member(chat_id=chat.id, user_id=user.id)
            logging.info(f"Пользователь {user.full_name} ({user.id}) разбанен в чате {chat.title} ({chat.id})")

        except Exception as e:
            logging.error(f"Ошибка при бане/разбане пользователя {user.full_name} ({user.id}): {e}")


@dp.message(Command("unban"))
async def unban_command_handler(message: Message):
    if not message.chat.type in ["group", "supergroup"]:
        logging.info(f"Команда /unban вызвана вне группы: {message.chat.title} ({message.chat.id})")
        return

    chat_id = message.chat.id

    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
    if chat_member.status != ChatMemberStatus.CREATOR:
        logging.info(f"Пользователь {message.from_user.full_name} ({message.from_user.id}) пытался использовать /unban, но не является владельцем чата {message.chat.title} ({chat_id}).")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        logging.info(f"Использование команды /unban без аргументов от пользователя {message.from_user.full_name} ({message.from_user.id}) в чате {message.chat.title} ({message.chat.id}).")
        return

    target_id_or_username = args[1].strip()

    user_to_unban_id = None
    if target_id_or_username.startswith("@"):
        logging.warning(f"Попытка разбана по юзернейму '{target_id_or_username}'. Для надежного разбана нужен ID пользователя.")
        try:
            user_to_unban_id = int(target_id_or_username.replace("@", ""))
        except ValueError:
            logging.error(f"Неверный формат ID/юзернейма для разбана: '{target_id_or_username}'. Используйте числовой ID или @username, если бот уже взаимодействовал с этим пользователем.")
            return

    else:
        try:
            user_to_unban_id = int(target_id_or_username)
        except ValueError:
            logging.error(f"Неверный формат ID/юзернейма для разбана: '{target_id_or_username}'. Используйте числовой ID.")
            return

    if user_to_unban_id:
        try:
            await bot.unban_chat_member(chat_id=chat_id, user_id=user_to_unban_id)
            logging.info(f"Пользователь с ID {user_to_unban_id} разбанен в чате {message.chat.title} ({chat_id}).")
        except Exception as e:
            logging.error(f"Ошибка при разбане пользователя с ID {user_to_unban_id} в чате {message.chat.title} ({chat_id}): {e}")


@dp.message(Command("ban"))
async def ban_command_handler(message: Message):
    if not message.chat.type in ["group", "supergroup"]:
        logging.info(f"Команда /ban вызвана вне группы: {message.chat.title} ({message.chat.id})")
        return

    chat_id = message.chat.id

    chat_member = await bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
    if chat_member.status != ChatMemberStatus.CREATOR:
        logging.info(f"Пользователь {message.from_user.full_name} ({message.from_user.id}) пытался использовать /ban, но не является владельцем чата {message.chat.title} ({chat_id}).")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        logging.info(f"Использование команды /ban без аргументов от пользователя {message.from_user.full_name} ({message.from_user.id}) в чате {message.chat.title} ({message.chat.id}).")
        return

    target_id_or_username = args[1].strip()

    user_to_ban_id = None
    if target_id_or_username.startswith("@"):
        logging.warning(f"Попытка бана по юзернейму '{target_id_or_username}'. Для надежного бана нужен ID пользователя.")
        try:
            user_to_ban_id = int(target_id_or_username.replace("@", ""))
        except ValueError:
            logging.error(f"Неверный формат ID/юзернейма для бана: '{target_id_or_username}'. Используйте числовой ID или @username, если бот уже взаимодействовал с этим пользователем.")
            return

    else:
        try:
            user_to_ban_id = int(target_id_or_username)
        except ValueError:
            logging.error(f"Неверный формат ID/юзернейма для бана: '{target_id_or_username}'. Используйте числовой ID.")
            return

    if user_to_ban_id:
        try:
            await bot.ban_chat_member(chat_id=chat_id, user_id=user_to_ban_id)
            logging.info(f"Пользователь с ID {user_to_ban_id} забанен в чате {message.chat.title} ({chat_id}).")
        except Exception as e:
            logging.error(f"Ошибка при бане пользователя с ID {user_to_ban_id} в чате {message.chat.title} ({chat_id}): {e}")


async def main():

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
