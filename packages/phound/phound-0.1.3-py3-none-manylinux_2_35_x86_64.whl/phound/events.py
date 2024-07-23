import json
import shlex
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum, IntEnum

from phound.logging import logger
from phound import exceptions


class EventType(str, Enum):
    CONNECTED = "connected"
    NEW_CHANNEL = "new_channel"
    CLOSE_CHANNEL = "close_channel"
    ERROR = "error"

    CHAT_MESSAGE = "chat_message"
    CHAT_MESSAGE_SENT = "chat_message_sent"
    CHAT_HISTORY = "chat_history_bulk"
    CHAT_ERROR = "chat_error"

    CALL_INCOMING = "call_incoming"
    CALL_ANSWER = "call_answer"
    CALL_READY = "call_ready"
    AUDIO_CHUNK_RECORDED = "audio_chunk_recorded"
    PLAYBACK_STATUS = "playback_status"
    CALL_HANGUP = "call_hangup"
    CALL_DELAY_COMPLETE = "call_delay_complete"
    CALL_REESTABLISHED = "call_reestablished"
    CALL_ATTENDEE_JOINED = "call_attendee_joined"
    CALL_ATTENDEE_ID_DROP = "call_attendee_id_drop"
    CALL_CHAT_ID_RECEIVED = "call_chat_id_received"

    PHONE_NUMBER_INFO = "phone_number_info"
    UNKNOWN = "unknown"


class PlaybackStatus(str, Enum):
    IN_PROGRESS = "inprogress"
    COMPLETE = "complete"


class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


@dataclass(frozen=True)
class NewChannel:
    id: str

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "NewChannel":
        return cls(id=str(event["headers"]["ChanID"]))


class MetaType(IntEnum):
    UNKNOWN = 0
    CALL = 1
    ATTACHMENT = 2
    QUOTE = 3
    SPC_RECORDING = 4
    CONF_RECORDING = 5


@dataclass(frozen=True)
class MessageAttachment:
    name: str
    size: int
    url: str

    @classmethod
    def from_dict(cls, attachment: Dict[str, Any]) -> "MessageAttachment":
        return cls(
            name=attachment["name"],
            size=attachment["size"],
            url=attachment["publishURI"],
        )


@dataclass(frozen=True)
class Message:
    id: str
    text: str
    from_uid: str
    from_name: str
    tagged: bool
    persona_uid: str
    chat_id: str
    chat_type: ChatType
    attachments: List[MessageAttachment]

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "Message":
        _chat_type_int_to_enum = {
            1: ChatType.PRIVATE,
            2: ChatType.GROUP,
            3: ChatType.GROUP,
            4: ChatType.GROUP,
        }
        headers, body = event["headers"], event["body"]
        return cls(
            id=str(headers["MsgID"]),
            text=body,
            from_uid=str(headers["FromUID"]),
            from_name=headers.get("FromName", ""),
            tagged=headers.get("Tagged", False),
            persona_uid=str(headers["PersonaUID"]),
            chat_id=headers["ChatID"],
            chat_type=_chat_type_int_to_enum[headers["ChatType"]],
            attachments=([MessageAttachment.from_dict(a) for a in json.loads(headers["Meta"]).get("items", [])]
                         if "Meta" in headers and headers.get("MetaType") == MetaType.ATTACHMENT
                         else []),
        )


@dataclass(frozen=True)
class Call:
    id: str
    persona_uid: str
    from_persona_uid: str
    from_name: str

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "Call":
        headers = event["headers"]
        return cls(
            id=str(headers["CallID"]),
            persona_uid=str(headers["LocalUID"]),
            from_persona_uid=str(headers["RemoteUID"]),
            from_name=headers.get("RemoteName", ""),
        )


@dataclass(frozen=True)
class CallAnswer:
    attendee_id: str

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "CallAnswer":
        return cls(str(event["headers"]["AttendieID"]))


@dataclass(frozen=True)
class CallReady:
    attendee_id: str

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "CallReady":
        return cls(str(event["headers"]["AttendieId"]))


@dataclass(frozen=True)
class AudioChunk:
    audio_file_path: str
    asn_file_path: str
    duration: float
    last_chunk: bool
    full_audio_file_path: Optional[str]
    full_duration: Optional[float]

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "AudioChunk":
        headers = event["headers"]
        return cls(
            audio_file_path=headers["AudioFile"],
            asn_file_path=headers["ASNFile"],
            duration=float(headers["Duration"]),
            last_chunk=headers.get("LastChunk", False),
            full_audio_file_path=headers.get("FullAudioFile"),
            full_duration=float(headers["FullDuration"]) if "FullDuration" in headers else None,
        )


@dataclass(frozen=True)
class CallAttendee:
    id: str
    number: str
    name: str
    persona_uid: str

    @classmethod
    def from_tokens(cls, tokens: List[str]) -> "CallAttendee":
        return cls(
            id=tokens[1],
            number=tokens[16],
            name=tokens[17],
            persona_uid=tokens[20],
        )


@dataclass
class PhoneNumberInfo:
    number: str
    uid: str

    @classmethod
    def from_dict(cls, event: Dict[str, Any]) -> "PhoneNumberInfo":
        return cls(
            number=event["headers"]["E164Number"],
            uid=str(event["headers"]["UserID"]),
        )


@dataclass(frozen=True)
class Event:
    type: EventType
    body: Any = None


def parse(string: str) -> Optional[Event]:
    try:
        raw_event = json.loads(string)
    except json.decoder.JSONDecodeError:
        # string is not an event, skipping
        return None

    logger.debug(f"Raw event: {raw_event}")
    event = None
    try:
        raw_event_type = raw_event["headers"]["Event"]
        if raw_event_type == _RawEventType.CONNECTED:
            event = Event(
                type=EventType.CONNECTED,
            )
        elif raw_event_type == _RawEventType.CLOSE_CHANNEL:
            event = Event(
                type=EventType.CLOSE_CHANNEL,
            )
        elif raw_event_type == _RawEventType.NEW_CHANNEL:
            event = Event(
                type=EventType.NEW_CHANNEL,
                body=NewChannel.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.ERROR:
            event = Event(
                type=EventType.ERROR,
                body=raw_event["headers"]["ErrInfo"],
            )
        elif raw_event_type == _RawEventType.CHAT_MESSAGE:
            event = Event(
                type=EventType.CHAT_MESSAGE,
                body=Message.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.CHAT_MESSAGE_SENT:
            event = Event(
                type=EventType.CHAT_MESSAGE_SENT,
                body=Message.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.CHAT_HISTORY_BULK:
            event = Event(
                type=EventType.CHAT_HISTORY,
                body=_build_chat_history(raw_event["body"]),
            )
        elif raw_event_type == _RawEventType.INVALID_CHAT:
            event = Event(
                type=EventType.CHAT_ERROR,
                body=f"invalid chat id: {raw_event['headers']['ChatID']}"
            )
        elif raw_event_type == _RawEventType.CHAT_MESSAGE_FAILED:
            event = Event(
                type=EventType.CHAT_ERROR,
                body=raw_event["headers"]["ErrMessage"],
            )
        elif raw_event_type == _RawEventType.INVALID_PERSONA:
            event = Event(
                type=EventType.CHAT_ERROR,
                body=f"invalid persona id: {raw_event['headers']['PersonaUID']}"
            )
        elif raw_event_type == _RawEventType.CALL_INCOMING:
            event = Event(
                type=EventType.CALL_INCOMING,
                body=Call.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.CALL_ANSWER:
            event = Event(
                type=EventType.CALL_ANSWER,
                body=CallAnswer.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.CONFERENCE_READY:
            event = Event(
                type=EventType.CALL_READY,
                body=CallReady.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.RECORDING_CHUNK:
            event = Event(
                type=EventType.AUDIO_CHUNK_RECORDED,
                body=AudioChunk.from_dict(raw_event),
            )
        elif raw_event_type == _RawEventType.PLAYBACK_STATUS:
            event = Event(
                type=EventType.PLAYBACK_STATUS,
                body=raw_event["headers"]["Status"],
            )
        elif raw_event_type == _RawEventType.CALL_HANGUP:
            event = Event(
                type=EventType.CALL_HANGUP,
            )
        elif raw_event_type == _RawEventType.DELAY_COMPLETE:
            event = Event(
                type=EventType.CALL_DELAY_COMPLETE,
            )
        elif raw_event_type == _RawEventType.CALL_RT:
            event = _parse_call_rt_event(raw_event)
        elif raw_event_type == _RawEventType.PHONE_NUMBER_INFO:
            event = Event(
                type=EventType.PHONE_NUMBER_INFO,
                body=PhoneNumberInfo.from_dict(raw_event),
            )
    except (KeyError, IndexError) as e:
        logger.error(f"Failed to parse raw event {raw_event}: {e}")
        raise exceptions.EventParseError(e)

    return event or Event(type=EventType.UNKNOWN)


def _parse_call_rt_event(raw_event: Dict[str, Any]) -> Optional[Event]:
    tokens = shlex.split(raw_event["body"])
    rt_type = tokens[0]
    event = None
    if rt_type == _RTType.NOTIFY_CONFERENCE:
        event = Event(
            type=EventType.CALL_REESTABLISHED,
        )
    elif rt_type == _RTType.NOTIFY_CHAT_ID:
        event = Event(
            type=EventType.CALL_CHAT_ID_RECEIVED,
            body=tokens[1].upper(),
        )
    elif rt_type == _RTType.NOTIFY_JOIN:
        event = Event(
            type=EventType.CALL_ATTENDEE_JOINED,
            body=CallAttendee.from_tokens(tokens),
        )
    elif rt_type == _RTType.NOTIFY_DROP:
        event = Event(
            type=EventType.CALL_ATTENDEE_ID_DROP,
            body=tokens[1],
        )
    return event


def _build_chat_history(body: str) -> List[Message]:
    return [Message.from_dict(m) for m in json.loads(body)]


class _RawEventType(str, Enum):
    CONNECTED = "Connected"
    NEW_CHANNEL = "NewChannel"
    CLOSE_CHANNEL = "CloseChannel"
    ERROR = "Error"

    CHAT_MESSAGE = "ChatMessage"
    CHAT_MESSAGE_SENT = "ChatMessageSent"
    CHAT_HISTORY_BULK = "ChatHistoryBulk"
    INVALID_CHAT = "InvalidChat"
    CHAT_MESSAGE_FAILED = "ChatMessageFailed"
    INVALID_PERSONA = "InvalidPersona"

    CALL_INCOMING = "CallIncoming"
    CALL_ANSWER = "CallAnswer"
    CONFERENCE_READY = "ConferenceReady"
    RECORDING_CHUNK = "RecordingChunk"
    PLAYBACK_STATUS = "PlaybackStatus"
    CALL_HANGUP = "CallHangup"
    DELAY_COMPLETE = "DelayComplete"
    CALL_RT = "CallRT"

    PHONE_NUMBER_INFO = "PhoneNumberInfo"


class _RTType(str, Enum):
    NOTIFY_CONFERENCE = "NOTIFY-CONFERENCE"
    NOTIFY_CHAT_ID = "NOTIFY-CHAT-ID"
    NOTIFY_JOIN = "NOTIFY-JOIN"
    NOTIFY_DROP = "NOTIFY-DROP"
