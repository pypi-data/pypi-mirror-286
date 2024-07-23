import abc
from typing import Any, Dict, List, Optional, cast

from phound.events import (
    AudioChunk,
    Call,
    CallAttendee,
    Event,
    EventType,
    Message,
    PlaybackStatus,
    PhoneNumberInfo,
)
from phound.event_listener import EventListener
from phound.logging import logger
from phound.client import Client
from phound.server import Connection
from phound.chats.utils import get_chat_id, parse_attachments, extract_mentions
from phound.chats.text_helpers import MessageTextFormat
from phound.exceptions import ChatError


class Chat:
    def __init__(
        self, persona_uid: str, chat_id: str, channel_id: str, client: Client, event_listener: EventListener
    ) -> None:
        self.persona_uid = persona_uid
        self.chat_id = chat_id
        self._channel_id = channel_id
        self._client = client
        self._event_listener = event_listener

    def send_message(
        self,
        text: str,
        text_format: MessageTextFormat = MessageTextFormat.PLAIN,
        attachments: Optional[List[str]] = None,
        app_meta: Optional[Dict[str, Any]] = None,
        chat_id: str = "",
        persona_uid: str = "",
        phone_number: str = "",
    ) -> Message:
        text, mentions = extract_mentions(text, text_format)
        self._client.send_message(self.persona_uid,
                                  self._get_chat_id(chat_id, persona_uid, phone_number),
                                  text,
                                  text_format=text_format,
                                  attachments=parse_attachments(attachments) if attachments else None,
                                  mentions=mentions,
                                  app_meta=app_meta,
                                  channel_id=self._channel_id)
        return self._event_listener.wait_event(EventType.CHAT_MESSAGE_SENT).body

    def show_typing(self, timeout: int = 60, chat_id: str = "", persona_uid: str = "", phone_number: str = "") -> None:
        self._client.show_typing(self.persona_uid,
                                 self._get_chat_id(chat_id, persona_uid, phone_number),
                                 timeout,
                                 self._channel_id)

    def get_history(
        self,
        depth: int = 10,
        start_message_id: str = "0",
        chat_id: str = "",
        persona_uid: str = "",
        phone_number: str = ""
    ) -> List[Message]:
        self._client.request_chat_history(self.persona_uid,
                                          self._get_chat_id(chat_id, persona_uid, phone_number),
                                          start_message_id,
                                          self._channel_id,
                                          depth)
        return self._event_listener.wait_event(EventType.CHAT_HISTORY).body

    def _get_chat_id(self, chat_id: str, persona_uid: str, phone_number: str) -> str:
        if chat_id:
            to_chat_id = chat_id
        elif persona_uid:
            to_chat_id = get_chat_id(self.persona_uid, persona_uid)
        elif phone_number:
            self._client.lookup_phone_number(phone_number, self._channel_id)
            phone_number_info = cast(
                PhoneNumberInfo, self._event_listener.wait_event(EventType.PHONE_NUMBER_INFO).body)
            to_chat_id = get_chat_id(self.persona_uid, phone_number_info.uid)
        else:
            to_chat_id = self.chat_id
        if not to_chat_id:
            raise ChatError("chat_id or persona_uid or phone_number must be provided")
        return to_chat_id


class BaseHandler(metaclass=abc.ABCMeta):
    def __init__(self, channel_id: str, conn: Connection, client: Client) -> None:
        self._channel_id = channel_id
        self._event_listener = EventListener(conn.file)
        self._client = client
        self._is_active = True

    def start(self, start_event: Event) -> None:
        self._handle_event(start_event)
        while self._is_active:
            self._client.request_next_event(self._channel_id)
            event = self._event_listener.wait_event()
            if event.type == EventType.UNKNOWN:
                # unknown type is a temporary workaround, ideally event listener should always wait for known event
                # but in channel mode it might be hard to request the next one since some events requested
                # explicitly whereas others are not
                continue
            logger.info(f"Got new event in channel with id {self._channel_id}: {event}")
            if event.type == EventType.CLOSE_CHANNEL:
                self._is_active = False
            else:
                self._handle_event(event)
        logger.info(f"Channel with id {self._channel_id} closed")

    @abc.abstractmethod
    def _handle_event(self, event: Event) -> None:
        pass


class BaseChatHandler(BaseHandler, Chat):
    _SYSTEM_MESSAGE_FROM_UID = "0"

    def __init__(
        self,
        chat_id: str,
        persona_uid: str,
        chat_type: str,
        channel_id: str,
        conn: Connection,
        client: Client
    ) -> None:
        super().__init__(channel_id, conn, client)
        self.persona_uid = persona_uid
        self.chat_type = chat_type
        self.chat_id = chat_id

    def on_message(self, message: Message) -> None:
        pass

    def _handle_event(self, event: Event) -> None:
        if event.type == EventType.CHAT_MESSAGE:
            message = event.body
            if message.from_uid in (self.persona_uid, self._SYSTEM_MESSAGE_FROM_UID):
                self._is_active = False
            else:
                self.on_message(message)


class BaseCallHandler(BaseHandler):
    _CALL_DELAY_TIME_MILLISECONDS = 1000

    def __init__(
        self, call_id: str, persona_uid: str, channel_id: str, conn: Connection, client: Client
    ) -> None:
        super().__init__(channel_id, conn, client)
        self.persona_uid = persona_uid
        self.chat = Chat(persona_uid, "", channel_id, client, self._event_listener)
        self._call_id = call_id
        self._delayed_event: Optional[Event] = None
        self._all_attendees: Dict[str, CallAttendee] = {}
        self._active_attendees: Dict[str, CallAttendee] = {}

    def on_incoming_call(self, call: Call) -> None:
        pass

    def on_call_ready(self) -> None:
        pass

    def on_playback_status(self, status: PlaybackStatus) -> None:
        pass

    def on_audio_chunk_recorded(self, audio_chunk: AudioChunk) -> None:
        pass

    def on_hangup(self) -> None:
        pass

    def on_attendee_join(self, attendee: CallAttendee) -> None:
        pass

    def on_attendee_drop(self, attendee: CallAttendee) -> None:
        pass

    def answer(self) -> None:
        self._client.answer_call(self._call_id)

    def reject(self) -> None:
        self._intentionally_end_call()

    def play(self, file_path: str) -> None:
        self._client.play_file(self._call_id, file_path)

    def record(self, file_path: str) -> None:
        self._client.record_call(self._call_id, file_path)

    def hangup(self) -> None:
        self._intentionally_end_call()

    def get_active_attendees(self) -> List[CallAttendee]:
        return list(self._active_attendees.values())

    def get_all_attendees(self) -> List[CallAttendee]:
        return list(self._all_attendees.values())

    def _handle_event(self, event: Event) -> None:
        delayed = False
        if event.type == EventType.CALL_DELAY_COMPLETE and self._delayed_event:
            event = self._delayed_event
            delayed = True

        if event.type == EventType.CALL_INCOMING:
            self.on_incoming_call(event.body)
        elif event.type == EventType.CALL_READY:
            if delayed:
                self.on_call_ready()
            else:
                self._delay(event)
        elif event.type == EventType.CALL_REESTABLISHED:
            self._all_attendees = {}
            self._active_attendees = {}
            self.chat.chat_id = ""
        elif event.type == EventType.CALL_ATTENDEE_JOINED:
            attendee = event.body
            self._all_attendees[attendee.id] = attendee
            self._active_attendees[attendee.id] = attendee
            if attendee.persona_uid != self.persona_uid:
                self.on_attendee_join(attendee)
        elif event.type == EventType.CALL_ATTENDEE_ID_DROP:
            attendee_id = event.body
            attendee = self._active_attendees.pop(attendee_id, None)
            if attendee:
                self.on_attendee_drop(attendee)
        elif event.type == EventType.CALL_CHAT_ID_RECEIVED:
            self.chat.chat_id = event.body
        elif event.type == EventType.PLAYBACK_STATUS:
            self.on_playback_status(event.body)
        elif event.type == EventType.AUDIO_CHUNK_RECORDED:
            self.on_audio_chunk_recorded(event.body)
        elif event.type == EventType.CALL_HANGUP:
            self._is_active = False
            self.on_hangup()

    def _delay(self, event: Event) -> None:
        self._delayed_event = event
        self._client.delay_call(self._call_id, self._CALL_DELAY_TIME_MILLISECONDS)

    def _intentionally_end_call(self) -> None:
        self._client.hangup(self._call_id)
        # avoid calling on_hangup if call ended intentionally
        self._client.request_next_event(self._channel_id)
        self._event_listener.wait_event(EventType.CALL_HANGUP)
        self._is_active = False
