from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


def register(cb):
    cb(installer())


class installer(loader.Module):
    """Модуль скачивает видео с Instagram, YouTube, TikTok, Pinterest или VK Clips\n подпишись на канал @modwini"""

    strings = {"name": "installer"}

    def __init__(self):
        self.name = self.strings["name"]
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()

    async def incmd(self, event):
        """<ссылка>"""
        user_msg = """{}""".format(utils.get_args_raw(event))
        global reply_and_text
        reply_and_text = False
        if event.fwd_from:
            return
        if not event.reply_to_msg_id:
            self_mess = True
            if not user_msg:
                await event.edit(".in")
                return
        elif event.reply_to_msg_id and user_msg:
            reply_message = await event.get_reply_message()
            reply_and_text = True
            self_mess = True
        elif event.reply_to_msg_id:
            reply_message = await event.get_reply_message()
            self_mess = False
        chat = "@allsaverbot"
        await event.edit("<code>Загрузка...</code>")
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=804576054)
                )
                if not self_mess:
                    await event.client.forward_messages(chat, reply_message)
                else:
                    await event.client.send_message(chat, user_msg)
                response = await response
            except YouBlockedUserError:
                await event.reply("<code>Разблокируй </code>@allsaverbot")
                return
            await event.delete()
            if reply_and_text:
                await event.client.send_file(
                    event.chat_id, response.video, reply_to=reply_message.id
                )
            else:
                await event.client.send_file(event.chat_id, response.video)