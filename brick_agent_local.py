import gradio as gr
from openai import OpenAI
import json
import os
import time
import threading
from playwright.sync_api import sync_playwright

from brick_agent_tools import *
from brick_agent_functions import *

api_key = 'ollama'

MODEL = "llama3.2:3b"
ollama = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key=api_key
)


system_prompt = """You are a LEGO set assistant. Answer in 1 sentence max.

RULES:
- Use tools to find data. Never guess.
- Use ONLY the exact parameter names each tool defines.
- If a tool errors, try a different approach.
- If no tool fits the question, say you don't know.
"""


def handle_tool_call(message):
    responses = []
    for tool_call in message.tool_calls:
        fn_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        fn = TOOL_REGISTRY.get(fn_name)
        result = fn(**args) if fn else {"error": f"Unknown tool: {fn_name}"}

        if isinstance(result, (pd.Series, pd.DataFrame)):
            content = result.to_json()
        elif isinstance(result, str):
            content = result
        else:
            content = json.dumps(result, default=str)

        responses.append({"role": "tool", "tool_call_id": tool_call.id, "content": content})
    return responses



def chat(message, history):
    messages = [{"role": "system", "content": system_prompt}]

    for item in history:
        if item["role"] == "user":
            messages.append({"role": "user", "content": item["content"]})
        elif item["role"] == "assistant":
            messages.append({"role": "assistant", "content": item["content"]})

    messages.append({"role": "user", "content": message})

    response = ollama.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS
    )
    msg = response.choices[0].message

    if not msg.tool_calls:
        return msg.content

    tool_log = []

    messages.append(msg)
    for tc in msg.tool_calls:
        tool_log.append(f"🔧 `{tc.function.name}` → args: `{tc.function.arguments}`")
    messages.extend(handle_tool_call(msg))

    response = ollama.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS
    )
    msg = response.choices[0].message

    while msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            tool_log.append(f"🔧 `{tc.function.name}` → args: `{tc.function.arguments}`")
        messages.extend(handle_tool_call(msg))
        response = ollama.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = response.choices[0].message

    log_text = "\n\n".join(tool_log)
    return f"{msg.content}\n\n---\n{log_text}"


def open_browser():
    time.sleep(1)
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.goto("http://localhost:7860")
        while page.url:
            time.sleep(1)


if __name__ == "__main__":
    gr.close_all()
    threading.Thread(target=open_browser, daemon=True).start()
    gr.ChatInterface(fn=chat).launch()