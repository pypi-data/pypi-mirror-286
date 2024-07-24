import json
import re
import time
import uuid
from typing import List, Dict, Any, Union, Tuple

from jinja2 import Environment, FileSystemLoader
from openai import OpenAI, AsyncOpenAI
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

from vector_store import add_tool_to_vector_store, get_tool_from_vector_store
import ast





MODEL_NAMES_TYPES= {
    'ScaleGenAI/LLAMA-3-8B-MERGED-FC-CALLING':'latest_tool_version',
    'accounts/kartheek2000mike-d253d7/models/llama-70b-fc-lora-chat':'fireworks',
    'ScaleGenAI/Llama3-70B-Function-Calling':'old_tool_version'

}

def process_messages(messages, add_generation_prompt=True, bos_token="<|begin_of_text|>"):
    env = Environment(loader=FileSystemLoader('.'))
    template = """{% set loop_messages = messages %}{% for message in loop_messages %}{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\n\n'+ message['content'] | trim + '<|eot_id|>' %}{% if loop.index0 == 0 %}{% set content = bos_token + content %}{% endif %}{{ content }}{% endfor %}{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>\n\n' }}{% endif %}"""
    return env.from_string(template).render(messages=messages, add_generation_prompt=add_generation_prompt, bos_token=bos_token)

def extract_constraints(properties, defs):
    constraint_text = ""
    for name, prop in properties.items():
        type_info = prop.get('type', 'unknown type')
        required = ", required" if name in properties.get('required', []) else ""
        enum = ", should be one of [{}]".format(", ".join(prop["enum"])) if prop.get("enum") else ""
        
        items = ""
        if "items" in prop:
            if "$ref" in prop["items"]:
                ref_path = prop["items"]['$ref'].split('/')[-1]
                nested_props = defs.get(ref_path, {})
                items = " with nested properties: \n" + extract_constraints(nested_props.get('properties', {}), defs)
            elif "type" in prop["items"]:
                items = ", each item should be {}".format(prop["items"]["type"])
            else:
                items = ", each item follows a complex structure"

        constraint_text += f"  - {name} ({type_info}{required}): {enum}{items}\n"
    return constraint_text

def generate_json_format_example(parameters, examples):
    if examples:
        return json.dumps(examples[0])
    example_kwargs = {name: "example_value" if param.get("type") not in ["integer", "boolean"] else (1 if param.get("type") == "integer" else True) for name, param in parameters.items()}
    return json.dumps(example_kwargs)

def default_tool_formatter(tools: List[Dict[str, Any]]) -> str:
    tool_text = ""
    tool_names = []
    example_inputs = []
    
    for tool in tools:
        param_text = ""
        parameters = tool["function"]["parameters"]
        for name, param in parameters.get("properties", {}).items():
            required = ", required" if name in parameters.get("required", []) else ""
            enum = ", should be one of [{}]".format(", ".join(param["enum"])) if param.get("enum") else ""
            items = ", where each item should be {}".format(param["items"].get("type", "")) if param.get("items") else ""
            param_text += f"  - {name} ({param.get('type', '')}{required}): {param.get('description', '')}{enum}{items}\n"

        description = tool["function"].get("description", "")
        if description:
            description += 'Ensure the following constraints are met:\n'
            defs = parameters.get('$defs', {})
            tool_constraints = extract_constraints(parameters.get('properties', {}), defs)
            description += '\n' + tool_constraints
        
        tool_text += f"> Tool Name: {tool['function']['name']}\nTool Description: {description}\nTool Args:\n{param_text}\n"
        tool_names.append(tool["function"]["name"])
        example_inputs.append(generate_json_format_example(parameters.get("properties", {}), []))

    if not tool_text:
        return "No tools available."
    
    example_input_text = " or ".join(example_inputs)
    return f"You have access to the following tools:\n{tool_text}Use the following format if using a tool:\nIf a tool errors out or does not return the expected output, please try again with a fixed input.\n```\nAction: tool name (one of [{', '.join(tool_names)}]).\nAction Input: the input to the tool, in a JSON format representing the kwargs (e.g. ```{{'input': 'hello world', 'num_beams': 5}}```)\n```\n"

def default_tool_extractor(content: str) -> Union[str, Tuple[str, str]]:
    regex = re.compile(r"Action:\s*([a-zA-Z0-9_]+).*?Action Input:\s*(.*)", re.DOTALL)
    action_match = re.search(regex, content)
    if not action_match:
        return content
    tool_name = action_match.group(1).strip()
    tool_input = action_match.group(2).strip().strip('"').strip("```")
    try:
        arguments = json.loads(tool_input)
    except json.JSONDecodeError:
        return content
    return tool_name, json.dumps(arguments, ensure_ascii=False)


#llama3 8b code-

def convert_to_llama_tool_response_multiple(tool_calls:List[Dict[str, Any]]) -> str:
    """
    Converts a tool response content to a Mixtral tool response content.
    """
    tool_call_array=[]
    for tool_call in tool_calls:
        tool_name=tool_call['function']['name']
        tool_args=tool_call['function']['arguments']
        dict_response={'tool_name':tool_name,'arguments':tool_args}
        tool_call_array.append(dict_response)

    return f"TOOL_CALL : {tool_call_array}"

def format_tools_for_prompt(tools):
    def format_schema(schema, name=None, indent=""):
        formatted = ""
        if name:
            formatted += f"{indent}<{name}>\n"
        
        if 'type' in schema:
            formatted += f"{indent}  <type>{schema['type']}</type>\n"
        
        if 'description' in schema:
            formatted += f"{indent}  <description>{schema['description']}</description>\n"
        
        if 'properties' in schema:
            formatted += f"{indent}  <properties>\n"
            for prop_name, prop_schema in schema['properties'].items():
                formatted += format_schema(prop_schema, prop_name, indent + "    ")
            formatted += f"{indent}  </properties>\n"
        
        if 'items' in schema:
            formatted += f"{indent}  <items>\n"
            formatted += format_schema(schema['items'], indent=indent + "    ")
            formatted += f"{indent}  </items>\n"
        
        if '$ref' in schema:
            formatted += f"{indent}  <ref>{schema['$ref']}</ref>\n"
        
        if 'enum' in schema:
            formatted += f"{indent}  <enum>{', '.join(map(str, schema['enum']))}</enum>\n"
        
        if 'default' in schema:
            formatted += f"{indent}  <default>{schema['default']}</default>\n"
        
        if name:
            formatted += f"{indent}</{name}>\n"
        
        return formatted

    formatted_tools = "<Tools>\n"
    for tool in tools:
        function = tool['function']
        formatted_tools += f"  <{function['name']}>\n"
        formatted_tools += f"    <description>{function['description']}</description>\n"
        formatted_tools += "    <parameters>\n"
        
        if '$defs' in function['parameters']:
            formatted_tools += "      <definitions>\n"
            for def_name, def_schema in function['parameters']['$defs'].items():
                formatted_tools += format_schema(def_schema, def_name, "        ")
            formatted_tools += "      </definitions>\n"
        
        formatted_tools += format_schema(function['parameters'], indent="      ")
        formatted_tools += "    </parameters>\n"
        formatted_tools += f"  </{function['name']}>\n"
    
    formatted_tools += "</Tools>"
    return formatted_tools


def fix_json_string(json_str: str,client:OpenAI,model:str) -> str:
    """
    Fixes a JSON string by removing any special characters that might cause issues.
    """
    try:
        message = [
            {'role': 'system', 'content': 'You are a helpful assistant that fixes json strings of tool calls, Your job is to fix the json string of the tool call and return the fixed json string, make sure the adhere to all the tools constraints'},
            {'role': 'user', 'content': f'The json string that needs to be fixed is: {json_str}'}
        ]
        fixed_output = client.chat.completions.create(model=model, messages=message).choices[0].message.content
        return fixed_output
    
    except Exception as e:
        return json_str
    


def parse_tool_response_latest(input_str: str,client,model) -> List[Dict[str, Any]]:
    # Remove the "TOOL_CALL : " prefix if present
     # Remove the "TOOL_CALL : " prefix if present
    if input_str.startswith("TOOL_CALL : "):
        input_str = input_str[12:]

    def extract_objects(s):
        objects = []
        stack = []
        start = 0
        for i, char in enumerate(s):
            if char == '{':
                if not stack:
                    start = i
                stack.append(i)
            elif char == '}':
                if stack:
                    stack.pop()
                    if not stack:
                        objects.append(s[start:i+1])
        return objects

    def process_string(s):
        # Replace all double quotes within __arg1 with single quotes
        s = re.sub(r'("__arg1":\s*")(.+?)(")', 
                   lambda m: m.group(1) + m.group(2).replace('"', "'") + m.group(3), 
                   s, flags=re.DOTALL)
        
        return s

    result = []
    objects = extract_objects(input_str)
    
    for obj in objects:
        try:
            processed = process_string(obj)
            parsed_obj = json.loads(processed)
            result.append(parsed_obj)
        except json.JSONDecodeError as e:
            print(f"Failed to parse: {processed}")
            print(f"Error: {e}")

    return result
    
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
        tool_name = tool_call['name'] if  tool_call.get('name') else ''
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



def manual_json_stringify(data):
    if isinstance(data, dict):
        return _dict_to_json_string(data)
    elif isinstance(data, list):
        return '[' + ', '.join(_dict_to_json_string(item) for item in data if isinstance(item, dict)) + ']'
    else:
        raise ValueError("Input must be a dictionary or list of dictionaries")

def _dict_to_json_string(data_dict):
    items = []
    for key, value in data_dict.items():
        if isinstance(value, str):
            value = '"' + value.replace('"', '\\"') + '"'  # Escape double quotes in string values
        items.append(f'"{key}": {value}')
    return '{' + ', '.join(items) + '}'


def format_tool_result(result):
    try:
        result_dict = json.loads(result) if isinstance(result, str) else result
        formatted = json.dumps(result_dict, indent=2)
        return f"Tool Result:\n{formatted}\n"
    except json.JSONDecodeError:
        return f"Tool Result (raw):\n{result}\n"
    

class CustomOpenAIClient(OpenAI):
    def __init__(self, client):
        super().__init__(api_key=client.api_key)
        self.client = client
        if isinstance(client, OpenAI):
            self.chat.completions.create = self.chat_completion
        if isinstance(client, AsyncOpenAI):
            self.chat.completions.create = self.chat_completion_async

    def _format_chunks(self, response, model):
        is_tool = False
        function_name = ""
        is_tool_arg = False
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content is None:
                continue
            if content == "Action":
                is_tool = True
                continue
            if content == ":":
                continue
            if is_tool:
                function_name += content
            if content == "\n":
                is_tool = False
                function_name = function_name.strip()
                yield self._create_tool_call_chunk(function_name, "", model)
            if content and "{" in content:
                is_tool_arg = True
            if is_tool_arg:
                yield self._create_tool_call_chunk(None, content, model)
            if content and "}" in content:
                is_tool_arg = False

    def _create_tool_call_chunk(self, function_name, arguments, model):
        return ChatCompletionChunk(
            id=str(uuid.uuid4()),
            choices=[
                Choice_Chunk(
                    delta=ChoiceDelta(
                        content=None,
                        function_call=None,
                        role="assistant",
                        tool_calls=[
                            ChoiceDeltaToolCall(
                                index=0,
                                id=str(uuid.uuid4()),
                                function=ChoiceDeltaToolCallFunction(
                                    arguments=arguments, name=function_name
                                ),
                                type="function",
                            )
                        ],
                    ),
                    finish_reason=None,
                    index=0,
                    logprobs=None,
                    content_filter_results={},
                )
            ],
            created=int(time.time()),
            model=model,
            object="chat.completion.chunk",
            system_fingerprint=None,
            usage=None,
        )

    def _process_messages(self, messages, tools, tool_choice,model_type='latest_tool_version', use_vector_store=False):

        if model_type=='old_tool_version' or model_type=='fireworks':
            system_message = next((msg for msg in messages if msg.get("role") == "system"), None)
            system_prompt = system_message["content"] if system_message else "You are a helpful assistant. You have access to the following tools:\n"
            
            
            if use_vector_store:
                added = add_tool_to_vector_store('tools', tools)
                query = messages[-1]['content']
                
                filtered_tool_names = get_tool_from_vector_store('tools', query)
                filtered_tools = [tool for tool in tools if tool['function']['name'] in filtered_tool_names]
                system_prompt += default_tool_formatter(filtered_tools)
            else:
                system_prompt += default_tool_formatter(tools)
            
            messages = [{"role": "system", "content": system_prompt}] + messages

            if tool_choice != "auto" and tool_choice["type"] == "function":
                function = tool_choice["function"]
                if messages[-1]["role"] == "user":
                    messages[-1]["content"] += f",  utilize the tool {function['name']} \n"

            return self._transform_messages(messages)
        elif model_type=='latest_tool_version':

            system_message = messages[0] if  type(messages[0])==dict and messages[0].get("role") == "system" else None

            system_prompt = system_message["content"] if system_message else "You are a helpful assistant. You have access to the following tools:\n\n"
            system_prompt += """If user asks for something trivial that can be done without a tool answer it directly like a normal assistant\n
            Don't deny like currently i dont have that ability or i am not able to do that\n
            """
            #added_tool = add_tool_to_vector_store('tools', tools)
            #if added_tool:
            if use_vector_store:
                pass
            else:
                system_prompt+= format_tools_for_prompt(tools)

            

            messages = [{"role": "system", "content": system_prompt}] + messages

            if tool_choice != "auto" and tool_choice["type"] == "function":
                function = tool_choice["function"]
                if messages[-1]["role"] == "user":
                    messages[-1]["content"] += f",  utilize the tool {function['name']} \n"

            return self._transform_messages(messages,model_type)


    def _transform_messages(self, messages,model_type='latest_tool_version'):

        if model_type=='old_tool_version':
            transformed_messages = []
            for msg in messages:
                if msg.get("role") == "tool":
                    msg["content"] = str({"response": msg["content"]})
                    transformed_messages.append(msg)
                elif msg.get("role") == "assistant" and (isinstance(msg.get("content"), Function) or not msg.get("content")):
                    function_content = msg.get("content") or msg['tool_calls'][0]['function']
                    transformed_messages.append({
                        "role": "assistant",
                        "content": f"Action: {function_content.name}\nAction Input: {function_content.arguments}",
                    })
                elif msg.get("role") == "assistant" and isinstance(msg.get("content"), ChatCompletionMessage):
                    content = msg.get("content")
                    if not content.content:
                        tool = content.tool_calls[0]
                        function_content = tool.function
                        transformed_messages.append({
                            "role": "assistant",
                            "content": f"Action: {function_content.name}\nAction Input: {function_content.arguments}",
                        })
                    else:
                        transformed_messages.append({
                            "role": "assistant",
                            "content": content.content,
                        })
                else:
                    transformed_messages.append(msg)

        elif model_type=='latest_tool_version':
            transformed_messages = []
            tool_results = []
            
            for i, msg in enumerate(messages):
                if isinstance(msg, ChatCompletionMessage):
                    if not msg.content and msg.tool_calls:
                        if isinstance(msg.tool_calls[0], ChatCompletionMessageToolCall):
                            tool_calls = []
                            for tool_call in msg.tool_calls:
                                tool_calls.append({"function": {"name": tool_call.function.name, "arguments": tool_call.function.arguments}})
                            tool_response = convert_to_llama_tool_response_multiple(tool_calls)
                            transformed_messages.append({"content": tool_response, "role": "assistant"})
                    elif msg.content:
                        transformed_messages.append({"content": msg.content, "role": "assistant"})

                    
                
                elif msg.get("role") == "tool":
                    content = msg.get("content")
                    tool_results.append(format_tool_result(content))
                    
                    # If this is the last message or the next message is not a tool response,
                    # add the accumulated tool results as a single string
                    if i == len(messages) - 1 or messages[i+1].get("role") != "tool":
                        merged_tool_results = "\n".join(tool_results)
                        tool_message = {
                            "role": "user",
                            "content": merged_tool_results
                        }
                        
                        transformed_messages.append(tool_message)
                        tool_results = []  # Reset tool_results for the next set
                  
                elif msg.get("role") == "assistant" and isinstance(msg.get("content"), Function):
                    function_content = msg["content"]
                    function_name = function_content.name
                    function_args = function_content.arguments
                    tool_response = convert_to_llama_tool_response_multiple([{"function": {"name": function_name, "arguments": function_args}}])
                    transformed_messages.append({"content": tool_response, "role": "assistant"})
                
                elif msg.get("role") == "assistant" and not msg.get("content"):
                    tool_calls = msg.get("tool_calls")
                    tool_response = convert_to_llama_tool_response_multiple(tool_calls)
                    transformed_messages.append({"content": tool_response, "role": "assistant"})
                
                elif msg.get("role") == "assistant" and isinstance(msg.get("content"), ChatCompletionMessage):
                    content = msg.get("content")
                    if not content.content:
                        tool_calls = content.tool_calls
                        tool_response = convert_to_llama_tool_response_multiple(tool_calls)
                        transformed_messages.append({"content": tool_response, "role": "assistant"})
                    else:
                        transformed_messages.append({"content": content.content, "role": "assistant"})
                
                else:
                    transformed_messages.append(msg)

        return transformed_messages
            

    

    def _create_chat_completion(self, extracted_info, model):
        if isinstance(extracted_info, tuple):
            tool_name, tool_args = extracted_info
            tool_call = ChatCompletionMessageToolCall(
                id=str(uuid.uuid4()),
                function=Function(name=tool_name, arguments=tool_args),
                type="function",
            )
            message = ChatCompletionMessage(content=None, role="assistant", tool_calls=[tool_call])
            return ChatCompletion(
                id=str(uuid.uuid4()),
                choices=[Choice(finish_reason="tool_calls", index=0, logprobs=None, message=message)],
                created=int(time.time()),
                model=model,
                object="chat.completion",
                system_fingerprint=None,
                usage=CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0),
            )
        return None

    def _handle_fireworks_response(self, response, model):
        choice = response.choices[0]
        extracted_info = default_tool_extractor(choice.text)
        chat_completion = self._create_chat_completion(extracted_info, model)
        if chat_completion:
            return chat_completion
        return ChatCompletion(
            id=str(uuid.uuid4()),
            choices=[Choice(finish_reason=choice.finish_reason, index=0, logprobs=None, message=ChatCompletionMessage(content=choice.text, role="assistant"))],
            created=int(time.time()),
            model=model,
            object="chat.completion",
            system_fingerprint=None,
            usage=CompletionUsage(completion_tokens=0, prompt_tokens=0, total_tokens=0)
        )

    async def chat_completion_async(self, model: str, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = [], tool_choice: Union[str, Dict[str, Any]] = "auto", *args, **kwargs):
        if model not in MODEL_NAMES_TYPES:
            raise Exception(f"CustomOpenAIClient does not support the model provided, it only supports {MODEL_NAMES_TYPES.keys()}")
        
        model_type = MODEL_NAMES_TYPES[model]

        use_vector_store = kwargs.pop("use_vector_store", False)

        transformed_messages = self._process_messages(messages, tools, tool_choice, model_type, use_vector_store)

        is_fireworks = model_type == 'fireworks'

        if is_fireworks:
            if kwargs.get('stream'):
                raise Exception("Client does not support stream for fireworks")
            prompt = process_messages(transformed_messages)
            response = await self.client.completions.create(model=model, prompt=prompt, *args, **kwargs)
        else:
            response = await self.client.chat.completions.create(model=model, messages=transformed_messages, *args, **kwargs)

        if kwargs.get("stream") and kwargs["stream"] is True:
            return self._format_chunks(response, model)
        
        if response.choices:
            if is_fireworks:
                return self._handle_fireworks_response(response, model)
            choice = response.choices[0].message
            if model_type == 'old_tool_version':
                extracted_info = default_tool_extractor(choice.content)
                chat_completion = self._create_chat_completion(extracted_info, model)
                if chat_completion:
                    return chat_completion
            elif model_type == 'latest_tool_version':
                tool_calls = parse_tool_response_latest(choice.content, self.client, model)

                if len(tool_calls) and isinstance(tool_calls[0], dict):
                    chat_completion_tool_calls = get_chat_completions_tool_calls(tool_calls, model)
                    return chat_completion_tool_calls
                elif len(tool_calls) and isinstance(tool_calls[0], list):
                    chat_completion_tool_calls = get_chat_completions_tool_calls(tool_calls[0], model)
                    return chat_completion_tool_calls
            else:
                return response
        return response

    def chat_completion(self, model: str, messages: List[Dict[str, Any]], tools: List[Dict[str, Any]] = [], tool_choice: Union[str, Dict[str, Any]] = "auto", *args, **kwargs):
        
        if model not in MODEL_NAMES_TYPES:
            raise Exception(f"CustomOpenAIClient does not support the model provided,it only supports {MODEL_NAMES_TYPES.keys()}")
        
        model_type=MODEL_NAMES_TYPES[model]


        use_vector_store = kwargs.pop("use_vector_store", False)

        transformed_messages = self._process_messages(messages, tools, tool_choice, model_type, use_vector_store)
        
        is_fireworks = model_type == 'fireworks'


        if is_fireworks:
            if kwargs.get('stream'):
                raise Exception("Client does not support stream for fireworks")
            prompt = process_messages(transformed_messages)

            response = self.client.completions.create(model=model, prompt=prompt, *args, **kwargs)

        else:
            response = self.client.chat.completions.create(model=model, messages=transformed_messages, *args, **kwargs)

        if kwargs.get("stream") and kwargs["stream"] is True:
            return self._format_chunks(response, model)
        
        if response.choices:
            if is_fireworks:
                return self._handle_fireworks_response(response, model)
            choice = response.choices[0].message
            if model_type=='old_tool_version':
                extracted_info = default_tool_extractor(choice.content,model_type)
                chat_completion = self._create_chat_completion(extracted_info, model)
                if chat_completion:
                    return chat_completion
            elif model_type=='latest_tool_version':

                tool_calls = parse_tool_response_latest(choice.content,self.client,model)

                
            

                if len(tool_calls) and type(tool_calls[0])==dict:
                    chat_completion_tool_calls = get_chat_completions_tool_calls(tool_calls,model)
                    return chat_completion_tool_calls
            
                elif len(tool_calls) and type(tool_calls[0])==list:
                    chat_completion_tool_calls = get_chat_completions_tool_calls(tool_calls[0],model)
                    return chat_completion_tool_calls
            else:
      
                return response
        return response