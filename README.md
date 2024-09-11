# Document Summarizer

[![](https://github.com/luisgomez214/docsum/workflows/tests/badge.svg)](https://github.com/luisgomez214/docsum/actions?query=workflow%3Atests)

Use an LLM to summarize a document on the command line.

# DocSum

**DocSum** is a Python command-line tool that takes a document of any type (PDF, text, etc.) as input and generates a summary using the [Groq API](https://console.groq.com/docs/openai). The tool uses Groq's API, compatible with OpenAI, for text summarization.

## Features

- Summarizes documents in various formats (PDF, text, etc.).
- Automatically detects and processes text using fulltext and Groq API.
- Supports command-line execution.

## Installation

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd docsum
    ```

2. Create a Python virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Add your Groq API key:
    ```bash
    export GROQ_API_KEY='your-api-key'
    ```

## Usage

To summarize a document, run the following command:

```bash
python docsum.py <your-file>


EX:
```
$ python3 docsum.py docs/'declaration'

Here is a summary of the text in one sentence, written at a 1st-grade reading level:

A long time ago, some people decided to create a new country called America, and they wrote a letter to each other explaining why they wanted to be free from another country, Great Britain

```

