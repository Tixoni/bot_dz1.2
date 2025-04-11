from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database import create_table, add_homework, get_all_homework, delete_homework,delete_old_homework


router = Router()  # router = Dispatcher

create_table()#база данных 


class Add(StatesGroup):
    date = State()
    subject = State()
    home_work = State()

    delete_homework_date = State()
    delete_homework_subject = State()




@router.message(Command("start"))
async def cmd_start(message: Message):
    kb = [
        [KeyboardButton(text="/list")],
        [KeyboardButton(text="/add")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    await message.answer("Я бот с ДЗ. Используйте кнопки /add для добавления задания и /list для просмотра списка дз.", reply_markup=keyboard)

@router.message(Command("list"))
async def list_homework(message: Message, state: FSMContext):
    homework_list = get_all_homework()

    if not homework_list:
        await message.answer("📭 На данный момент домашних заданий нет!")
        return

    # Сортируем по дате (в формате ДД.ММ.ГГГГ) и затем по предмету
    homework_list.sort(key=lambda hw: (hw[0].split('.')[::-1], hw[1]))

    hlist = "📌 <b>Актуальное домашнее задание:</b>\n\n"

    for hw in homework_list:
        hw_date, subject, task = hw  # Распаковываем кортеж (Дата, Предмет, Задание)
        hlist += f"📅 <b>{hw_date}</b>\n📖 <b>{subject}</b>\n📝 {task}\n\n"

    await message.answer(hlist, parse_mode="HTML")


#----------------------------------------------------/delete--------------------------------------------------------------------------------------------

@router.message(Command("delete"))
async def delete(message: Message, state: FSMContext):
    global homework_date, homework_subject
    await state.set_state(Add.delete_homework_date)
    msg = await message.answer("📅 Введите дату (например, 05.11.2025):")
    await state.update_data(bot_id=msg.message_id)

@router.message(Add.delete_homework_date)
async def delete_date(message: Message, state: FSMContext):
    global homework_date
    data = await state.get_data()
    bot_id = data.get("bot_id")
    user_id = message.message_id

    homework_date = message.text
    await state.set_state(Add.delete_homework_subject)
    msg = await message.answer("📖 Выберите предмет:")#
    await state.update_data(bot_id=msg.message_id)

    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_id) # удаление последнего сообщения бота
    await message.bot.delete_message(chat_id=message.chat.id, message_id=user_id) # удаление последнего сообщения юзера

@router.message(Add.delete_homework_subject)
async def delete_homework_entry(message: Message, state: FSMContext):
    
    homework_subject = message.text
    delete_homework(homework_date, homework_subject)  # вызов функции удаления ДЗ
    
    await message.answer("✅ Домашнее задание удалено.")
    await state.clear()




#---------------------------------------------------/add----------------------------------------------------------------------------------------------------

# Функция для создания inline-клавиатуры с предметами
def get_subject_keyboard():
    subjects = ["Матан", "Линал", "Информатика", "СиАОД", "ИИ", "ООП", "Физика",
    "История", "Английский 1 груп.", "Английский 2 груп.", "Руский","Правоведение"]
    
    builder = InlineKeyboardBuilder()
    for subject in subjects:
        builder.button(text=subject, callback_data=f"subject_{subject}")
    builder.adjust(2)  # Делает кнопки по 2 в ряд
    return builder.as_markup()



# Обработчик команды /add
# Обработчик ввода даты
@router.message(Command("add"))
async def add(message: Message, state: FSMContext):
    delete_old_homework() #удаляем старое дз
    await state.set_state(Add.date)
    msg = await message.answer("📅 Введите дату (например, 05.11.2025):")
    await state.update_data(bot_id=msg.message_id)


@router.message(Add.date)
async def add_date(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_id = data.get("bot_id")
    user_id = message.message_id

    await state.update_data(date=message.text)
    await state.set_state(Add.subject)

    msg = await message.answer("📖 Выберите предмет:", reply_markup=get_subject_keyboard())
    await state.update_data(bot_id=msg.message_id)

    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_id) #удаление последнего сообщения бота
    await message.bot.delete_message(chat_id=message.chat.id, message_id=user_id)#удаление последнего сообщения юзера

#обработка нажатия на кнопку - выбор предмета 
@router.callback_query(lambda c: c.data.startswith("subject_"))
async def subject_selected(callback: CallbackQuery, state: FSMContext):
    # Получаем текст предмета из callback_data
    subject = callback.data.replace("subject_", "")  # Например, "Математика"

    # Получаем данные из состояния
    data = await state.get_data()
    bot_id = data.get("bot_id")

    # Сохраняем выбранный предмет в состоянии
    await state.update_data(subject=subject)
    await state.set_state(Add.home_work)

    # Отправляем сообщение от имени бота с текстом, как на кнопке
    await callback.message.answer(f"📖 Вы выбрали предмет: {subject}")

    # Удаляем предыдущее сообщение бота (с клавиатурой)
    try:
        await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=bot_id)
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")

    # Удаляем сообщение с кнопкой
    try:
        await callback.message.delete()
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")

    # Запрашиваем ввод задания
    msg = await callback.message.answer("📝 Введите задание:")
    await state.update_data(bot_id=msg.message_id)

# Обработчик ввода задания
@router.message(Add.home_work)
async def add_home_work(message: Message, state: FSMContext):
    data = await state.get_data()
    bot_id = data.get("bot_id")
    user_id = message.message_id

    date = data.get("date")
    subject = data.get("subject")
    homework = message.text

    add_homework(date, subject, homework)

    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_id)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=user_id)

    await message.answer(f"✅ ДЗ добавлено!\n\n📅 Дата: {date}\n📖 Предмет: {subject}\n📝 Задание: {homework}")
    await state.clear()

