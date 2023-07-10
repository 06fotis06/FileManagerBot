import os
from aiogram import Bot, Dispatcher, types,executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

TOKEN = "6052307193:AAEGqIyhbzSx0L1_G6twalTI-PqLNLqwGVI"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Создаем клавиатуру с кнопками команд
commands_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/list"),
            KeyboardButton(text="/change_dir"),
        ],
        [
            KeyboardButton(text="/create_dir"),
            KeyboardButton(text="/delete_dir"),
        ],
        [
            KeyboardButton(text="/create_file"),
            KeyboardButton(text="/delete_file"),
        ],
        [
            KeyboardButton(text="/command"),
        ]
    ],
    resize_keyboard=True
)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """Обработчик команды /start"""
    await message.reply("Привет! Я файловый менеджер бот. Ниже кнопки для управления файлами и папками:",
                             reply_markup=commands_keyboard)


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    """Обработчик команды /help"""
    help_text = "/list - Показать файлы и папки в текущей директории\n"
    help_text += "/change_dir - Сменить текущую директорию\n"
    help_text += "/create_dir - Создать новую папку\n"
    help_text += "/delete_dir - Удалить папку\n"
    help_text += "/create_file - Создать новый файл\n"
    help_text += "/delete_file - Удалить файл"
    await message.reply(help_text)


@dp.message_handler(commands=['list'])
async def list_files(message: types.Message):
    """Обработчик команды /list"""
    current_dir = os.getcwd()
    files = os.listdir(current_dir)
    file_list = "\n".join(files)
    await message.reply(f"Файлы и папки в текущей директории:\n{file_list}")


@dp.message_handler(commands=['change_dir'])
async def change_dir(message: types.Message, state: FSMContext):
    """Обработчик команды /change_dir"""
    await message.reply("Введите путь к новой директории:")
    await state.set_state("change_dir")
    
    		


@dp.message_handler(state="change_dir")
async def process_change_dir(message: types.Message, state: FSMContext):
    try:
    	new_dir = message.text
    	os.chdir(new_dir)
    	await message.reply(f"Текущая директория изменена на: {new_dir}")
    	await state.finish()
    except:
    	await message.reply(f"Директория {new_dir} не найдена")


@dp.message_handler(commands=['create_dir'])
async def create_dir(message: types.Message, state: FSMContext):
    """Обработчик команды /create_dir"""
    await message.reply("Введите имя новой папки:")
    await state.set_state("create_dir")


@dp.message_handler(state="create_dir")
async def process_create_dir(message: types.Message, state: FSMContext):
    """Обработка имени новой папки в состоянии create_dir"""
    dir_name = message.text
    os.mkdir(dir_name)
    await message.reply(f"Папка {dir_name} создана.")
    await state.finish()



@dp.message_handler(commands=['delete_dir'])
async def delete_dir(message: types.Message, state: FSMContext):
    """Обработчик команды /delete_dir"""
    await message.reply("Введите имя папки для удаления:")
    await state.set_state("delete_dir")


@dp.message_handler(state="delete_dir")
async def process_delete_dir(message: types.Message, state: FSMContext):
    """Обработка имени папки для удаления в состоянии delete_dir"""
    try:
    	dir_name = message.text
    	os.rmdir(dir_name)
    	await message.reply(f"Папка {dir_name} удалена.")
    	await state.finish()
    except:
    	await message.reply(f"Папка {dir_name} не найдена.")
    	



@dp.message_handler(commands=['create_file'])
async def create_file(message: types.Message, state: FSMContext):
    """Обработчик команды /create_file"""
    await message.reply("Введите имя нового файла:")
    await state.set_state("create_file")


@dp.message_handler(state="create_file")
async def process_create_file(message: types.Message, state: FSMContext):
    """Обработка имени нового файла в состоянии create_file"""
    file_name = message.text
    open(file_name, "w").close()
    await message.reply(f"Файл {file_name} создан.")
    await state.finish()


@dp.message_handler(commands=['delete_file'])
async def delete_file(message: types.Message, state: FSMContext):
    """Обработчик команды /delete_file"""
    await message.reply("Введите имя файла для удаления:")
    await state.set_state("delete_file")


@dp.message_handler(state="delete_file")
async def process_delete_file(message: types.Message, state: FSMContext):
    """Обработка имени файла для удаления в состоянии delete_file"""
    try:
    	file_name = message.text
    	os.remove(file_name)
    	await message.reply(f"Файл {file_name} удален.")
    	await state.finish()
    except:
    	await message.reply(f"Файл  {file_name} не найден.")
    

@dp.message_handler(commands=['command'])
async def execute_command(message: types.Message, state: FSMContext):
    """Обработчик команды /command"""
    await message.reply("Введите команду для выполнения:")
    await state.set_state("command")


@dp.message_handler(state="command")
async def process_command(message: types.Message, state: FSMContext):
    """Обработка команды для выполнения в состоянии command"""
    command = message.text
    os.system(f"{command}")
    await message.reply(f"Команда : {command}: выполнена")
    await state.finish()



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
