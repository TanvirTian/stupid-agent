<p align="center">
  <img src="https://github.com/user-attachments/assets/31615629-43fb-47cd-a9a0-6545bfd9ec4a"
       alt="Stupid-Agent"
       width="256" height=200>
</p>

# Stupid Agent

Learning how AI agents work by building one from scratch using Python, Ollama, and Qwen 2.5:7B.

No frameworks. Just the fundamentals.

---

## Quick Start
im assuming you already have `qwen2.5:7b` downloaded in Ollama

```bash
#clone the repo
git clone https://github.com/TanvirTian/stupid-agent.git
cd stupid-agent
#start ollama
systemctl start ollama
#start the agent
python main.py
```


## Progress

### Conversation Memory

My stupid agent can now remember previous messages.

whoaaa

Before

```bash
you: my name is Tian

you: what is my name?
assistant: idk
```

After

```bash
you: my name is Tian

you: what is my name?
assistant: Your name is Tian.
```

### Tool
```text
Added File reading tool. 
now my agent can read text files but only from the /files directory
```