# utils/llm_interface.py
# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage, AIMessage
# from typing import List, Dict, Any, Optional
# import time
# import tiktoken
# import os
#
#
# class LLMInterface:
#     def __init__(self, model_config: Dict[str, Any], model_name: str = None):
#         """
#         Initialize the LLM interface
#         """
#         if model_name and model_name in model_config:
#             config = model_config[model_name]
#         else:
#             # Default to the first model in the config
#             model_name = list(model_config.keys())[0]
#             config = model_config[model_name]
#
#         self.model_name = model_name
#         self.api_key = config["api_key"]
#         self.base_url = config["base_url"]
#         self.model = config["model_name"]
#         self.max_tokens = config.get("max_tokens", 2000)
#         self.temperature = config.get("temperature", 0.7)
#
#         self.llm = ChatOpenAI(
#             model=self.model,
#             temperature=self.temperature,
#             max_tokens=self.max_tokens,
#             openai_api_key=self.api_key,
#             openai_api_base=self.base_url
#         )
#
#         # Initialize token encoder based on model
#         self.encoder = self._get_token_encoder()
#
#         # Token usage tracking
#         self.total_prompt_tokens = 0
#         self.total_completion_tokens = 0
#         self.total_tokens = 0
#
#     def _get_token_encoder(self):
#         """
#         Get the appropriate token encoder for the model
#         """
#         try:
#             # Try to get an OpenAI encoder if possible
#             if "gpt" in self.model.lower():
#                 return tiktoken.encoding_for_model(self.model)
#             else:
#                 # Default to cl100k_base for other models
#                 return tiktoken.get_encoding("cl100k_base")
#         except Exception as e:
#             print(f"Warning: Could not load tiktoken encoder: {e}")
#             # Fallback to a simple approximation
#             return None
#
#     def _count_tokens(self, text: str) -> int:
#         """
#         Count tokens in text
#         """
#         if self.encoder:
#             return len(self.encoder.encode(text))
#         else:
#             # Fallback approximation: ~4 characters per token for English text
#             return len(text) // 4
#
#     def generate(self, system_prompt: str, user_prompt: str, chat_history: List[Dict[str, str]] = None) -> str:
#         """
#         Generate a response from the LLM
#         """
#         messages = [SystemMessage(content=system_prompt)]
#
#         if chat_history:
#             for message in chat_history:
#                 if message["role"] == "user":
#                     messages.append(HumanMessage(content=message["content"]))
#                 elif message["role"] == "assistant":
#                     messages.append(AIMessage(content=message["content"]))
#
#         messages.append(HumanMessage(content=user_prompt))
#
#         # Count prompt tokens
#         prompt_text = system_prompt + "\n"
#         if chat_history:
#             for message in chat_history:
#                 prompt_text += message["content"] + "\n"
#         prompt_text += user_prompt
#
#         prompt_tokens = self._count_tokens(prompt_text)
#
#         # Measure response time
#         start_time = time.time()
#         response = self.llm.invoke(messages)
#         end_time = time.time()
#
#         # Count completion tokens
#         completion_tokens = self._count_tokens(response.content)
#         total_tokens = prompt_tokens + completion_tokens
#
#         # Update token counts
#         self.total_prompt_tokens += prompt_tokens
#         self.total_completion_tokens += completion_tokens
#         self.total_tokens += total_tokens
#
#         print(f"Token usage: {total_tokens} tokens (Prompt: {prompt_tokens}, Completion: {completion_tokens})")
#         print(f"Response time: {end_time - start_time:.2f} seconds")
#
#         return response.content
#
#     def stream(self, system_prompt: str, user_prompt: str, chat_history: List[Dict[str, str]] = None):
#         """
#         Stream a response from the LLM
#         """
#         messages = [SystemMessage(content=system_prompt)]
#
#         if chat_history:
#             for message in chat_history:
#                 if message["role"] == "user":
#                     messages.append(HumanMessage(content=message["content"]))
#                 elif message["role"] == "assistant":
#                     messages.append(AIMessage(content=message["content"]))
#
#         messages.append(HumanMessage(content=user_prompt))
#
#         # Count prompt tokens
#         prompt_text = system_prompt + "\n"
#         if chat_history:
#             for message in chat_history:
#                 prompt_text += message["content"] + "\n"
#         prompt_text += user_prompt
#
#         prompt_tokens = self._count_tokens(prompt_text)
#         self.total_prompt_tokens += prompt_tokens
#
#         # Measure response time
#         start_time = time.time()
#
#         # Buffer for accumulating streamed content
#         full_response = ""
#
#         for chunk in self.llm.stream(messages):
#             chunk_content = chunk.content
#             full_response += chunk_content
#             yield chunk_content
#
#         # Count completion tokens at the end
#         completion_tokens = self._count_tokens(full_response)
#         self.total_completion_tokens += completion_tokens
#         self.total_tokens += prompt_tokens + completion_tokens
#
#         end_time = time.time()
#         print(f"Stream response time: {end_time - start_time:.2f} seconds")
#         print(
#             f"Token usage: {prompt_tokens + completion_tokens} tokens (Prompt: {prompt_tokens}, Completion: {completion_tokens})")
#
#     def get_token_usage(self) -> Dict[str, int]:
#         """
#         Get the current token usage statistics
#         """
#         return {
#             "prompt_tokens": self.total_prompt_tokens,
#             "completion_tokens": self.total_completion_tokens,
#             "total_tokens": self.total_tokens
#         }
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from typing import List, Dict, Any, Optional
import time
import tiktoken


class LLMInterface:
    def __init__(self, model_config: Dict[str, Any], model_name: str = None):
        """
        Initialize the LLM interface
        """
        if model_name and model_name in model_config:
            config = model_config[model_name]
        else:
            # Default to the first model in the config
            model_name = list(model_config.keys())[0]
            config = model_config[model_name]

        self.model_name = model_name
        self.api_key = config["api_key"]
        self.base_url = config["base_url"]
        self.model = config["model_name"]
        self.max_tokens = config.get("max_tokens", 2000)
        self.temperature = config.get("temperature", 0.7)

        self.llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=self.api_key,
            openai_api_base=self.base_url
        )

        # Initialize token encoder based on model
        self.encoder = self._get_token_encoder()

        # Token usage tracking
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0

    def _get_token_encoder(self):
        """
        Get the appropriate token encoder for the model
        """
        try:
            # Try to get an OpenAI encoder if possible
            if "gpt" in self.model.lower():
                return tiktoken.encoding_for_model(self.model)
            else:
                # Default to cl100k_base for other models
                return tiktoken.get_encoding("cl100k_base")
        except Exception as e:
            print(f"Warning: Could not load tiktoken encoder: {e}")
            # Fallback to a simple approximation
            return None

    def _count_tokens(self, text: str) -> int:
        """
        Count tokens in text
        """
        if self.encoder:
            return len(self.encoder.encode(text))
        else:
            # Fallback approximation: ~4 characters per token for English text
            return len(text) // 4

    def generate(self, system_prompt: str, user_prompt: str, chat_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from the LLM
        """
        messages = [SystemMessage(content=system_prompt)]

        if chat_history:
            for message in chat_history:
                if message["role"] == "user":
                    messages.append(HumanMessage(content=message["content"]))
                elif message["role"] == "assistant":
                    messages.append(AIMessage(content=message["content"]))

        messages.append(HumanMessage(content=user_prompt))

        # Count prompt tokens
        prompt_text = system_prompt + "\n"
        if chat_history:
            for message in chat_history:
                prompt_text += message["content"] + "\n"
        prompt_text += user_prompt

        prompt_tokens = self._count_tokens(prompt_text)

        # Measure response time
        start_time = time.time()
        response = self.llm.invoke(messages)
        end_time = time.time()

        # Count completion tokens
        completion_tokens = self._count_tokens(response.content)
        total_tokens = prompt_tokens + completion_tokens

        # Update token counts
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += total_tokens

        print(f"Token usage: {total_tokens} tokens (Prompt: {prompt_tokens}, Completion: {completion_tokens})")
        print(f"Response time: {end_time - start_time:.2f} seconds")

        return response.content

    def stream(self, system_prompt: str, user_prompt: str, chat_history: List[Dict[str, str]] = None):
        """
        Stream a response from the LLM
        """
        messages = [SystemMessage(content=system_prompt)]

        if chat_history:
            for message in chat_history:
                if message["role"] == "user":
                    messages.append(HumanMessage(content=message["content"]))
                elif message["role"] == "assistant":
                    messages.append(AIMessage(content=message["content"]))

        messages.append(HumanMessage(content=user_prompt))

        # Count prompt tokens
        prompt_text = system_prompt + "\n"
        if chat_history:
            for message in chat_history:
                prompt_text += message["content"] + "\n"
        prompt_text += user_prompt

        prompt_tokens = self._count_tokens(prompt_text)
        self.total_prompt_tokens += prompt_tokens

        # Measure response time
        start_time = time.time()

        # Buffer for accumulating streamed content
        full_response = ""

        for chunk in self.llm.stream(messages):
            chunk_content = chunk.content
            full_response += chunk_content
            yield chunk_content

        # Count completion tokens at the end
        completion_tokens = self._count_tokens(full_response)
        self.total_completion_tokens += completion_tokens
        self.total_tokens += prompt_tokens + completion_tokens

        end_time = time.time()
        print(f"Stream response time: {end_time - start_time:.2f} seconds")
        print(
            f"Token usage: {prompt_tokens + completion_tokens} tokens (Prompt: {prompt_tokens}, Completion: {completion_tokens})")

    def get_token_usage(self) -> Dict[str, int]:
        """
        Get the current token usage statistics
        """
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens
        }