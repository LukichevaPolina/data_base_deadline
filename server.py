import logging

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

from database import bot_db

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
array = []


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
    keyboard = [[KeyboardButton(text='Delete db')],
                [KeyboardButton(text='Print table')],
                [KeyboardButton(text='Clear table')],
                [KeyboardButton(text='Add data')],
                [KeyboardButton(text='Search by field')],
                [KeyboardButton(text='Update tuple')],
                [KeyboardButton(text='Delete by field')],
                [KeyboardButton(text='Delete data')]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    update.message.reply_text(
        f"Здраствуйте, {update.effective_user.first_name}! Этот чат-бот создан для отслеживания дедлайнов.\n"
        f"Доступные команды:\n", reply_markup=reply_markup)
    return 'choose_action'


# ======== choose action ========
@decorator_error
@analise
def choose_action(update: Update, context: CallbackContext):
    text = {'Delete db': 'Удаление базы данных...',
            'Print table': 'Распечатываем...',
            'Clear table': 'Выберете таблицу, которую хотите удалить:',
            'Add data': 'Введите сообщение в формате ...',
            'Search by field': 'Введите данные, которые небходимо ввести',
            'Update tuple': 'это что такое, а ?',
            'Delete by field': 'нет блин по лесу',
            'Delete data': 'Введите номер записи, которую хотите удалить'}

    role = update.message.text
    update.message.reply_text(text[role])
    if role == 'Delete db':
        delete_db(update, context)
    elif role == 'Print table':
        print_table(update, context)
    elif role == 'Clear table':
        clear_table(update, context)
    elif role == 'Add data':
        add_data(update, context)
    elif role == 'Search by field':
        search(update, context)
    elif role == 'Update tuple':
        update_tuple(update, context)
    elif role == 'Delete by field':
        delete_by_field(update, context)
    elif role == 'Delete data':
        delete_data(update, context)
    return 'choose_action'


# ======== actions ========
@decorator_error
@analise
def delete_db(update: Update, context: CallbackContext):
    bot_db.delete_db()
    update.message.reply_text('Delete!')


@decorator_error
@analise
def print_table(update: Update, context: CallbackContext):
    bot_db.select_from_db()
    update.message.reply_text('Print!')


@decorator_error
@analise
def clear_table(update: Update, context: CallbackContext):
    bot_db.clear()
    update.message.reply_text('Clear!')


@decorator_error
@analise
def add_data(update: Update, context: CallbackContext):
    bot_db.add_data()
    update.message.reply_text('Add!!!!')


@decorator_error
@analise
def search(update: Update, context: CallbackContext):
    bot_db.search()
    update.message.reply_text('Search!')


@decorator_error
@analise
def update_tuple(update: Update, context: CallbackContext):
    bot_db.update_tuple()
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
            'choose_action': [MessageHandler(Filters.text, choose_action)],
            '': ''},
        fallbacks=[MessageHandler(Filters.text, error)]
    ))

    dispatcher.add_error_handler(error)

    updater.start_polling()


if __name__ == '__main__':
    logger.info('Start Bot')
    main()

