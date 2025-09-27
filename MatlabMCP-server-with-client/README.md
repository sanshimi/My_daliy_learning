# 复现尝试

## 源项目

[MatlabMCP](https://github.com/jigarbhoye04/MatlabMCP)

## 虚拟环境

On Windows:
```powershell
git clone https://github.com/jigarbhoye04/MatlabMCP.git
cd MatlabMCP
uv init
uv venv
.venv\Scripts\activate
uv pip sync pyproject.toml 
```

###  Matlab环境

参阅[Can I use the MATLAB Engine API for Python with a virtual environment?](https://ww2.mathworks.cn/matlabcentral/answers/2086093-can-i-use-the-matlab-engine-api-for-python-with-a-virtual-environment)、[MATLAB and Simulink Requirements](https://ww2.mathworks.cn/support/requirements/python-compatibility.html)和[Release history](https://pypi.org/project/matlabengine/#history)。

The MATLAB Python Engine API only supports local communication.

But in a Docker environment, you can connect to a MATLAB engine inside the container from outside the container (host)

```powershell
uv pip install matlabengine==25.1.2 # My Matlab version is R2025a.
```

## 运行服务端

在matlab中运行：

```m
matlab.engine.shareEngine
% matlab.engine.isEngineShared
```

```
uv run main.py
```

如过Matlab没打开，则会报错。例如：

```
2025-09-27 16:21:58,551 - MatlabMCP - INFO - Finding shared MATLAB sessions...
2025-09-27 16:21:58,606 - MatlabMCP - INFO - Found sessions: ()
2025-09-27 16:21:58,606 - MatlabMCP - ERROR - No shared MATLAB sessions found. This server requires a shared MATLAB session.
2025-09-27 16:21:58,606 - MatlabMCP - ERROR - Please start MATLAB and run 'matlab.engine.shareEngine' in its Command Window.
```

## 运行客户端

启动大模型模型API管理工作台网页。

在VSCode中新建一个终端，运行：

```powershell
.venv\Scripts\activate
uv run client.py
```

## 效果

实现从向大模型提问的问题中提取matlab命令行代码文本，并将其输入到本地后台matlab程序中运行。

本项目使用kimi模型[kimi-k2-0711-preview](https://platform.moonshot.cn/)

代码后台执行成功后，输出被 mcp 库捕获并返回给 Python 供 AI 模型使用。

例如：

```powershell
Changed OpenAI client with env: MOONSHOT_API_KEY, MOONSHOT_BASE_URL

Connected to server with tools:
  - runMatlabCode:
    Runs arbitrary MATLAB code in the shared MATLAB session.
    WARNING: Executing arbitrary code can be a security risk.
    This tool attempts execution via a temporary file first, then falls back to eng.evalc() to capture output.

    Args:
        code: The MATLAB code string to execute.

    Returns:
        A dictionary with:
        - "status": "success" or "error"
        - "output": (on success) A message indicating success or the captured output from eng.evalc().
        - "error_type": (on error) The type of Python exception.
        - "stage": (on error) The stage of execution where the error occurred.
        - "message": (on error) A detailed error message.

  - getVariable:
    Gets the value of a variable from the MATLAB workspace.

    Args:
        variable_name: The name of the variable to retrieve.

    Returns:
        A dictionary with:
        - "status": "success" or "error"
        - "variable": (on success) The name of the variable.
        - "value": (on success) The JSON-serializable value of the variable.
        - "error_type": (on error) The type of Python exception.
        - "message": (on error) A detailed error message.

Time taken to connect to server: 3.81 seconds

Query: Hello!. Please use matlab to run code: LEO;

Response: The MATLAB code `LEO;` executed successfully. The output indicates that a file has been saved to the `..\output` directory.
Time taken to process query: 6.28 seconds
```
