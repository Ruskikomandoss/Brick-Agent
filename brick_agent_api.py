import gradio as gr
from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import time
import threading
from playwright.sync_api import sync_playwright

from src.brick_agent_tools import *
from src.brick_agent_functions import *

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
MODEL = "gpt-4.1-mini"
openai = OpenAI()


system_prompt = """
You're a smart handy assistant that finds requested information about LEGO sets. You have several tools at your disposal to use efectively to acquire information.
Give short, courteous answers, no more than 1 sentence. Always be accurate. If you don't know the answer, say so.
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

    response = openai.chat.completions.create(
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

    response = openai.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS
    )
    msg = response.choices[0].message

    while msg.tool_calls:
        messages.append(msg)
        for tc in msg.tool_calls:
            tool_log.append(f"🔧 `{tc.function.name}` → args: `{tc.function.arguments}`")
        messages.extend(handle_tool_call(msg))
        response = openai.chat.completions.create(
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
        page.wait_for_timeout(99999)


if __name__ == "__main__":
    gr.close_all()
    threading.Thread(target=open_browser, daemon=True).start()
    gr.ChatInterface(fn=chat).launch()