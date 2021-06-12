import logging

import database
from telegram.ext import (Updater,
                          Dispatcher,
                          Filters,
                          CommandHandler,
                          CallbackContext,
                          ConversationHandler,
                          MessageHandler
                          )

from telegram import (Bot,
                      ReplyKeyboardRemove, ReplyKeyboardMarkup,
                      KeyboardButton,
                      Update,
                      )

from config import TOKEN

from database import Database, Deadline, Teacher, Group

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
array = []

global bot_db, log


def analise(function):
    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message') and hasattr(update, 'effective_user'):
            array.append({
                "user": update.effective_user.first_name,
                "function": function.__name__,
                "message": update.message.text})
        return function(*args, **kwargs)

    return inner


def decorator_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SyntaxError:
            update = args[0]
            if update:
                update.message.reply_text(f'Error! Function:{func.__name__}')

    return inner


@decorator_error
@analise
def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    erroring = context.error
    logger.warning(f'Update {update} caused error {erroring}')
    return erroring


# ======== start command ========
@decorator_error
@analise
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Здраствуйте, {update.effective_user.first_name}! Этот чат-бот создан для отслеживания дедлайнов.\n"
        f"Проийти авторизацию. Для начала работы необходимо авторизоваться.\n")
    update.message.reply_text(f"Введите логин:")
    return 'login'


# ======== authorization ========
@decorator_error
@analise
def login(update: Update, context: CallbackContext):
    global log
    log = update.message.text
    update.message.reply_text('Введите пароль:')
    return 'passwd'


@decorator_error
@analise
def passwd(update: Update, context: CallbackContext):
    global bot_db, password
    password = update.message.text
    try:
        bot_db = Database(log, password)
    except database.OperationalError:
        update.message.reply_text('Неверные данные!')
    else:
        update.message.reply_text(f'Готово!\n'
                                  f'Для просмотра доступных действий введите /choose_actions')
    return ConversationHandler.END


# ======== choose action ========
@decorator_error
@analise
def choose_action(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton(text='Create db')],
                [KeyboardButton(text='Delete db')],
                [KeyboardButton(text='Print table')],
                [KeyboardButton(text='Clear table')],
                [KeyboardButton(text='Add data')],
                [KeyboardButton(text='Search by field')],
                [KeyboardButton(text='Update tuple')],
                [KeyboardButton(text='Delete by field')],
                [KeyboardButton(text='Delete data')]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f"Выберете действие:", reply_markup=reply_markup)
    return 'choose_action_end'


@decorator_error
@analise
def choose_action_end(update: Update, context: CallbackContext):
    text = {'Create db': 'Создание базы данных',
            'Delete db': 'Удаление базы данных...',
            'Print table': 'Распечатываем...',
            'Clear table': 'Выберете таблицу, которую хотите удалить:',
            'Add data': 'Выберете таблицу, в которую хотите добавить данные:',
            'Search by field': 'Производится поиск...',
            'Update tuple': 'Обновление',
            'Delete by field': 'Удаляем',
            'Delete data': 'Введите номер записи, которую хотите удалить'}

    role = update.message.text
    update.message.reply_text(text[role])
    if role == 'Create db':
        update.message.reply_text('Введите название базы данных:')
    elif role == 'Delete db':
        delete_db(update, context)
        return ConversationHandler.END
    elif role == 'Print table':
        print_table(update, context)
        return ConversationHandler.END
    elif role == 'Clear table':
        keyboard_clear = [[KeyboardButton(text='Выбрать таблицу')],
                          [KeyboardButton(text='Очистить полностью')]]
        reply = ReplyKeyboardMarkup(keyboard_clear, one_time_keyboard=True)
        update.message.reply_text(
            f"Как вы хотите очистить таблицы?", reply_markup=reply)
    elif role == 'Add data':
        keyboard_tables = [[KeyboardButton(text='Таблица1')],
                           [KeyboardButton(text='Таблица2')]]
        reply = ReplyKeyboardMarkup(keyboard_tables, one_time_keyboard=True)
        update.message.reply_text('Выбор:', reply_markup=reply)
    elif role == 'Search by field':
        search(update, context)
    elif role == 'Update tuple':
        update_tuple(update, context)
    elif role == 'Delete by field':
        delete_by_field(update, context)
    elif role == 'Delete data':
        delete_data(update, context)
    return role


@decorator_error
@analise
def create_db(update: Update, context: CallbackContext):
    if bot_db.create_db(login=log, password=password, name=update.message.text) == 0:
        update.message.reply_text('База данных создана!\n'
                                  'Если хотите добавить в нее таблицы, введите /add_table')
    else:
        update.message.reply_text('Такая база данных уже существует!')
    return ConversationHandler.END


# ======== delete db ========
@decorator_error
@analise
def delete_db(update: Update, context: CallbackContext):
    bot_db.delete_db()
    update.message.reply_text('База данных успешно удалена!')


@decorator_error
@analise
def print_table(update: Update, context: CallbackContext):
    bot_db.select_from_db()
    update.message.reply_text('Print!')


# ======== clear tables ========
@decorator_error
@analise
def clear_table(update: Update, context: CallbackContext):
    tabl = bot_db.get_tables()
    if update.message.text == 'Выбрать таблицу':
        keyboard_tables = [[KeyboardButton(text=tabl[0])],
                           [KeyboardButton(text=tabl[1])],
                           [KeyboardButton(text=tabl[2])]]
        reply = ReplyKeyboardMarkup(keyboard_tables, one_time_keyboard=True)
        update.message.reply_text(
            f"Выберете талицу:", reply_markup=reply)
        return 'Select table'
    elif update.message.text == 'Очистить полностью':
        bot_db.clear(name_table='', full_del=True)
        update.message.reply_text('Таблицы успешно удалены!')
    else:
        update.message.reply_text('Некорректный ввод')
    return ConversationHandler.END


@decorator_error
@analise
def select_table(update: Update, context: CallbackContext):
    bot_db.clear(name_table=update.message.text, full_del=False)
    update.message.reply_text('Таблица успешно удалена!')
    return ConversationHandler.END


@decorator_error
@analise
def add_data(update: Update, context: CallbackContext):
    # if update.message.text == '':
    update.message.reply_text('Введите название дисциплины:')
    discipline = update.message.text
    update.message.reply_text('Введите дедлайн (формат: ? ):')
    deadline = update.message.text
    update.message.reply_text('Введите задание:')
    task = update.message.text
    update.message.reply_text('Введите группу:')
    group = update.message.text
    add = bot_db.add_data(discipline, deadline, task, group)
    if add == -1 or add == -3:
        update.message.reply_text('Введите ФИО преподавателя:')
        teacher = update.message.text
        update.message.reply_text('Введите e-mail преподавателя:')
        mail = update.message.text
        bot_db.add_teacher(discipline, teacher, mail)
    if add == -2 or add == -3:
        update.message.reply_text('Введите e-mail группы:')
        mail = update.message.text
        bot_db.add_group(group, mail)
    return 'End add'


def end_add(update:Update, context: CallbackContext):
    bot_db.add_data()
    update.message.reply_text('Добавлено')
    return ConversationHandler.END

@decorator_error
@analise
def search(update: Update, context: CallbackContext):
    bot_db.search()
    update.message.reply_text('Search!')


@decorator_error
@analise
def update_tuple(update: Update, context: CallbackContext):
    # bot_db.update_tuple()
    update.message.reply_text('Update tuple!')


@decorator_error
@analise
def delete_by_field(update: Update, context: CallbackContext):
    bot_db.delete_by_field()
    update.message.reply_text('Delete!')


@decorator_error
@analise
def delete_data(update: Update, context: CallbackContext):
    bot_db.delete_data()
    update.message.reply_text('Data delete!')


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # start command handler
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            'login': [MessageHandler(Filters.text, login)],
            'passwd': [MessageHandler(Filters.text, passwd)]},
        fallbacks=[MessageHandler(Filters.text, error)]
    ))

    # actions handler
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('choose_actions', choose_action)],

        states={
                'choose_action_end': [MessageHandler(Filters.text, choose_action_end)],
                'Create db': [MessageHandler(Filters.text,  create_db)],
                'Print table': [MessageHandler(Filters.text, print_table)],
                'Clear table': [MessageHandler(Filters.text, clear_table)],
                'Select table': [MessageHandler(Filters.text, select_table)],
                'Add data': [MessageHandler(Filters.text, add_data)],
                'End add': [MessageHandler(Filters.text, end_add)],
                'Search by field': [MessageHandler(Filters.text, search)],
                'Update tuple': [MessageHandler(Filters.text, update_tuple)],
                'Delete by field': [MessageHandler(Filters.text, delete_by_field)],
                'Delete data': [MessageHandler(Filters.text, delete_data)],
                },
        fallbacks=[MessageHandler(Filters.text, error)]
    ))
    dispatcher.add_error_handler(error)

    updater.start_polling()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()