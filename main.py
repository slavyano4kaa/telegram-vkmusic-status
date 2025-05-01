import time
import vk_api
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateProfileRequest

########################
app_token = 'yourapptoken' # токен из vk.com/apps?act=manage
user_id = 'yourvkusername' # id страницы или никнейм
defaultabout = 'youraboutme' # дефолтное описание в телеграме если ничего не играет
api_id = 000000000 # api_id из my.telegram.org
api_hash = 'yourapihash' # api_hash из my.telegram.org
########################

client = TelegramClient('session', api_id, api_hash)
async def main():
    await client.start()
    user = await client.get_me()
    print(f"Telegram: {user.first_name} ({user.username})")
    vk_session = vk_api.VkApi(token=app_token)
    vk = vk_session.get_api()
    last_status = None
    
    while True:
        try:
            res = vk.users.get(user_ids=user_id, fields="status")[0]
            if "status_audio" not in res:
                status = defaultabout
            else:
                currentmusic = res["status_audio"]
                artist = currentmusic["artist"]
                title = currentmusic["title"]
                status = f"🎧 Слушает {artist} - {title} | VK Music"
            if status != last_status:
                await client(UpdateProfileRequest(about=status))
                print("Установлено: ", status)
                last_status = status
        except Exception as error:
            print("Error:", error)
        time.sleep(5)

with client:
    client.loop.run_until_complete(main())
