import uuid
from dataclasses import dataclass, field

@dataclass
class InitialProject:
    name: str
    description: str
    id: str = field(default_factory=str(uuid.uuid4))