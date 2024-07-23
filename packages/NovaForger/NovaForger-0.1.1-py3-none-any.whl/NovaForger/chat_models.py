import requests
import json
import aiohttp
from typing import Optional, Tuple, Dict, Any, Generator,List,AsyncGenerator, Callable
import inspect
from .utils import readObject

class ChatModel:
    def __init__(self, BASEURL: str, modelname: str, apikey: str,roleplay_name:str = "assistant") -> None:
        """
        初始化 API 客户端实例。

        参数:
            BASEURL (str): API 提供商提供的基础 URL 地址。
            modelname (str): 模型名称，例如 'gpt-3.5-turbo-0125'。
            apikey (str): API 密钥，用于验证 API 请求的身份。
            roleplay_name (str, 可选): 如果需要使用多个模型进行角色扮演，可以在此处指定角色名称。默认为 'assistant'。

        功能:
            该方法初始化一个 API 客户端实例，并设置基础 URL、模型名称、API 密钥和角色名称。
            同时，它会配置请求头，以便正确地进行 API 调用。

        示例:
            model = ChatModel(
                BASEURL="https://api.example.com",
                modelname="gpt-3.5-turbo-0125",
                apikey="your_api_key",
                roleplay_name="assistant"
            )
        """
        self.url = BASEURL
        self.modelname = modelname
        self.roleplay_name = roleplay_name
        self.apikey = apikey
        self.tools = {}
        self.headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Content-Type': 'application/json'
        }

    def run(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: float = 0.5, max_token: int = 500, check_payload: bool = False,check_usage: bool = False) -> str:
        """
        Sends a request to the model API and returns the generated response.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : float, optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, returns the usage statistics along with the generated message, default is False.

        Returns:
        --------
        str
            The generated message from the model. If `check_usage` is True, returns a tuple with the message and usage statistics.
        """
        if history is None:
            history = []
        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "messages": history + [{"role": role, "content": content}]
        })

        if check_payload:
            print("Payload:", payload)
        
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            response.raise_for_status()  # Check for HTTP request errors
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
        message,usage = readObject(response.text)
        if check_usage:
            return message,usage
        else:
            return message


    def stream(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: Optional[float] = 0.5, max_token: int = 500, check_payload: bool = False,check_usage: bool = False) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        """
        Streams responses from the model API as they are generated.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : Optional[float], optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, yields the usage statistics along with each generated message, default is False.

        Yields:
        -------
        Generator[Tuple[str, Dict[str, Any]], None, None]
            Yields each generated message from the model. If `check_usage` is True, yields a tuple with the message and usage statistics for each generated message.
        """
        if history is None:
            history = []

        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "stream":True,
            "max_token": max_token,
            "messages": history + [{"role": role, "content": content}]
        })

        if check_payload:
            print("Payload:", payload)
        
        try:
            with requests.post(self.url, headers=self.headers, data=payload, stream=True) as response:
                response.raise_for_status()  # Check for HTTP request errors
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line.startswith("data: "):  # Check if the line starts with "data: "
                            decoded_line = decoded_line[len("data: "):]  # Remove the "data: " prefix
                        if decoded_line:  # Check if the line is not empty
                            if decoded_line == "[DONE]":  # Ignore the [DONE] line
                                continue
                            try:
                                data = json.loads(decoded_line)
                                message = data['choices'][0].get('delta', {}).get('content', '')
                                usage = data.get('usage', {})
                                if check_usage:
                                    yield message, usage
                                else:
                                    yield message
                            except json.JSONDecodeError as e:
                                print(f"JSON decode error: {e} - Line: {decoded_line}")
        except requests.exceptions.RequestException as e:
            yield f"An error occurred: {e}"
            
    def add_tools(self, tool_func: Callable) -> None:
        """Register a tool (function) that can be called by the model."""
        tool_name = tool_func.__name__
        sig = inspect.signature(tool_func)
        docstring = inspect.getdoc(tool_func) or "No description available"
        params = ", ".join([f"{name}: {param.annotation.__name__}" if param.annotation != inspect.Parameter.empty else name for name, param in sig.parameters.items()])
        description = f"{tool_name}({params}) - {docstring}"
        self.tools[tool_name] = {
            "func": tool_func,
            "description": description
        }
    def parse_function_call(self, response_text: str, history: List[Dict[str, str]], temperature: float, max_token: int,check_usage: bool = False):
        """Parse the model's response to check for function calls."""
        try:
            call_data = json.loads(response_text)  # 解析 JSON 格式的函数调用
            function_name = call_data.get("function")
            arguments = call_data.get("arguments", {})
            if function_name in self.tools:
                function = self.tools[function_name]["func"]
                result = function(**arguments)
                return self.continue_conversation(str(result), history, temperature, max_token,check_usage)
            else:
                raise ValueError(f"Function {function_name} not found in registry.")
        except json.JSONDecodeError as e:
            return response_text
        except Exception as e:
            return f"Error in function call: {str(e)}"
    def continue_conversation(self, result: str, history: List[Dict[str, str]], temperature: float, max_token: int,check_usage: bool = False) -> str:
        """Send the tool execution result back to the model to continue the conversation."""
        prompt = f"""
        system:
        The result of the function execution is: {result}
        """
        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "messages": history + [{"role": "user", "content": prompt}]
        })
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            response.raise_for_status()  # Check for HTTP request errors
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
        model_response,usage = readObject(response.text)
        if check_usage:
            return model_response,usage
        else:
            return model_response
    def parse_function_call_stream(self, response_text: str, history: List[Dict[str, str]], temperature: float, max_token: int, check_usage: bool = False) -> Generator[str, None, None]:
        """Parse the model's response to check for function calls."""
        try:
            call_data = json.loads(response_text)  # 解析 JSON 格式的函数调用
            function_name = call_data.get("function")
            arguments = call_data.get("arguments", {})

            if function_name in self.tools:
                function = self.tools[function_name]["func"]
                result = function(**arguments)
                yield from self.continue_conversation_stream(str(result), history, temperature, max_token, check_usage)
            else:
                raise ValueError(f"Function {function_name} not found in registry.")
        except json.JSONDecodeError:
            yield response_text
        except Exception as e:
            yield f"Error in function call: {str(e)}"

    def continue_conversation_stream(self, result: str, history: List[Dict[str, str]], temperature: float, max_token: int, check_usage: bool = False) -> Generator[str, None, None]:
        """Send the tool execution result back to the model to continue the conversation."""
        prompt = f"""
        system:
        The result of the function execution is: {result}
        """
        
        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "stream":True,
            "messages": history + [{"role": "user", "content": prompt}]
        })
        try:
            response = requests.post(self.url, headers=self.headers, data=payload, stream=True)
            response.raise_for_status()  # Check for HTTP request errors
            for chunk in response.iter_content(8192):
                if chunk:
                    decoded_chunk = chunk.decode('utf-8').strip()
                    for line in decoded_chunk.splitlines():
                        if line.startswith("data: "):
                            line = line[len("data: "):]
                        if line:
                            if line == "[DONE]":  # Ignore the [DONE] line
                                continue
                            try:
                                data = json.loads(line)
                                message = data['choices'][0].get('delta', {}).get('content', '')
                                usage = data.get('usage', {})
                                if check_usage:
                                    yield message, usage
                                else:
                                    yield message
                            except json.JSONDecodeError as e:
                                print(f"JSON decode error: {e} - Line: {line}")
                            except KeyError as e:
                                print(f"Key error: {e} - Data: {data}")
        except requests.exceptions.RequestException as e:
            yield f"An error occurred: {e}"
    def run_with_tools(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: float = 0.5, max_token: int = 500, check_payload: bool = False,check_usage: bool = False) -> str:
        """
        Sends a request to the model API with the capability to call predefined functions and returns the generated response.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : float, optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, returns the usage statistics along with the generated message, default is False.

        Returns:
        --------
        str
            The generated message from the model. If the model calls a function, the function call is parsed and executed, and the final response is returned.
        """
        if history is None:
            history = []

        tool_descriptions = "\n".join([tool["description"] for tool in self.tools.values()])
        tool_prompt = f"""
        You can perform tasks using predefined functions. Here are the available functions:

        {tool_descriptions}

        When you think a function call is necessary, respond with a JSON object in the following format and just output json object:
        {{"function": "function_name", "arguments": {{"arg1": value1, "arg2": value2}}}}

        If no function call is needed, provide the answer directly.
        """


        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "messages": history+ [{"role": "system", "content": tool_prompt}]+ [{"role": role, "content": content}]
        })

        if check_payload:
            print("Payload:", payload)

        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            response.raise_for_status()  # Check for HTTP request errors
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
        history += [{"role": role, "content": content}]
        model_response,usage = readObject(response.text)
        return self.parse_function_call(model_response, history, temperature, max_token,check_usage)
    def stream_with_tools(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: Optional[float] = 0.5, max_token: int = 500,check_payload: bool = False,check_usage: bool = False) -> Generator[Tuple[str, Dict[str, Any]], None, None]:
        """
        Streams responses from the model API with the capability to call predefined functions as they are generated.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : Optional[float], optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, yields the usage statistics along with each generated message, default is False.

        Yields:
        -------
        Generator[Tuple[str, Dict[str, Any]], None, None]
            Yields each generated message from the model. If the model calls a function, the function call is parsed and executed, and the final response is yielded.
        """
        if history is None:
            history = []

        tool_descriptions = "\n".join([tool["description"] for tool in self.tools.values()])
        tool_prompt = f"""
        You can perform tasks using predefined functions. Here are the available functions:

        {tool_descriptions}

        When you think a function call is necessary, respond with a JSON object in the following format and just output json object:
        {{"function": "function_name", "arguments": {{"arg1": value1, "arg2": value2}}}}

        If no function call is needed, provide the answer directly.
        """

        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "stream":True,
            "max_token":max_token,
            "messages": history + [{"role": "system", "content": tool_prompt}] + [{"role": role, "content": content}],
        })

        if check_payload:
            print("Payload:", payload)

        try:
            with requests.post(self.url, headers=self.headers, data=payload, stream=True) as response:
                response.raise_for_status()  # Check for HTTP request errors
                complete_response = ""
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        if decoded_line.startswith("data: "):  # Check if the line starts with "data: "
                            decoded_line = decoded_line[len("data: "):]  # Remove the "data: " prefix
                        if decoded_line:  # Check if the line is not empty
                            if decoded_line == "[DONE]":  # Ignore the [DONE] line
                                continue
                            try:
                                data = json.loads(decoded_line)
                                message = data['choices'][0].get('delta', {}).get('content', '')
                                usage = data.get('usage', {})
                                complete_response += message
                                # 如果想要知道llm调用tools的过程，请把这个注释取消
                                # yield message, usage
                            except json.JSONDecodeError as e:
                                print(f"JSON decode error: {e} - Line: {decoded_line}")
                            except KeyError as e:
                                print(f"Key error: {e} - Line: {decoded_line}")
                # After the stream is complete, check for a function call
                history += [{"role": role, "content": content}]
                parsed_response_generator = self.parse_function_call_stream(complete_response, history, temperature, 500,check_usage=check_usage)
                for parsed_response in parsed_response_generator:
                    yield parsed_response
        except requests.exceptions.RequestException as e:
            yield f"An error occurred: {e}", {}
    
class AsyncChatModel:
    def __init__(self, BASEURL: str, modelname: str, apikey: str,roleplay_name:str = "assistant") -> None:
        self.url = BASEURL
        self.modelname = modelname
        self.apikey = apikey
        self.roleplay_name = roleplay_name
        self.tools = {}
        self.headers = {
            'Authorization': f'Bearer {self.apikey}',
            'Content-Type': 'application/json'
        }

    async def arun(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: float = 0.5, max_token: int = 500, check_payload: bool = False,check_usage: bool = False) -> str:
        """
        Sends an asynchronous request to the model API and returns the generated response.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : float, optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, returns the usage statistics along with the generated message, default is False.

        Returns:
        --------
        str
            The generated message from the model. If check_usage is True, returns a tuple of the generated message and usage statistics.
        """
        if history is None:
            history = []
        
        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "messages": history + [{"role": role, "content": content}]
        })

        if check_payload:
            print("Payload:", payload)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.url, headers=self.headers, data=payload) as response:
                    response.raise_for_status()  # Check for HTTP request errors
                    message,usage = readObject(await response.text())
                    # 如果check_usage是True，返回message,usage
                    if check_usage:
                        return message,usage
                    else:
                        return message
            except aiohttp.ClientError as e:
                return f"An error occurred: {e}"

    async def astream(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: Optional[float] = 0.5, max_token: int = 500, check_payload: bool = False,check_usage: bool = False) -> AsyncGenerator[Tuple[str, Dict[str, Any]], None]:
        """
        Streams asynchronous responses from the model API as they are generated.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : Optional[float], optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, yields the usage statistics along with each generated message, default is False.

        Yields:
        -------
        AsyncGenerator[Tuple[str, Dict[str, Any]], None]
            Yields each generated message from the model. If check_usage is True, yields a tuple of the generated message and usage statistics.
        """
        if history is None:
            history = []

        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "stream":True,
            "max_token":max_token,
            "messages": history + [{"role": role, "content": content}]
        })

        if check_payload:
            print("Payload:", payload)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.url, headers=self.headers, data=payload) as response:
                    response.raise_for_status()  # Check for HTTP request errors
                    usage = None
                    async for line in response.content:
                            decoded_line = line.decode('utf-8').strip()
                            if decoded_line.startswith("data: "):  # 检查前缀并移除
                                decoded_line = decoded_line[len("data: "):]
                            
                            if decoded_line:  # Check if the line is not empty
                                if decoded_line == "[DONE]":  # Ignore the [DONE] line
                                    continue
                                try:
                                    data = json.loads(decoded_line)
                                    message = data['choices'][0].get('delta', {}).get('content', '')
                                    usage = data.get('usage', {})
                                    if check_usage:
                                        yield message, usage
                                    else:
                                        yield message
                                except json.JSONDecodeError as e:
                                    print(f"JSON decode error: {e} - Line: {decoded_line}")
            except aiohttp.ClientError as e:
                yield f"An error occurred: {e}", {}

    def add_tools(self, tool_func: Callable) -> None:
        """Register a tool (function) that can be called by the model."""
        tool_name = tool_func.__name__
        sig = inspect.signature(tool_func)
        docstring = inspect.getdoc(tool_func) or "No description available"
        params = ", ".join([f"{name}: {param.annotation.__name__}" if param.annotation != inspect.Parameter.empty else name for name, param in sig.parameters.items()])
        description = f"{tool_name}({params}) - {docstring}"
        self.tools[tool_name] = {
            "func": tool_func,
            "description": description
        }

    async def parse_function_call(self, response_text: str, history: List[Dict[str, str]], temperature: float, max_token: int,check_usage: bool = False) -> str:
        """Parse the model's response to check for function calls."""
        try:
            call_data = json.loads(response_text)  # 解析 JSON 格式的函数调用
            function_name = call_data.get("function")
            arguments = call_data.get("arguments", {})

            if function_name in self.tools:
                function = self.tools[function_name]["func"]
                result = function(**arguments)
                return await self.continue_conversation(str(result), history, temperature, max_token,check_usage)
            else:
                raise ValueError(f"Function {function_name} not found in registry.")
        except json.JSONDecodeError:
            return response_text
        except Exception as e:
            return f"Error in function call: {str(e)}"

    async def continue_conversation(self, result: str, history: List[Dict[str, str]], temperature: float, max_token: int,check_usage: bool = False) -> str:
        """Send the tool execution result back to the model to continue the conversation."""
        prompt = f"""
        system:
        The result of the function execution is: {result}
        """
        
        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "messages": history + [{"role": "user", "content": prompt}]
        })
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            response.raise_for_status()  # Check for HTTP request errors
        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
        model_response,usage = readObject(response.text)
        if check_usage:
            return model_response,usage
        else:
            return model_response
    async def parse_function_call_stream(self, response_text: str, history: List[Dict[str, str]], temperature: float, max_token: int, check_usage: bool = False) -> AsyncGenerator[str, None]:
        """Parse the model's response to check for function calls."""
        try:
            call_data = json.loads(response_text)  # 解析 JSON 格式的函数调用
            function_name = call_data.get("function")
            arguments = call_data.get("arguments", {})

            if function_name in self.tools:
                function = self.tools[function_name]["func"]
                result = await function(**arguments)
                async for item in self.continue_conversation_stream(str(result), history, temperature, max_token, check_usage):
                    yield item
            else:
                raise ValueError(f"Function {function_name} not found in registry.")
        except json.JSONDecodeError:
            yield response_text
        except Exception as e:
            yield f"Error in function call: {str(e)}"

    async def continue_conversation_stream(self, result: str, history: List[Dict[str, str]], temperature: float, max_token: int, check_usage: bool = False) -> AsyncGenerator[Tuple[str, Dict[str, Any]], None]:
        """Send the tool execution result back to the model to continue the conversation."""
        prompt = f"""
        system:
        The result of the function execution is: {result}
        """

        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "stream": True,
            "messages": history + [{"role": "user", "content": prompt}]
        })

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, data=payload) as response:
                    response.raise_for_status()  # Check for HTTP request errors
                    async for chunk in response.content.iter_chunked(8192):
                        if chunk:
                            decoded_chunk = chunk.decode('utf-8').strip()
                            for line in decoded_chunk.splitlines():
                                if line.startswith("data: "):
                                    line = line[len("data: "):]
                                if line:
                                    try:
                                        data = json.loads(line)
                                        message = data['choices'][0].get('delta', {}).get('content', '')
                                        usage = data.get('usage', {})
                                        if check_usage:
                                            yield message, usage
                                        else:
                                            yield message
                                    except json.JSONDecodeError as e:
                                        print(f"JSON decode error: {e} - Line: {line}")
                                    except KeyError as e:
                                        print(f"Key error: {e} - Data: {data}")
        except aiohttp.ClientError as e:
            yield f"An error occurred: {e}", {}
    async def arun_with_tools(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: float = 0.5, max_token: int = 500, check_payload: bool = False,check_usage: bool = False) -> str:
        """
        Sends an asynchronous request to the model API with tool descriptions and returns the generated response.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : float, optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, returns the usage statistics along with the generated message, default is False.

        Returns:
        --------
        str
            The generated message from the model. If check_usage is True, returns a tuple of the generated message and usage statistics.
        """
        if history is None:
            history = []

        tool_descriptions = "\n".join([tool["description"] for tool in self.tools.values()])
        tool_prompt = f"""
        You can perform tasks using predefined functions. Here are the available functions:

        {tool_descriptions}

        When you think a function call is necessary, respond with a JSON object in the following format:
        {{"function": "function_name", "arguments": {{"arg1": value1, "arg2": value2}}}}

        If no function call is needed, provide the answer directly.
        """

        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "max_token": max_token,
            "messages": history + [{"role": "system", "content": tool_prompt}] + [{"role": role, "content": content}]
        })

        if check_payload:
            print("Payload:", payload)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, data=payload) as response:
                    response.raise_for_status()  # Check for HTTP request errors
                    response_text = await response.text()
        except aiohttp.ClientError as e:
            return f"An error occurred: {e}"
        
        history += [{"role": role, "content": content}]
        model_response, usage = readObject(response_text)  # Assuming readObject is also async
        return await self.parse_function_call_stream(model_response, history, temperature, max_token,check_usage=check_usage)  # Awaiting parse_function_call

    async def astream_with_tools(self, content: str, role: str = "user", history: Optional[List[Dict[str, str]]] = None, temperature: Optional[float] = 0.5, max_token: int = 500, check_payload: bool = False, check_usage: bool = False) -> AsyncGenerator[Tuple[str, Dict[str, Any]], None]:
        """
        Streams asynchronous responses from the model API with tool descriptions as they are generated.

        Parameters:
        -----------
        content : str
            The input content to be processed by the model.
        
        role : str, optional
            The role of the message sender, default is "user".
        
        history : Optional[List[Dict[str, str]]], optional
            The conversation history as a list of dictionaries, each containing "role" and "content" keys. If None, an empty list is used.
        
        temperature : Optional[float], optional
            The sampling temperature to use, default is 0.5.
        
        max_token : int, optional
            The maximum number of tokens to generate, default is 500.
        
        check_payload : bool, optional
            If True, prints the payload being sent to the model API, default is False.
        
        check_usage : bool, optional
            If True, yields the usage statistics along with each generated message, default is False.

        Yields:
        -------
        AsyncGenerator[Tuple[str, Dict[str, Any]], None]
            Yields each generated message from the model. If check_usage is True, yields a tuple of the generated message and usage statistics.
        """
        if history is None:
            history = []
        
        tool_descriptions = "\n".join([tool["description"] for tool in self.tools.values()])
        tool_prompt = f"""
        You can perform tasks using predefined functions. Here are the available functions:

        {tool_descriptions}

        When you think a function call is necessary, respond with a JSON object in the following format:
        {{"function": "function_name", "arguments": {{"arg1": value1, "arg2": value2}}}}

        If no function call is needed, provide the answer directly.
        """
        

        payload = json.dumps({
            "model": self.modelname,
            "temperature": temperature,
            "stream": True,
            "max_token": max_token,
            "messages": history + [{"role": "system", "content": tool_prompt}] + [{"role": role, "content": content}],
        })
        if check_payload:
            print("Payload:", payload)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, data=payload) as response:
                    response.raise_for_status()  # Check for HTTP request errors
                    complete_response = ""
                    async for line in response.content:
                        if line:
                            decoded_line = line.decode('utf-8').strip()
                            if decoded_line.startswith("data: "):  # Check if the line starts with "data: "
                                decoded_line = decoded_line[len("data: "):]  # Remove the "data: " prefix
                            if decoded_line:  # Check if the line is not empty
                                if decoded_line == "[DONE]":  # Ignore the [DONE] line
                                    continue
                                try:
                                    data = json.loads(decoded_line)
                                    message = data['choices'][0].get('delta', {}).get('content', '')
                                    usage = data.get('usage', {})
                                    complete_response += message
                                    # 如果想要知道llm调用tools的过程，请把这个注释取消
                                    # yield message, usage
                                except json.JSONDecodeError as e:
                                    print(f"JSON decode error: {e} - Line: {decoded_line}")
                                except KeyError as e:
                                    print(f"Key error: {e} - Line: {decoded_line}")
                    # After the stream is complete, check for a function call
                    history += [{"role": role, "content": content}]
                    async for parsed_response in self.parse_function_call_stream(complete_response, history, temperature, 500, check_usage=check_usage):
                        yield parsed_response
        except aiohttp.ClientError as e:
            yield f"An error occurred: {e}", {}
