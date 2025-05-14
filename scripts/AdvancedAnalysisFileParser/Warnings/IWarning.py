from abc import ABC, abstractmethod
from ..Models import JsonDict

class IWarning(ABC):
    @abstractmethod
    def format(self, config: JsonDict, data: JsonDict) -> str:
        pass
