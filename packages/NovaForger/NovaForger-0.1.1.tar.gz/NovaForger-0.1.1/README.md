# 简介
NovaForger是一个用于构建LLM应用的框架,相比于LangChain删除了很多不必要的功能。
NovaForger的名字意味着希望这个工具可以帮助开发者构建自己心目中的新星。

# 快速入门
首先我们需要导入模块

    from NovaForger import ChatModel,build_history

然后我们需要LLM提供商提供的地址，LLM的型号，以及你所使用的APIKEY


    BASEURL = "your_baseurl"
    modelname = "secect your model"
    apikey = "your apikey"

我们把这三个变量输入进入ChatModel里并进行实例化

    model = ChatModel(BASEURL = BASEURL,modelname=modelname,apikey=apikey)

最后我们使用run方法并在content变量里放入我们像LLM发送的信息

    message = model.run(content="Hello")
    print(message) # 查看结果

这样就可以得到来自LLM的回复了。

# 给LLM加入记忆
LLM本身没有记忆能力，它是根据上下文的窗口进行内容生成的。
一般来讲，如果你需要构造上下文的，你需要按照以下方式进行构造。
    
    history = [
    {"role":"system","content":"You are a helpful assistant,your name is Alice"},
    {"role":"user","content":"Hello"},
    {"role":"assistant","content":"Hello! How can I assist you today?"}
    ]

接下来，我们就可以把记忆传给LLM了

    message = model.run(content="Hello",history=history)
    print(message) 

输出内容

    I'm Alice, your helpful assistant I'm here to assist you with any questions or tasks you may have. I'm a friendly and knowledgeable AI, and I'm excited to help you in any way I can. What's on your mind? Do you have a specific question or topic you'd like to discuss?

可以看到模型已经通过上下文记住了它的人设。

如果你觉得构建写字典太麻烦，NovaForger提供了三个可能能够简化记忆构建的方法。
分别是AIMessage，HumanMessage，SystemMessage,使用方法与langchain中的相同。

首先我们先导入

    from NovaForger.Message import AImessage,HumanMessage,SystemMessqge

接下来让我们看看它到底做了什么

    history = [
    SystemMessage("You are a helpful assistant,your name is Alice"),
    HumanMessage("Hello"),
    AIMessage("Hello! How can I assist you today?")
    ]
    print(history)

打印histroy
    
    [{'role': 'system', 'content': 'You are a helpful assistant,your name is Alice'}, {'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hello! How can I assist you today?'}]

接下来我们可以正常使用它了

    message = model.run(content="Who are you",history=history)
    print(message)

打印message：
    
    I'm Alice, a helpful assistant here to assist you with any questions or tasks you may have. I'm a large language model, trained to understand and respond to natural language inputs. I can provide information on a wide range of topics, from science and history to entertainment and culture. I can also help with tasks such as writing, proofreading, and translating. What can I help you with today?

# 流式传输

流式传输允许模型一边生成响应一边返回,而不是等待整个响应生成完毕。这可以显著提高用户体验,特别是在生成长文本时。

具体方法如下：

    messages = ""
    for message in model.stream(content="What are you going to do next?"):
        print(message)  # 实时打印每个部分
        messages += message
    print(f"Complete message: {messages}")

# 使用工具
NovaForger允许你给模型添加工具,增强其功能。你可以使用add_tools方法添加工具,然后通过run_with_tools或stream_with_tools方法在使用工具的情况下让模型进行推理。

NovaForger目前提供了Python代码执行器工具。以下是Python执行器工具的定义:

    def pythonRuner(code: str) -> str:
    """
    Executes the provided Python code and returns the result.

    Parameters:
    - code (str): The Python code to be executed.

    Returns:
    - str: The standard output produced by the code execution, or an error message if an exception occurs.
    """
    try:
        # Redirect standard output to capture prints
        import io
        import contextlib
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return output.getvalue()
    except Exception as e:
        return str(e)

接下来我们看看如何添加工具

首先我们先导入

    from NovaForger import ChatModel
    from NovaForger.tools import pythonRuner

然后实例化模型

    model = ChatModel(BASEURL = BASEURL,modelname=modelname,apikey=apikey)

添加工具

    model.add_tools(pythonRuner)

运行

    # 尽可能设定较小的temperature,过高的temperature可能会导致调用工具失败
    message = model.run_with_tools("What time is now",temperature=0.1)

### 自定义工具
你也可以自定义工具。创建自定义工具时,需要在函数的文档字符串中详细说明工具的使用方法。这样模型才能正确理解和使用该工具。


# 获取帮助与贡献
如果你遇到问题,可以在GitHub仓库提出issue。
欢迎提交Pull Request来改进NovaForger。



#### 感谢使用NovaForger!我们期待看到你用它创造出的新星应用!