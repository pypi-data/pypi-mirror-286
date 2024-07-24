import io
import json
from typing import Any, Iterable, Optional, Union

import aiohttp
import nio
from slidge import BaseSession, global_config
from slidge.util.types import (
    LegacyMessageType,
    LegacyThreadType,
    LinkPreview,
    Mention,
    PseudoPresenceShow,
    ResourceDict,
)
from slixmpp.exceptions import XMPPError

from . import config
from .contact import Contact, Roster
from .group import MUC, Bookmarks, Participant
from .matrix import Client
from .util import get_content

Sender = Union[Contact, Participant]
Recipient = Union[MUC, Contact]


class Session(BaseSession[str, Recipient]):
    bookmarks: Bookmarks
    contacts: Roster
    matrix: Client

    MESSAGE_IDS_ARE_THREAD_IDS = True

    def __init__(self, *a):
        super().__init__(*a)
        self.events_to_ignore = set[str]()
        self.migrate_shelf()

    def migrate_shelf(self):
        store_path = global_config.HOME_DIR / self.user_jid.bare
        if not store_path.exists():
            return
        user = self.user
        with store_path.open("r") as f:
            user.legacy_module_data = json.load(f)
        self.xmpp.store.users.update(user)
        self.log.info(
            "Credentials info transferred from %s to the slidge DB", store_path
        )
        store_path.unlink()

    async def login(self):
        f = self.user.legacy_module_data
        self.matrix = Client(f["homeserver"], f["user_id"], self)  # type:ignore
        await self.matrix.login_token()
        await self.matrix.listen()
        self.contacts.user_legacy_id = self.matrix.user_id  # type:ignore
        return f"Logged in as {self.matrix.user}"

    async def logout(self):
        self.matrix.stop_listen()

    async def __relates_to(
        self,
        room_id: str,
        content: dict[str, Any],
        reply_to_msg_id: Optional[str],
        thread: Optional[str],
    ):
        relates_to = dict[str, Any]()
        if reply_to_msg_id:
            relates_to["m.in_reply_to"] = {
                "event_id": await self.matrix.get_original_id(room_id, reply_to_msg_id)
            }
        if thread:
            relates_to["rel_type"] = "m.thread"
            relates_to["event_id"] = thread
        if relates_to:
            content["m.relates_to"] = relates_to

    async def __handle_response(self, response: nio.Response):
        self.log.debug("Send response: %s", response)
        if isinstance(response, nio.RoomSendError):
            raise XMPPError("internal-server-error", str(response))
        assert isinstance(response, nio.RoomSendResponse)
        i = response.event_id
        self.events_to_ignore.add(i)
        return i

    async def __room_send(
        self, chat: MUC, content: dict, message_type="m.room.message"
    ):
        await self.matrix.room_typing(chat.legacy_id, False)
        response = await self.matrix.room_send(
            chat.legacy_id,
            message_type=message_type,
            content=content,
            ignore_unverified_devices=config.TRUST_EVERYTHING,
        )
        return await self.__handle_response(response)

    async def on_text(
        self,
        chat: Recipient,
        text: str,
        *,
        reply_to_msg_id: Optional[str] = None,
        reply_to_fallback_text: Optional[str] = None,
        reply_to: Optional[Sender] = None,  # type: ignore
        thread: Optional[str] = None,  # type: ignore
        link_previews: Iterable[LinkPreview] = (),
        mentions: Optional[list[Mention]] = None,
    ) -> Optional[LegacyMessageType]:
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        content = get_content(text, mentions)
        await self.__relates_to(chat.legacy_id, content, reply_to_msg_id, thread)
        return await self.__room_send(chat, content)

    async def on_file(
        self,
        chat: Recipient,
        url: str,
        *,
        http_response: aiohttp.ClientResponse,
        reply_to_msg_id: Optional[str] = None,
        reply_to_fallback_text: Optional[str] = None,
        reply_to: Optional[Sender] = None,  # type: ignore
        thread: Optional[str] = None,  # type: ignore
    ) -> Optional[LegacyMessageType]:
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        filename = url.split("/")[-1]
        content_type = http_response.content_type
        resp, _ = await self.matrix.upload(
            io.BytesIO(await http_response.read()),
            content_type,
            filename,
            filesize=http_response.content_length,
        )
        self.log.debug("Upload response: %s %r", type(resp), resp)
        if not isinstance(resp, nio.UploadResponse):
            raise XMPPError("internal-server-error", str(resp))
        content = {
            "msgtype": "m.image" if content_type.startswith("image") else "m.file",
            "body": filename,
            "url": resp.content_uri,
        }
        await self.__relates_to(chat.legacy_id, content, reply_to_msg_id, thread)
        return await self.__room_send(chat, content)

    async def on_composing(
        self, chat: Recipient, thread: Optional[LegacyThreadType] = None
    ):
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        await self.matrix.room_typing(chat.legacy_id)

    async def on_paused(
        self, chat: Recipient, thread: Optional[LegacyThreadType] = None
    ):
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        await self.matrix.room_typing(chat.legacy_id, False)

    async def on_displayed(
        self,
        chat: Recipient,
        legacy_msg_id: LegacyMessageType,
        thread: Optional[LegacyThreadType] = None,
    ):
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        resp = await self.matrix.update_receipt_marker(chat.legacy_id, legacy_msg_id)
        self.log.debug("Displayed response: %s", resp)

    async def on_correct(
        self,
        chat: Recipient,
        text: str,
        legacy_msg_id: str,
        *,
        thread: Optional[str] = None,  # type: ignore
        link_previews: Iterable[LinkPreview] = (),
        mentions: Optional[list[Mention]] = None,
    ) -> Optional[str]:
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        content = {
            "msgtype": "m.text",
            "body": "* " + text,
            "m.new_content": get_content(text, mentions),
            "m.relates_to": {"rel_type": "m.replace", "event_id": legacy_msg_id},
        }
        await self.__relates_to(chat.legacy_id, content, None, thread)
        return await self.__room_send(chat, content)

    async def on_react(
        self,
        chat: Recipient,
        legacy_msg_id: str,
        emojis: list[str],
        thread: Optional[LegacyThreadType] = None,
    ):
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        new_emojis = set(emojis)
        old_emojis = await self.matrix.reactions.get(
            chat.legacy_id, legacy_msg_id, self.matrix.user_id, with_event_ids=True
        )
        for old_emoji, event in old_emojis.items():
            if old_emoji in new_emojis:
                new_emojis.remove(old_emoji)
            else:
                await self.on_retract(chat, event)
                self.matrix.reactions.remove(event)
        for emoji in new_emojis:
            content = {
                "m.relates_to": {
                    "rel_type": "m.annotation",
                    "event_id": legacy_msg_id,
                    "key": emoji,
                },
            }

            i = await self.__room_send(chat, content, "m.reaction")
            await self.matrix.reactions.add(
                chat.legacy_id, legacy_msg_id, self.matrix.user_id, emoji, i
            )

    async def on_retract(
        self,
        chat: Recipient,
        legacy_msg_id: str,
        thread: Optional[str] = None,  # type: ignore
    ):
        if isinstance(chat, Contact):
            raise XMPPError("bad-request", "Matridge does not implement 1:1 chats")
        resp = await self.matrix.room_redact(chat.legacy_id, legacy_msg_id)
        self.log.debug("Redact response: %s", resp)
        if isinstance(resp, nio.RoomRedactError):
            raise XMPPError("internal-server-error", str(resp))
        assert isinstance(resp, nio.RoomRedactResponse)
        self.events_to_ignore.add(resp.event_id)

    async def on_presence(
        self,
        resource: str,
        show: PseudoPresenceShow,
        status: str,
        resources: dict[str, ResourceDict],
        merged_resource: Optional[ResourceDict],
    ):
        if not merged_resource:
            resp = await self.matrix.set_presence("offline")
        else:
            resp = await self.matrix.set_presence(
                PRESENCE_DICT[merged_resource["show"]],
                merged_resource["status"] or None,
            )
        self.log.debug("Set presence response: %s", resp)

    async def on_avatar(
        self,
        bytes_: Optional[bytes],
        hash_: Optional[str],
        type_: Optional[str],
        width: Optional[int],
        height: Optional[int],
    ) -> None:
        if bytes_:
            resp, _ = await self.matrix.upload(io.BytesIO(bytes_), type_)
            self.log.debug("Upload response: %s %r", type(resp), resp)
            if not isinstance(resp, nio.UploadResponse):
                raise XMPPError("internal-server-error", str(resp))
            uri = resp.content_uri
        else:
            uri = ""
        await self.matrix.set_avatar(uri)


PRESENCE_DICT: dict[PseudoPresenceShow, str] = {
    "": "online",
    "chat": "online",
    "away": "unavailable",
    "xa": "unavailable",
    "dnd": "unavailable",
}
