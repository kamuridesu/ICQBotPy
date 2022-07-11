from dataclasses import dataclass

@dataclass
class FilePayload:
    file_id: str
    type: str


@dataclass
class StickerPayload(FilePayload):
    file_id: str


@dataclass
class VoicePayload(FilePayload):
    file_id: str


@dataclass
class MentionPayload:
    user_id: str
    first_name: str
    last_name: str = ""
    nickname: str = ""