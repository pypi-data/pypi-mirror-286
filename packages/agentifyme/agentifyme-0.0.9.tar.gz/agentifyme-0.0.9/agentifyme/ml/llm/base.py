from typing import Any, Dict, Optional, Protocol, Union, Iterable, overload, List, Tuple
from enum import Enum

from openai import BaseModel
from agentifyme.cache import cache, CacheType
from pytest import Cache


class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"
    FUNCTION = "function"


class LLMFunctionCall(BaseModel):
    name: str
    arguments: Optional[Dict[str, Any]]


class LLMTokenUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cost: float = 0.0
    calls: int = 0


class LLMMessage(BaseModel):

    role: Role
    content: Optional[str] = None
    tool_id: Optional[str] = None
    function_call: Optional[LLMFunctionCall] = None


class LLMCacheType(str, Enum):
    MEMORY = "memory"
    DISK = "disk"
    NONE = "none"


class LLMResponse(BaseModel):
    """
    Class representing response from LLM.
    """

    message: Optional[str] = None
    role: Role = Role.ASSISTANT
    tool_id: str = ""  # used by OpenAIAssistant
    function_call: Optional[LLMFunctionCall] = None
    usage: Optional[LLMTokenUsage] = None
    cached: bool = False
    error: Optional[str] = None


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    COHERE = "cohere"


class LLMModel(str, Enum):
    OPENAI_GPT3_5_TURBO = "openai/gpt3-5-turbo"
    OPENAI_GPT4 = "openai/gpt-4"
    OPENAI_GPT4_32K = "openai/gpt-4-32k"
    OPENAI_GPT4o = "openai/gpt-4o"


class LLM(Protocol):

    llm_model: LLMModel
    llm_cache_type: LLMCacheType

    def generate(
        self,
        messages: List[LLMMessage],
        tools: List[LLMFunctionCall],
        max_tokens: int = 256,
        temperature: float = 0.5,
        **kwargs,
    ) -> LLMResponse: ...


class BaseLLM(LLM):

    def __init__(
        self,
        llm_model: LLMModel,
        llm_cache_type: LLMCacheType,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> None:
        self.llm_model = llm_model
        self.llm_cache_type = llm_cache_type

        self.system_prompt = "You are an helpful assistant"
        if system_prompt is not None:
            self.system_prompt = system_prompt

    def get_model_name(self, llm_model: LLMModel) -> Tuple[str, str]:
        if "/" not in llm_model:
            raise ValueError(f"Invalid LLM model name: {llm_model}")

        provider, model_name = llm_model.split("/")
        return (provider, model_name)

    @cache(cache_type=CacheType.DISK)
    def generate_from_prompt(self, prompt: str) -> LLMResponse:
        """Generate response from a prompt."""

        llm_messages = [
            LLMMessage(
                role=Role.SYSTEM,
                content=self.system_prompt,
                function_call=None,
            ),
            LLMMessage(role=Role.USER, content=prompt, function_call=None),
        ]
        return self.generate(llm_messages, [])

    def generate_from_messages(self, messages: List[LLMMessage]) -> LLMResponse:
        """Generate response from a list of messages."""

        return self.generate(messages, [])
