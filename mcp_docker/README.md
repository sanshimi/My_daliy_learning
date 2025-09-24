# MCP 服务封装到 Docker

复现github项目[6-run-with-docker](https://github.com/daveebbelaar/ai-cookbook/tree/main/mcp/crash-course/6-run-with-docker)实现将mcp服务封装到docker容器中。

## 预先准备

- Win 11
- Ubuntu-24.04 (Win 11 use WSL2)
- uv installed on your system
- Docker installed on your system 
- Git (to clone the repository)

## 项目主结构

- `server.py`: The MCP server implementation with a simple calculator tool
- `client.py`: A client that connects to the server and calls the calculator tool
- `Dockerfile`: Instructions for building the Docker image
- `requirements.txt`: Python dependencies for the project

## 运行服务端

### Step 1: 配置环境

```bash
uv init # 初始化项目
source .venv/bin/activate # 启动虚拟环境
uv add $(cat requirements.txt)
```

可以自由修改uv初始化后新添加的文件，例如删去没用的main.py。

### Step 2: 建立 Docker 镜像

```bash
docker build -t mcp-server .
```

### Step 3: 运行 Docker 容器

```bash
docker run -p 8050:8050 mcp-server
```

This will start the MCP server inside a Docker container and expose it on port 8050.
运行之后会建立一个 Docker 容器并开放 8050 端口 用于监听。同时在 Docker Desktop 的 Containers 界面上可以看到当前容器条目。

## 运行客户端

Once the server is running, you can run the client in a separate terminal:
另开一个进程运行：

```bash
source .venv/bin/activate # 启动虚拟环境
python client.py
```

The client will connect to the server, list available tools, and call the calculator tool to add 2 and 3.
客户端会连接到服务端并调用工具执行功能。

## 规避可能的问题

- Make sure the Docker Desktop on your windows 11 is opening and has setted WSL2 opinion.
确保在Win 11上打开了 Docker Desktop，并在设置中启用了WSL2服务。
- Ubuntu 中 uv 下载 [download](https://docs.astral.sh/uv/getting-started/installation/#next-steps)。

## Notes

- 注意事项参考[6-run-with-docker](https://github.com/daveebbelaar/ai-cookbook/tree/main/mcp/crash-course/6-run-with-docker)
- 只实现了基本的简单函数调用，没有涉及与大模型交互。
- 结合[7-lifecycle-management](https://github.com/daveebbelaar/ai-cookbook/blob/main/mcp/crash-course/7-lifecycle-management/README.md) 在服务端增加了生命周期管理类。
- 设置客户端问两个问题：加法问题和（没有意义）询问生命周期管理类本身。
- 不太确定每次修改server.py后是否需要再运行一次建立 Docker 镜像。但目前是这么做的。

