from dataclasses import dataclass
from ..ext.util import CustomDict

@dataclass
class FilePayload(CustomDict):
    file_id: str
    type: str


@dataclass
class StickerPayload(FilePayload):
    file_id: str


@dataclass
class VoicePayload(FilePayload):
    file_id: str


@dataclass
class MentionPayload(CustomDict):
    user_id: str
    first_name: str
    last_name: str = ""
    nickname: str = ""