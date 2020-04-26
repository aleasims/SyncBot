"""
Simple echo bot.

Required env:
    TOKEN
    VK_GROUP_ID
"""

import os
import json

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll, VkBotEvent
from vk_api.utils import get_random_id

TOKEN = os.getenv('VK_TOKEN')
GROUP_ID = int(os.getenv('VK_GROUP_ID'))
API_VERSION = '5.103'
PHOTO_ID = 457239018


def main():
    vk_session = vk_api.VkApi(token=TOKEN, api_version=API_VERSION)
    print(f'API version: {vk_session.api_version}')

    vk = vk_session.get_api()

    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    print(f'Longpoll server: {longpoll.url}')

    print('Waiting for events...')
    for event in longpoll.listen():
        event: VkBotEvent
        print(event.type)

        if event.type == VkBotEventType.MESSAGE_NEW:
            print('New message:')
            print(json.dumps(event.message, indent=4))

            if event.from_chat:
                msg = f"{event.message['from_id']}: {event.message['text']}"
                vk.messages.send(chat_id=event.chat_id,
                                 message=msg,
                                 random_id=get_random_id(),
                                 attachment=f'photo-{GROUP_ID}_{PHOTO_ID}')
            print(f'Responded: {repr(msg)} + BONUS PHOTO')

        print('\nWaiting for events...')


if __name__ == "__main__":
    main()
