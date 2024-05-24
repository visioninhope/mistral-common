from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, List, Optional, TypeVar

from mistral_common.base import MistralBase
from mistral_common.tokens.instruct.request import InstructRequest


class SpecialTokens(str, Enum):
    bos = "<s>"
    eos = "</s>"
    begin_inst = "[INST]"
    end_inst = "[/INST]"
    begin_tools = "[AVAILABLE_TOOLS]"
    end_tools = "[/AVAILABLE_TOOLS]"
    begin_tool_results = "[TOOL_RESULTS]"
    end_tool_results = "[/TOOL_RESULTS]"
    tool_calls = "[TOOL_CALLS]"


class Tokenized(MistralBase):
    """
    A tokenized InstructRequest
    """

    tokens: List[int]
    text: Optional[str] = None


class Tokenizer(ABC):
    @property
    @abstractmethod
    def n_words(self) -> int:
        """Vocabulary size"""

    @abstractmethod
    def vocab(self) -> List[str]:
        """All tokens in the vocabulary as strings"""

    @property
    @abstractmethod
    def bos_id(self) -> int:
        """id of the Beginning of String token"""

    @property
    @abstractmethod
    def eos_id(self) -> int:
        """id of the End of String token"""

    @abstractmethod
    def encode(self, s: str, bos: bool, eos: bool) -> List[int]:
        """String to token ids"""

    @abstractmethod
    def decode(self, t: List[int]) -> str:
        """Token ids to string"""

    @abstractmethod
    def get_control_token(self, s: str) -> int:
        """Get the id of a control token"""

    @abstractmethod
    def to_string(self, tokens: List[int]) -> str:
        """Convert token ids to string"""


InstructRequestType = TypeVar("InstructRequestType", bound=InstructRequest)
TokenizedType = TypeVar("TokenizedType", bound=Tokenized)


class InstructTokenizer(Generic[InstructRequestType, TokenizedType], ABC):
    tokenizer: Tokenizer

    def __init__(self, model_path: str):
        """Init from model file"""

    @abstractmethod
    def encode_instruct(self, request: InstructRequestType) -> TokenizedType:
        """Instruct request to Tokenized object"""

    @abstractmethod
    def decode(self, tokens: List[int]) -> str:
        """Convert token ids to string"""
