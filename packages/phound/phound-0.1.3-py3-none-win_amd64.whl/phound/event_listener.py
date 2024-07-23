from typing import TextIO

from phound import events
from phound.events import EventType, Event
from phound import exceptions


class EventListener:
    def __init__(self, source: TextIO) -> None:
        self._source = source

    def wait_event(self, *event_types: EventType) -> Event:
        event = self._get_next_event()
        self._raise_for_error(event)
        if event_types and event.type not in event_types:
            raise exceptions.UnexpectedEventError(
                f"Unexpected event: {event.type}, expected: {', '.join(event_types)}")
        return event

    def _get_next_event(self) -> Event:
        while True:
            data = self._source.readline()
            if not data:
                raise exceptions.InputError
            event = events.parse(data)
            if event:
                return event

    @staticmethod
    def _raise_for_error(event: Event) -> None:
        if event.type == EventType.ERROR:
            raise exceptions.PhoundError(event.body)
        if event.type == EventType.CHAT_ERROR:
            raise exceptions.ChatError(event.body)
