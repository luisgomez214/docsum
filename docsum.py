import os
from groq import Groq
import argparse
import fulltext
import chardet
import time

def split_document_into_chunks(text, chunk_size=5000):
    """
    Split text into smaller chunks for LLM processing.
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def get_text_from_file(filename):
    """
    Extract text from a file using fulltext or fallback to chardet for encoding detection.
    """
    try:
        return fulltext.get(filename)
    except Exception as e:
        print(f"fulltext failed: {e}. Attempting chardet...")

        try:
            with open(filename, 'rb') as f:
                encoding = chardet.detect(f.read())['encoding']
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            print(f"Failed to read file: {e}")
            exit(1)

def summarize_chunk(client, chunk, retries=3, delay=5):
    """
    Summarize a chunk of text using the Groq API with retry logic.
    """
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Summarize the input text below. Limit the summary to 1 sentence and use a 1st grade reading level."},
                    {"role": "user", "content": chunk}
                ],
                model="llama3-8b-8192"
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print("Max retries reached. Skipping this chunk.")
                return None

def main():
    # Parse command-line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to the file to be summarized')
    args = parser.parse_args()

    # Initialize Groq client
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Extract text from the input file
    text = get_text_from_file(args.filename)

    # Split document into chunks
    chunks = split_document_into_chunks(text)

    # Summarize each chunk and collect the summaries
    summaries = [summarize_chunk(client, chunk) for chunk in chunks if chunk]

    # Combine the summaries into a final summary
    final_summary = f"This is a summary of the file '{args.filename}': " + " ".join(summaries)
    print(final_summary)

if __name__ == "__main__":
    main()
