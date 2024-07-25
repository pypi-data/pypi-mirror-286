from abc import ABC, abstractmethod
from typing import TypedDict
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage


class ExtensionInput(TypedDict):
    messages: list[BaseMessage]


class ExtensionOutput(TypedDict):
    response: BaseMessage


class BaseExtension(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def astream(
        self, llm: BaseChatModel, input: ExtensionInput
    ) -> ExtensionOutput:
        pass

    @abstractmethod
    async def ainvoke(
        self, llm: BaseChatModel, input: ExtensionInput
    ) -> ExtensionOutput:
        pass
