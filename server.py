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

# ======== start command ========
CHOOSE_GROUP = 1


def start(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton(text='19ПИ-1')],
                [KeyboardButton(text='19ПИ-2')]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    update.message.reply_text(
        f"Здраствуйте, {update.effective_user.first_name}! Этот чат-бот создан для отслеживания дедлайнов."
        f"\n\n"
        f"Выберете вашу группу:",
        reply_markup=reply_markup)
    return CHOOSE_GROUP


def choose_group(update: Update, context: CallbackContext):
    text = {"19ПИ-1": "Hello, 19ПИ-1",
            "19ПИ-2": "Hello, 19ПИ-2"}

    role = update.message.text

    update.message.reply_text(text[role])

    update.message.reply_text("Доступные действия:",
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def cancel_start(update: Update, context: CallbackContext):
    return ConversationHandler.END


# ======= choose action ==========
CHOOSE_ACTION = 2


def choose_action(update: Update, context: CallbackContext):
    print('hi, i\'m here!')
    keyboard = [[KeyboardButton(text='Удаление db')],
                [KeyboardButton(text='Вывести таблицу')],
                [KeyboardButton(text='Очистка таблицы')],
                [KeyboardButton(text='Добавление данных')],
                [KeyboardButton(text='Поиск')],
                [KeyboardButton(text='Обновление кортежа')],
                [KeyboardButton(text='Удаление по полю')],
                [KeyboardButton(text='Удаление конкретной записи')]]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

    update.message.reply_text(reply_markup=reply_markup)

    return CHOOSE_ACTION


def choose_action_end(update: Update, context: CallbackContext):
    text = {'Удаление db': 'Вы уверены, что хотите удалить db?',
            'Вывести таблицу': 'Таблица:',
            'Очистка таблицы': 'Выберете, как вы хотите очистить таблицу:',
            'Добавление данных': '',
            'Поиск': '',
            'Обновление кортежа': '',
            'Удаление по полю': '',
            'Удаление конкретной записи': ''}

    role = update.message.text

    update.message.reply_text(text[role])

    if role == 'Удаление db':
        update.message.reply_text('Ну давай, удаляй!')

    return ConversationHandler.END


def cancel_choose_action(update: Update, context: CallbackContext):
    return ConversationHandler.END


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # start command handler
    start_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSE_GROUP: [MessageHandler(Filters.text & ~Filters.command, choose_group)],
            CHOOSE_ACTION: [MessageHandler(Filters.text & ~Filters.command, choose_action)]},

        fallbacks=[CommandHandler("cancel_start", cancel_start)]
    )

    dispatcher.add_handler(start_handler)

    # choose action handler
    choose_action_handler = ConversationHandler(
        entry_points=[CommandHandler('choose_action', choose_action)],

        states={
            CHOOSE_ACTION: [MessageHandler(Filters.text & ~Filters.command, choose_action_end)]},

        fallbacks=[CommandHandler("cancel_choose_action", cancel_choose_action)]

    )
    dispatcher.add_handler(choose_action_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()

# todo: разобраться, почему не показываются кнопки
