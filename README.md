# 🧠🎙️ Voice2Voice 2-Phase AI Assistant

A lightweight **Voice-to-Voice Conversational AI Assistant** that simplifies the traditional 3-stage pipeline into just **2 phases**:
- **Phase 1:** `Ultravox` model for **Audio → Text → LLM Response**
- **Phase 2:** `Kokoro` model for **Text → AI Voice Output**

This project allows users to **speak into a mic** and hear **natural-sounding AI responses**, in near real-time.

---

## 🚀 Key Features

- ✅ **2-Phase Simplicity:** Merges ASR + LLM using [Ultravox](https://huggingface.co/fixie-ai/ultravox-v0_5-llama-3_1-8b)
- 🧠 **LLM-powered conversations** (Llama 3.1-based model)
- 🔊 **High-quality voice responses** using [Kokoro TTS](https://huggingface.co/hexgrad/Kokoro-82M)
- 🎛️ **Gradio UI** for easy interaction and live audio chat
- 🧩 Easily extendable to other models or pipelines

---

## 🛠️ Tech Stack

| Component    | Model / Tool                         |
|--------------|--------------------------------------|
| ASR + LLM    | [`fixie-ai/ultravox-v0_5`](https://huggingface.co/fixie-ai/ultravox-v0_5-llama-3_1-8b) |
| TTS          | [`hexgrad/Kokoro-82M`](https://huggingface.co/hexgrad/Kokoro-82M) |
| UI           | [Gradio](https://gradio.app)         |
| Language     | Python 3.10+                         |

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/voice2voice-2phase-ai.git
cd voice2voice-2phase-ai
