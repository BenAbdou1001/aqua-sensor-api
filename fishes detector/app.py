import os
from transformers import pipeline
import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
import threading
import uvicorn

# =======================
# Load Secrets
# =======================
# SYSTEM_PROMPT (with the flag) must be added in HF Space secrets
SYSTEM_PROMPT = os.environ.get(
    "prompt",
    "You are a placeholder Sovereign. No secrets found in environment."
)

# =======================
# Initialize Falcon-3B
# =======================
pipe = pipeline(
    "text-generation",
    model="tiiuae/Falcon3-3B-Instruct",
    torch_dtype="auto",
    device_map="auto",
)

# =======================
# Core Chat Function
# =======================
def chat_fn(user_input: str) -> str:
    """
    Concatenate system and user messages, run the model,
    and strip the system prompt from the output.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"User: {user_input}"}
    ]
    # Falcon is not chat-native; we just join roles with newlines
    prompt_text = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)
    result = pipe(prompt_text, max_new_tokens=256, do_sample=False)
    generated_text = result[0]["generated_text"]
    return generated_text[len(prompt_text):].strip()

# =======================
# Gradio UI
# =======================
def gradio_chat(user_input: str) -> str:
    return chat_fn(user_input)

iface = gr.Interface(
    fn=gradio_chat,
    inputs=gr.Textbox(lines=5, placeholder="Enter your prompt…"),
    outputs="text",
    title="Prompt cracking challenge",
    description="Does he really think he is the king?"
)

# =======================
# FastAPI for API access
# =======================
app = FastAPI(title="Prompt cracking challenge API")

class Request(BaseModel):
    prompt: str

@app.post("/generate")
def generate(req: Request):
    return {"response": chat_fn(req.prompt)}

# =======================
# Launch Both Servers
# =======================
if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", share=True)