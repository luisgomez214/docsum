# Document Summarizer

[![](https://github.com/luisgomez214/docsum/workflows/tests/badge.svg)](https://github.com/luisgomez214/docsum/actions?query=workflow%3Atests)

Use an LLM to summarize a document on the command line.

## Setup

Create a python virtual environment for packages.
```
$ python3 -m venv venv
$ . ./venv/bin/activate
$ echo venv > .gitignore
```

Install packages.
```
$ pip3 install groq fulltext
$ pip3 freeze > requirements.txt
``` 

Create a .env file and add your GROQ_API_KEY
```
GROQ_API_KEY=your_api_key_here
```

```
$ export $(cat .env)
```

## Usage

```
$ python3 docsum.py <file_path>
```

For example:
```
$ python3 docsum.py docs/'declaration'

This is a summary of the file 'docs/declaration': Here is a summary of the text in one sentence, written at a 1st-grade reading level:

A long time ago, some people decided to create a new country called America, and they wrote a letter to each other explaining why they wanted to be free from another country, Great Britain

```

