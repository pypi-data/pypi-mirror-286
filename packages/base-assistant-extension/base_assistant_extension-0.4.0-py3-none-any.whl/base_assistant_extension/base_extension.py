from abc import ABC, abstractmethod
from typing import TypedDict
from langchain_core.runnables import Runnable
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


class ExtensionInput(TypedDict):
    messages: list[BaseMessage]


class BaseExtension(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        """
        Will be used by LLM for tool calling selection.
        It's prefered to have a relevant description
        """
        pass

    @abstractmethod
    def create_runnable(self, llm: BaseChatModel) -> Runnable:
        pass
