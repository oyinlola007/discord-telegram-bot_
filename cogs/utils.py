
def read_message_text(message):
    message = message.to_dict()
    text = message['message']['text']
    username = message['message']['from']['first_name']
    return f">>> {username}: {text}"

def read_message_id(message):
    message = message.to_dict()
    chat_id = message['message']['chat']['id']
    return chat_id

def is_bot(message):
    message = message.to_dict()
    return message['message']['from']['is_bot']

def get_sent_time(message):
    message = message.to_dict()
    return message['message']['date']


def send_to_telegram(bot, chat_id, text):
    bot.send_message(chat_id=chat_id, text=text)
