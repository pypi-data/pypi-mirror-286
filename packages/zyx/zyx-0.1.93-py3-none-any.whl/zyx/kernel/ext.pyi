# zyx ==============================================================================

from semantic_kernel.kernel import Kernel as Kernel_type
from semantic_kernel.connectors.ai.ollama import OllamaChatCompletion as OllamaChatCompletion_type
from semantic_kernel.connectors.ai.ollama import OllamaTextEmbedding as OllamaTextEmbedding_type
from semantic_kernel.connectors.ai.ollama import OllamaPromptExecutionSettings as OllamaPromptExecutionSettings_type
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion as OpenAIChatCompletion_type
from semantic_kernel.connectors.ai.open_ai import OpenAITextEmbedding as OpenAITextEmbedding_type
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings as OpenAIPromptExecutionSettings_type
from semantic_kernel.contents.chat_history import ChatHistory as ChatHistory_type
from semantic_kernel.contents.chat_message_content import ChatMessageContent as ChatMessageContent_type
from semantic_kernel.contents.function_call_content import FunctionCallContent as FunctionCallContent_type
from semantic_kernel.contents.streaming_chat_message_content import StreamingChatMessageContent as StreamingChatMessageContent_type 
from semantic_kernel.functions.kernel_function import KernelFunction as KernelFunction_type
from semantic_kernel.functions.kernel_arguments import KernelArguments as KernelArguments_type
from semantic_kernel.functions.kernel_function_decorator import kernel_function as kernel_function_type
from semantic_kernel.functions.kernel_function_extension import KernelFunctionExtension as KernelFunctionExtension_type
from semantic_kernel.agents.chat_completion_agent import ChatCompletionAgent as ChatCompletionAgent_type
from semantic_kernel.agents.agent import Agent as Agent_type

Kernel = Kernel_type
OllamaChatCompletion = OllamaChatCompletion_type
OllamaTextEmbedding = OllamaTextEmbedding_type
OllamaPromptExecutionSettings = OllamaPromptExecutionSettings_type
OpenAIChatCompletion = OpenAIChatCompletion_type
OpenAITextEmbedding = OpenAITextEmbedding_type
OpenAIPromptExecutionSettings = OpenAIPromptExecutionSettings_type
ChatHistory = ChatHistory_type
ChatMessageContent = ChatMessageContent_type
FunctionCallContent = FunctionCallContent_type
StreamingChatMessageContent = StreamingChatMessageContent_type
KernelFunction = KernelFunction_type
KernelArguments = KernelArguments_type
kernel_function = kernel_function_type
KernelFunctionExtension = KernelFunctionExtension_type
ChatCompletionAgent = ChatCompletionAgent_type
Agent = Agent_type