from mistral_common.protocol.instruct.messages import (
    AssistantMessage,
    UserMessage,
    ToolMessage,
)
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from mistral_common.protocol.instruct.tool_calls import (
    Function as MistralFunction,
    Tool,
    ToolCall,
    FunctionCall,
)
from mistral_common.protocol.instruct.request import ChatCompletionRequest

from openai.types.chat import (
    ChatCompletionMessage,
    ChatCompletionMessageToolCall,
    ChatCompletion,
)
from openai.types.chat.chat_completion_message_tool_call import Function
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    ChoiceDeltaToolCall,
    ChoiceDelta,
    ChoiceDeltaToolCallFunction,
    Choice as Choice_Chunk,
)
from openai.types.completion_usage import CompletionUsage
from openai.types.chat.chat_completion import Choice
from openai import OpenAI, AsyncOpenAI
from typing import List, Dict, Any, Union, Tuple

import json
import re
import time
import uuid 
import ast

from vector_store import add_tool_to_vector_store, summarize_user_messages_into_query,get_tool_from_vector_store

#GLOBAL CONFIG 

MODEL_NAME='open-mixtral-8x22b'


# Define your desired output structure

SUPPORTED_MODELS=['ScaleGenAI/mixtral-8x7-function-calling-v2']


def build_system_prompt(predefined_prompt:str,tools: List[Dict[str, Any]]) -> str:
    if not predefined_prompt:
        system_prompt = "You are a tool calling agent with access to the following tools:\n"
    else:
        system_prompt = predefined_prompt+"\n"

   #system_prompt += "Don't make up any tools , always use the tools from below list to achieve the task\n"

    for tool in tools:
        tool_name = tool["function"]["name"]
        tool_description = tool["function"]["description"]
        system_prompt += f"{tool_name}: {tool_description}\n"
        
        # Parameters info
        for param_name, param_info in tool["function"]["parameters"]["properties"].items():
            param_title = param_info.get("title", param_name)
            param_type = param_info.get("type", "unknown")
            system_prompt += f" - {param_name} ({param_type}): {param_title}\n"
            
            # If the parameter has a reference to $defs, include the definitions
            if "$ref" in param_info:
                ref = param_info["$ref"].split("/")[-1]
                if ref in tool["function"]["parameters"]["$defs"]:
                    defs_info = tool["function"]["parameters"]["$defs"][ref]
                    system_prompt += f"   Definitions for {ref}:\n"
                    for def_param_name, def_param_info in defs_info["properties"].items():
                        def_param_title = def_param_info.get("title", def_param_name)
                        def_param_type = def_param_info.get("type", "unknown")
                        system_prompt += f"   - {def_param_name} ({def_param_type}): {def_param_title}\n"
                        if "enum" in def_param_info:
                            system_prompt += f"     Allowed values: {def_param_info['enum']}\n"
        system_prompt+="\n"
    return system_prompt


def parse_tool_response(response):
    """
    Parses a tool response string and extracts a list of dictionaries for tools.
    
    Args:
    response (str): The string response containing tool information.
    
    Returns:
    list: A list of dictionaries for the tools extracted from the response.
    """
    try:
        # Step 1: Use regex to extract the JSON-like part
        match = re.search(r'\[.*\]', response, re.DOTALL)
        if not match:
            return "No valid JSON-like structure found in the response"
        
        json_str = match.group()
        
        # Step 2: Use ast.literal_eval to safely evaluate the string
        tool_response = ast.literal_eval(json_str)
        
        # Ensure the result is a list of dictionaries
        if isinstance(tool_response, list) and all(isinstance(d, dict) for d in tool_response):
            return tool_response
        else:
            return "Parsed response is not a list of dictionaries"
    
    except (ValueError, SyntaxError) as e:
        return f"Error parsing the response: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def convert_to_mixtral_tool_result(tool_name:str,content:str) -> str:
    """
    Converts a tool result content to a Mixtral tool result content.
    """
    return f"TOOL_RESULT : [{tool_name} : {content}]"

def convert_to_mixtral_tool_response(tool_name:str,tool_args:str) -> str:
    """
    Converts a tool response content to a Mixtral tool response content.
    """
    dict_response={'tool_name':tool_name,'arguments':tool_args}
    return f"TOOL_RESPONSE : [{dict_response}]"

def convert_to_mixtral_tool_response_multiple(tool_calls:List[Dict[str, Any]]) -> str:
    """
    Converts a tool response content to a Mixtral tool response content.
    """
    tool_call_array=[]
    for tool_call in tool_calls:
        tool_name=tool_call['function']['name']
        tool_args=tool_call['function']['arguments']
        dict_response={'tool_name':tool_name,'arguments':tool_args}
        tool_call_array.append(dict_response)

    return f"TOOL_RESPONSE : {tool_call_array}"


def transform_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """
    Transforms a list of messages into a list of messages in mixtral format,
    combining all tool results into a single array within one TOOL_RESULT entry.
    """
    transformed_messages = []
    tool_results = []
    
    for i, msg in enumerate(messages):
        if isinstance(msg, ChatCompletionMessage):
            if not msg.content and msg.tool_calls:
                if isinstance(msg.tool_calls[0], ChatCompletionMessageToolCall):
                    tool_calls = []
                    for tool_call in msg.tool_calls:
                        tool_calls.append({"function": {"name": tool_call.function.name, "arguments": tool_call.function.arguments}})
                    tool_response = convert_to_mixtral_tool_response_multiple(tool_calls)
                    transformed_messages.append({"content": tool_response, "role": "assistant"})
            elif msg.content:
                transformed_messages.append({"content": msg.content, "role": "assistant"})
        
        elif msg.get("role") == "tool":
            content = msg.get("content")
            
            try:
                tool_result = {"result":json.loads(content)}
            except json.JSONDecodeError:
                tool_result = {"result":content}
            tool_results.append(tool_result)
            
            # If this is the last message or the next message is not a tool response,
            # add the accumulated tool results as a single user message
            if i == len(messages) - 1 or messages[i+1].get("role") != "tool":
                merged_tool_results = f"TOOL_RESULT : {json.dumps(tool_results)}"
                transformed_messages.append({"content": merged_tool_results, "role": "user"})
                tool_results = []  # Reset tool_results for the next set
        
        elif msg.get("role") == "assistant" and isinstance(msg.get("content"), Function):
            function_content = msg["content"]
            function_name = function_content.name
            function_args = function_content.arguments
            tool_response = convert_to_mixtral_tool_response(function_name, function_args)
            transformed_messages.append({"content": tool_response, "role": "assistant"})
        
        elif msg.get("role") == "assistant" and not msg.get("content"):
            tool_calls = msg.get("tool_calls")
            tool_response = convert_to_mixtral_tool_response_multiple(tool_calls)
            transformed_messages.append({"content": tool_response, "role": "assistant"})
        
        elif msg.get("role") == "assistant" and isinstance(msg.get("content"), ChatCompletionMessage):
            content = msg.get("content")
            if not content.content:
                tool_calls = content.tool_calls
                tool_response = convert_to_mixtral_tool_response_multiple(tool_calls)
                transformed_messages.append({"content": tool_response, "role": "assistant"})
            else:
                transformed_messages.append({"content": content.content, "role": "assistant"})
        
        else:
            transformed_messages.append(msg)

    return transformed_messages





def get_chat_completions_tool_calls(tool_calls: List[Dict[str, Any]],model_name:str) -> List[ChatCompletionMessageToolCall]:
    """
    Converts a list of tool calls into a list of ChatCompletionMessageToolCall objects.

    Args:
        tool_calls (list): A list of tool calls.

    Returns:
        list: A list of ChatCompletionMessageToolCall objects.
    """
    chat_completion_tool_calls = []
    for tool_call in tool_calls:

        tool_name = tool_call['tool_name']
        tool_args = tool_call['arguments']
        tool_args=json.dumps(tool_args)
        chat_completion_tool_call = ChatCompletionMessageToolCall(
            id=str(uuid.uuid4()),
            function=Function(name=tool_name, arguments=tool_args),
            type="function",
        )
        chat_completion_tool_calls.append(chat_completion_tool_call)

    
    message=ChatCompletionMessage(
        content=None, role="assistant", tool_calls=chat_completion_tool_calls
    )
    return ChatCompletion(
        id=str(uuid.uuid4()),
        choices=[
            Choice(
                finish_reason="tool_calls",
                index=0,
                logprobs=None,
                message=message,
            )
        ],
        created=int(time.time()),
        model=model_name,
        object="chat.completion",
        system_fingerprint=None,
        usage=CompletionUsage(
            completion_tokens=0,  # Assuming no tokens used for simplicity
            prompt_tokens=0,  # Assuming no tokens used for simplicity
            total_tokens=0,  # Assuming no tokens used for simplicity
        ),
    )


class MistralOpenAIClient(OpenAI):

    def __init__(self, client):
        super().__init__(api_key=client.api_key)
        self.client = client

        if isinstance(client, OpenAI):
            self.chat.completions.create = self.chat_completion

        if isinstance(client, AsyncOpenAI):
            self.chat.completions.create = self.chat_completion_async

    async def chat_completion_async(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]] = [],
        tool_choice: Union[str, Dict[str, Any]] = "auto",
        *args,
        **kwargs,
    ):

        if kwargs.get('stream') == True:
            raise Warning("stream is not supported by the MistralOpenAiClient,if you want to use tools use with stream as False")
        
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"Model {model} is not supported by the MistralOpenAiClient, currently supported models are {SUPPORTED_MODELS}")
      
        tools_added=add_tool_to_vector_store('tools',tools)
        if tools_added:
            #query = summarize_user_messages_into_query(messages,self.client,model,tools)
            query = messages[-1]['content']
            tool_names=get_tool_from_vector_store('tools',query)

            filtered_tools=[]
            for tool in tools:
                if tool['function']['name'] in tool_names:
                    filtered_tools.append(tool)
      
            if messages[0]["role"] == "system":
                system_prompt = messages[0]["content"]
                system_prompt_with_tools = build_system_prompt(system_prompt, filtered_tools)
                messages[0]["content"] = system_prompt_with_tools
            else:
                system_prompt_with_tools = build_system_prompt("", tools)
                messages.insert(0, {"role": "system", "content": system_prompt_with_tools})
        else:
            if messages[0]["role"] == "system":
                system_prompt = messages[0]["content"]
                system_prompt_with_tools = build_system_prompt(system_prompt, tools)
                messages[0]["content"] = system_prompt_with_tools
            else:
                system_prompt_with_tools = build_system_prompt("", tools)
                messages.insert(0, {"role": "system", "content": system_prompt_with_tools})
                
        
        if tool_choice != "auto":
            last_message = messages[-1]
            tool = tool_choice['function']['name']
            if last_message["role"] == "user":
                content = last_message["content"]
                content += f'\n use the tool , {tool} to complete the task'
                messages[-1]["content"] = content

        messages = transform_messages(messages)

        out = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            *args,
            **kwargs,
        )
        response = out.choices[0].message.content

        tool_calls = parse_tool_response(response)
        
        if tool_calls:
            chat_completion_tool_calls = get_chat_completions_tool_calls(tool_calls, model)
            return chat_completion_tool_calls
        else:
            return out

    def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]] = [],
        tool_choice: Union[str, Dict[str, Any]] = "auto",
        *args,
        **kwargs,
    ):

        
        

        
        if kwargs.get('stream') == True:
            raise Warning("stream is not supported by the MistralOpenAiClient,if you want to use tools use with stream as False")
                
        if model not in SUPPORTED_MODELS:
            raise ValueError(f"Model {model} is not supported by the MistralOpenAiClient, currently supported models are {SUPPORTED_MODELS}")
        

        tools_added=add_tool_to_vector_store('tools',tools)
        if tools_added:
            #query = summarize_user_messages_into_query(messages,self.client,model,tools)
            query = messages[-1]['content']
            tool_names=get_tool_from_vector_store('tools',query)

            filtered_tools=[]
            for tool in tools:
                if tool['function']['name'] in tool_names:
                    filtered_tools.append(tool)
      
            if messages[0]["role"] == "system":
                system_prompt = messages[0]["content"]
                system_prompt_with_tools = build_system_prompt(system_prompt, filtered_tools)
                messages[0]["content"] = system_prompt_with_tools
            else:
                system_prompt_with_tools = build_system_prompt("", tools)
                messages.insert(0, {"role": "system", "content": system_prompt_with_tools})
        else:
            if messages[0]["role"] == "system":
                system_prompt = messages[0]["content"]
                system_prompt_with_tools = build_system_prompt(system_prompt, tools)
                messages[0]["content"] = system_prompt_with_tools
            else:
                system_prompt_with_tools = build_system_prompt("", tools)
                messages.insert(0, {"role": "system", "content": system_prompt_with_tools})

        if tool_choice!="auto":
            last_message = messages[-1]
            tool=tool_choice['function']['name']
            if last_message["role"] == "user":
                content=last_message["content"]
                content+=f'\n use the tool , {tool} to complete the task'
                messages[-1]["content"]=content

        messages=transform_messages(messages)

        

        out=self.client.chat.completions.create(
            model=model,
            messages=messages,
            *args,
            **kwargs,
        )


      
        response=out.choices[0].message.content

        
        
        tool_calls = parse_tool_response(response)
        
        if tool_calls and type(tool_calls)==list:
            chat_completion_tool_calls = get_chat_completions_tool_calls(tool_calls,model)
            return chat_completion_tool_calls
        else:
            return out
    