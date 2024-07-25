import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage
from whoi_nlu_server_messages.Vector3Message import Vector3Message

@dataclasses.dataclass
class CustomMarkerArrayMessage(CBorMessage):
    header: HeaderMessage
    size: int
    scale: Vector3Message
    points: list
    colors: list 