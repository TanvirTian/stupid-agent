<p align="center">
  <img src="https://github.com/user-attachments/assets/31615629-43fb-47cd-a9a0-6545bfd9ec4a" alt="Stupid-Agent Logo" width="220">
</p>

<p align="center">
A minimal AI agent built from scratch using Python, Ollama, and Qwen 2.5:7B
<br>
No frameworks. Just the fundamentals.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Ollama-Local-black?style=flat-square">
  <img src="https://img.shields.io/badge/Qwen-2.5:7B-purple?style=flat-square"> 
</p>


## About

Stupid-Agent is a personal learning project for understanding how AI agents work under the hood.

Rather than relying on frameworks like LangChain, LangGraph, CrewAI, or AutoGen, this project implements the core building blocks manually to better understand how modern AI agents are designed.

The project runs entirely locally  using Ollama with Qwen 2.5:7B


## Goals

This project focuses on learning the fundamentals behind AI agents, including:

- LLM communication
- Prompt engineering
- Conversation memory
- Tool calling
- JSON parsing
- Agent orchestration
- Modular agent architecture

## Features

- Local chat powered by Ollama
- Session-based conversation memory
- File reader tool
- Automatic tool calling
- Simple, modular codebase
-  Runs completely offline



## Supported Features

- Local LLM interaction
- Conversation history
- File reading tool
- Function/tool calling
- JSON response handling

More capabilities will be added as I continue learning how AI agents work internally.

## Quick Start

This guide assumes Qwen 2.5:7B is already installed in Ollama

```bash
git clone https://github.com/TanvirTian/stupid-agent.git
cd stupid-agent

#Make sure Ollama is running
systemctl start ollama
# Start the agent
python main.py
```
## Example Usage

### Basic Chat

```text
You: What is recursion?

Assistant: Recursion is a programming technique where a function calls itself...
```

### Conversation Memory
```text
You: My name is Tian.
You: What is my name?

Assistant: Your name is Tian.
```

### File Reader Tool

Place a file inside the `files/` directory:

```text
files/
└── notes.txt
```

Then simply ask:

```text
You: Read notes.txt and summarize it.
```

The agent will decide whether to use the file reader tool and answer based on the file's contents.

> **Note**
> The file reader is intentionally sandboxed and can only access files inside the `files/` directory.

## Philosophy

The goal isn't to build the smartest agent.

The goal is to understand **why** agent frameworks work by building the underlying components from scratch.


## License

MIT
