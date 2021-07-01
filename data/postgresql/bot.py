import requests
import os

def telegram_bot_sendtext(message):

    bot_token = ''
    chatID = ''
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chatID + '&text=' + message
    requests.get(send_text)

    return

def get_blocks_status():
    count = len(os.listdir("/home/VMadmin/data/blocks"))
    return "Parsed untill block {}".format(count)

telegram_bot_sendtext(get_blocks_status())
