# Function for sending message to Telegram using Telegram BeautifulSoup
import requests

def telegram_bot_sendtext(bot_message):
    # Put your bot_token (use BotFather - Telegram id - "bot",  to get your own new bot, use /help and /newbot for that)
    bot_token = 'YOUR TOKEN'
    # Hoe to get your bot chat ID you can see on the webpage https://buddha.net.ua/find-telegram-chat-bot-id
    bot_chatID = 'YOUR CHATID'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
