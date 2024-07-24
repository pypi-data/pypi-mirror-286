import os
import hashlib
from typing import List, Literal, Optional, overload, Union

from joblib import Memory

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionMessageParam,
    ChatCompletion,
)

from .base import (
    BaseLLM,
    LLMCacheType,
    LLMMessage,
    LLMModel,
    LLMProvider,
    LLMResponse,
    LLMTokenUsage,
    LLMFunctionCall,
    Role,
)


def llm_cache_key(model_name, llm_messages, tools):
    raw_key = model_name
    if len(llm_messages) > 0:
        raw_key = raw_key + str(llm_messages)

    if len(tools) > 0:
        raw_key = raw_key + str(tools)

    hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()
    return hashed_key


class LLMCacheJoblib(Memory):
    def _cache_key(self, func, *args, **kwargs):
        model_name, llm_messages, tools = args
        return llm_cache_key(model_name, llm_messages, tools)


class OpenAILLM(BaseLLM):

    def __init__(
        self,
        llm_model: LLMModel,
        api_key: Optional[str] = None,
        llm_cache_type: LLMCacheType = LLMCacheType.NONE,
        system_prompt: Optional[str] = None,
        api_base_url: Optional[str] = None,
        organization: Optional[str] = None,
        timeout: Optional[int] = None,
        max_retries: int = 2,
        **kwargs,
    ) -> None:

        super().__init__(
            llm_model, llm_cache_type, system_prompt=system_prompt, **kwargs
        )

        _api_key = os.getenv("OPENAI_API_KEY") if api_key is None else api_key
        if not _api_key:
            raise ValueError("OpenAI API key is required")

        self.api_key = _api_key
        self.client = OpenAI(
            api_key=_api_key,
            base_url=api_base_url,
            organization=organization,
            timeout=timeout,
            max_retries=max_retries,
        )

        self.model = llm_model

        self.llm_cache: Optional[LLMCacheJoblib] = None

        if self.llm_cache_type == LLMCacheType.DISK:
            self.llm_cache = LLMCacheJoblib(location="joblib_cache", verbose=0)
        elif self.llm_cache_type == LLMCacheType.MEMORY:
            self.llm_cache = LLMCacheJoblib(location=None, verbose=0)

    def generate(
        self,
        messages: List[LLMMessage],
        tools: List[LLMFunctionCall],
        max_tokens: int = 256,
        temperature: float = 0.5,
        **kwargs,
    ) -> LLMResponse:
        llm_messages: List[ChatCompletionMessageParam] = []

        for message in messages:
            if message.content is None:
                continue

            if message.role == Role.USER:
                user_message = ChatCompletionUserMessageParam(
                    content=message.content, role="user"
                )
                llm_messages.append(user_message)
            elif message.role == Role.SYSTEM:
                system_message = ChatCompletionSystemMessageParam(
                    content=message.content, role="system"
                )
                llm_messages.append(system_message)
            elif message.role == Role.ASSISTANT:
                assistant_message = ChatCompletionAssistantMessageParam(
                    content=message.content, role="assistant"
                )
                llm_messages.append(assistant_message)
            else:
                raise ValueError(f"Invalid role: {message.role}")

        provider, model_name = self.get_model_name(self.model)

        assert provider == LLMProvider.OPENAI, f"Invalid provider: {provider}"

        if self.llm_cache is not None:
            response = self.llm_cache.cache(self._call_openai)(model_name, llm_messages)
        else:
            response = self._call_openai(model_name, llm_messages)

        usage = None
        if response.usage:
            usage = LLMTokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                cost=0.0,
                calls=1,
            )

        llm_response = LLMResponse(
            message=response.choices[0].message.content,
            role=Role.ASSISTANT,
            tool_id="",
            function_call=None,
            usage=usage,
            cached=False,
            error=None,
        )

        return llm_response

    def _call_openai(
        self, model_name: str, llm_messages: List[ChatCompletionMessageParam]
    ) -> ChatCompletion:
        response = self.client.chat.completions.create(
            model=model_name, messages=llm_messages
        )
        return response
