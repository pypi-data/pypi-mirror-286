from abc import ABC, abstractmethod
from typing import AsyncIterator, TypedDict
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, BaseMessageChunk


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
    async def astream(
        self, llm: BaseChatModel, input: ExtensionInput
    ) -> AsyncIterator[BaseMessageChunk]:
        pass

    @abstractmethod
    async def ainvoke(self, llm: BaseChatModel, input: ExtensionInput) -> BaseMessage:
        pass
