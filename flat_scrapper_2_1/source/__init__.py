from time import sleep

from ComparisScrapper import ComparisScrapper
from HomeGateScrapper import HomeGateScrapper
import telegram
from datetime import datetime
from RequestHandler import RequestHandler

bot = telegram.Bot(token="<token goes here>")
request_handler = RequestHandler().requests_retry_session()

while True:
    try:
        updates = bot.get_updates()
        if len(updates) > 0:
            for update in updates:
                if update.effective_message["message_id"] == updates[len(updates) - 1].effective_message["message_id"]:
                    if int(datetime.timestamp(update["message"]["date"])) == int(datetime.timestamp(datetime.now())):
                        message_text = update.effective_message.text
                        chat_id = update.effective_chat
                        if message_text == "Homegate":
                            homegate_scrapper = HomeGateScrapper(request_handler,"2.5", "1500", "2400")
                            homegate_list = homegate_scrapper.getFlats()
                            for flat in homegate_list:
                                update.message.reply_text(flat)
                        elif message_text == "Comparis":
                            comparis_scrapper = ComparisScrapper(request_handler,"2.5", "1500", "2400")
                            comparis_list = comparis_scrapper.getFlats()
                            for flat in comparis_list:
                                update.message.reply_text(flat)
    except Exception as e:
        sleep(10)
        print("Failed to retrieve updates from Telegram with exception: ", e)
