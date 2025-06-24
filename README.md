# tdd-generator

## AI-Powered Tech Article Generators

This repository contains **two different Streamlit applications** for generating high-quality technology articles using AI language models powered by Ollama.

---

### 1. Simple Ollama Article Generator (`main.py`)

A straightforward Streamlit app that generates a tech article based on a user topic, word count, and target audience using the Ollama LLaMA 3.2 model.

- **Input:** Topic, word count, and target audience.
- **Output:** A concise, engaging technology article tailored for the specified audience.
- **Model:** `llama3.2:1b-instruct-fp16` via Ollama API.
- **Usage:** Best for quick article generation with minimal complexity.

### Run

```bash
pip install streamlit ollama
streamlit run main.py
```


### Multi-Agent Ollama Article Generator (`main2.py`)

An advanced Streamlit app leveraging the LangChain framework and Ollama's Mistral model to generate detailed tech articles via a two-step multi-agent process:

- **Research Agent:** Performs in-depth research on the topic.
- **Writer Agent:** Crafts an engaging article based on the research.

Features a progress bar and markdown output with an option to download the article.

- **Model:** `mistral` via Ollama API.
- **Technology:** LangChain prompts and chains for multi-step generation.

### Run

```bash
pip install streamlit langchain langchain-community ollama
streamlit run main2.py
