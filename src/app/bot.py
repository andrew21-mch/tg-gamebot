import logging
import platform

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram.update import Update

from constants import BOT_API_KEY, BOT_NAME
# function to greet the user
from data.quiz import test_poll

# function to handle the /start command
from menus import main_menu_keyboard


def start_command(update: Update, context: CallbackContext) -> None:
    logging.info('Starting game')
    update.message.reply_text("Hi\nTo start a game, select game type.")


def oss_bot_about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'BOT NAME: {BOT_NAME} \n BOT VERSION: 1.0 \n BOT PLATFORM: {platform.system()} is a quizbot designed to make the community interactive 😂 have fun while developing your skills')


# show available games
def oss_bot_games(update: Update, context: CallbackContext):
    update.message.reply_text("Games are not implemented yet")


# Display leaderboard
def oss_bot_leaderboard(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Leaderboard is not implemented yet")


# stop ongoing game
def oss_bot_stop(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Stopping game")
    test_poll.stop()


# schedule a game
def oss_bot_schedule(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Scheduling games")


# pause game
def oss_bot_pause(update: Update, context: CallbackContext) -> None:
    test_poll.pause()


# resume game
def oss_bot_resume(update: Update, context: CallbackContext) -> None:
    test_poll.resume()


def oss_bot_menu(update: Update, context: CallbackContext) -> None:
    reply_markup = main_menu_keyboard
    update.message.reply_text('Select Menu', reply_markup=reply_markup)


# function to handle the /help command
def help_command(update: Update, context: CallbackContext):
    commands = {
        'About': 'Display information about the bot \nPress',
        'Help': 'display help comands \nPress',
        'Games': 'display a list of available games \nPress',
        'Leaderboard': 'display the leaderboard \nPress',
        'Schedule': 'schedules games \nPress',
        'Start': 'Start a game \nPress',
        'Pause': 'pause ongoing game \nPress',
        'Resume': 'resume paused game \nPress',
        'Stop': 'stop game \nPress',
    }
    reply = 'OSSCAMEROON QUIZBOT HELP!:\n=====================\n'
    # format the help commands as type buttons
    for command in commands:
        reply += f'To {commands[command]} : \t /{command.lower()}\n\n'
    update.message.reply_text(reply)

    



# function to handle errors occurred in dispatcher
def oss_bot_error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)


def oss_bot_text(update: Update, context: CallbackContext):
    text_received = update.message.text
    update.message.reply_text(f'You said: {text_received}')


def menu_actions(update: Update, context: CallbackContext) -> None:
    print("menu_actions")
    query = update.callback_query
    query.answer()

    query.edit_message_text(text='Start Menu', reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='START', callback_data="/start")],
         [InlineKeyboardButton(text='back', callback_data="main_menu")], ]
    ))


def handler():
    updater = Updater(BOT_API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    # create handlers for all functions above
    dispatcher.add_handler(CommandHandler('start', oss_bot_start))
    dispatcher.add_handler(CommandHandler('help', oss_bot_help))
    dispatcher.add_handler(CommandHandler('about', oss_bot_about))
    dispatcher.add_handler(CommandHandler('games', oss_bot_games))
    dispatcher.add_handler(CommandHandler('leaderboard', oss_bot_leaderboard))
    dispatcher.add_handler(CommandHandler('stop', oss_bot_stop))
    dispatcher.add_handler(CommandHandler('schedule', oss_bot_schedule))
    dispatcher.add_handler(CommandHandler('pause', oss_bot_pause))
    dispatcher.add_handler(CommandHandler('resume', oss_bot_resume))
    dispatcher.add_handler(CommandHandler('menu', oss_bot_menu))

    # callback query handlers
    dispatcher.add_handler(CallbackQueryHandler(menu_actions, pattern='menu1'))

    dispatcher.add_handler(MessageHandler(Filters.text, oss_bot_text))
    dispatcher.add_error_handler(oss_bot_error)

    # run til infinity
    updater.start_polling()

    updater.idle()
