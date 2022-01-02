import os
import pytz
import time
import datetime
from pyrogram import Client

user_session_string = os.environ.get("SESSION_NAME")
bots = [i.strip() for i in os.environ.get("BOTS").split(' ')]
updates_channel = os.environ.get("UPDATES_CHANNEL")
status_message_ids = [int(i.strip()) for i in os.environ.get("MESSAGE_ID").split(' ')]
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
user_client = Client(session_name=str(user_session_string), api_id=api_id, api_hash=api_hash)


def main():
    with user_client:
        while True:
            print("[INFO] starting to check bots uptime...")
            edit_text = "@JaguarBots Status\n\n\n"
            for bot in bots:
                print(f"[INFO] checking @{bot}")
                snt = user_client.send_message(bot, '/start')

                time.sleep(10)

                msg = user_client.get_history(bot, 1)[0]
                if snt.message_id == msg.message_id:
                    print(f"[WARNING] @{bot} is down")
                    edit_text += f"🤖 - @{bot}\nStatus ❌\n\n"
                else:
                    print(f"[INFO] @{bot} is up")
                    edit_text += f"🤖 - @{bot}\nStatus ✅\n\n"
                user_client.read_history(bot)

            time_now = datetime.datetime.now(pytz.timezone('Asia/Colombo'))
            formatted_time = time_now.strftime("%d %B %Y %I:%M %p")

            edit_text += f"**Last Update: {formatted_time} (LST)**"

            for status_message_id in status_message_ids:
                user_client.edit_message_text(int(updates_channel), status_message_id,
                                         edit_text)
                time.sleep(5)
            print(f"[INFO] everything done! sleeping for 6 hours...")

            time.sleep(21600)


if __name__ == "__main__":
    main()
