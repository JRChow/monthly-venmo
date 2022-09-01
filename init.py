from venmo_api import Client
from dotenv import load_dotenv
from notifiers import get_notifier
from datetime import datetime

from utils import get_env, env_vars, get_month, Venmo, Telegram

def main(now):
  """
  The main function which initiates the script.
  """

  load_dotenv()  # take environment variables from .env.
  actualVars = []
  for var in env_vars:
    actualVars.append(get_env(var))

  access_token, chat_id, bot_token, p_friend_id, d_friend_id, g_friend_id = actualVars

  month = get_month(now)
  venmo = Venmo(access_token)
  telegram = Telegram(bot_token, chat_id)

  friends =[
    {
      "name": "XP",
      "id": p_friend_id,
    },
# On pause until payment resumes
#    {
#      "name": "YD",
#      "id": d_friend_id,
#    },
    {
      "name": "GL",
      "id": g_friend_id,
    },
  ]

  successfulRequests = []
  expectedRequests = len(friends)

  for friend in friends:
    name = friend["name"]
    id = venmo.get_user_id_by_username(friend["id"])
    description = "HBO Max for the month of " + month + " — Sent by JrZ's GitHub Actions"
    amount = 14.99 / (len(friends) + 1)
    message = f"""Good news old sport!

I have successfully requested money from {name}.

— Efron 🤵🏻‍♂️
    """
    success = venmo.request_money(id, amount, description, telegram.send_message(message))
    if success:
      successfulRequests.append(success)

  if len(successfulRequests) == expectedRequests:
    print("✅ Ran script successfully and sent " + str(expectedRequests) + " Venmo requests.")
  else:
    print("❌ Something went wrong. Only sent " + str(len(successfulRequests)) + "/" + str(expectedRequests) + " venmo requests.")

now = datetime.now()
main(now)
