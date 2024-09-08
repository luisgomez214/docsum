import os
from groq import Groq
import argparse
import fulltext
import chardet
import time

def split_document_into_chunks(text, chunk_size=5000):
    """
    Split text into smaller chunks so an LLM can process those chunks individually.

    Args:
        text (str): The input text to split into chunks.
        chunk_size (int): The maximum size of each chunk in terms of characters.

    Returns:
        List[str]: A list of text chunks.
    """
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def get_text_from_file(filename):
    try:
        # Try using fulltext to extract text from the file
        return fulltext.get(filename)
    except (UnicodeDecodeError, Exception) as e:
        print(f"fulltext failed: {e}")
        print("Attempting to detect encoding with chardet...")

        # Fallback to using chardet to detect encoding and read the file
        try:
            with open(filename, 'rb') as f:
                result = chardet.detect(f.read())
                charenc = result['encoding']
                print(f"Detected encoding: {charenc}")

                # Read the file with the detected encoding
                with open(filename, 'r', encoding=charenc) as f:
                    return f.read()
        except Exception as e:
            print(f"Failed to read the file even after detecting encoding: {e}")
            exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='Path to the file to be summarized')
    args = parser.parse_args()

    # Initialize Groq client with API key
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Get text from the file
    text = get_text_from_file(args.filename)

    # Split the document into smaller chunks
    chunks = split_document_into_chunks(text)

    # Initialize an empty list to hold individual summaries
    summaries = []

    # Retry mechanism parameters
    max_retries = 3
    retry_delay = 5  # in seconds

    # Iterate over each chunk and generate a summary for each
    for chunk in chunks:
        for attempt in range(max_retries):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": "Summarize the input text below. Limit the summary to 1 sentence and use a 1st-grade reading level.",
                        },
                        {
                            "role": "user",
                            "content": chunk,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                # Append the generated summary to the list
                summaries.append(chat_completion.choices[0].message.content)
                break  # Break out of retry loop if successful
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Skipping this chunk.")

    # Join all summaries into one final summary
    final_summary = f"This is a summary of the file '{args.filename}': " + " ".join(summaries)
    print(final_summary)

if __name__ == "__main__":
    main()

