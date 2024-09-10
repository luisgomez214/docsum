
import os
from groq import Groq
import argparse
import chardet

# Function to split the document into chunks of a manageable size
def split_document_into_chunks(text, max_chunk_size=1000):
    """
    Split the input text into smaller chunks of a manageable size.
    
    Args:
        text (str): The input text to split.
        max_chunk_size (int): Maximum character length for each chunk.
    
    Returns:
        list: A list of text chunks.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) < max_chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph + "\n\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Function to detect encoding
def detect_encoding(filename):
    with open(filename, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

if __name__ == '__main__':
    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # Initialize the Groq client with the API key from the environment
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Detect encoding
    encoding = detect_encoding(args.filename)

    try:
        # Open the file with the detected encoding
        with open(args.filename, 'r', encoding=encoding, errors='replace') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading the file: {e}")
        exit(1)

    # Split document into manageable chunks
    chunks = split_document_into_chunks(text, max_chunk_size=1000)

    # List to hold summaries of each chunk
    summaries = []

    # Summarize each chunk
    for chunk in chunks:
        if chunk.strip():  # Skip empty chunks
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        'role': 'system',
                        'content': 'Summarize the input text below. Limit the summary to 1 paragraph and use a 1st grade reading level.',
                    },
                    {
                        'role': 'user',
                        'content': chunk,
                    }
                ],
                model="llama3-8b-8192",
            )
            summaries.append(chat_completion.choices[0].message.content)

    # Combine the summaries into a smaller document
    smaller_document = ' '.join(summaries)

    # Summarize the smaller document
    final_summary = client.chat.completions.create(
        messages=[
            {
                'role': 'system',
                'content': 'Summarize the input text below. Limit the summary to 1 paragraph and use a 1st grade reading level.',
            },
            {
                'role': 'user',
                'content': smaller_document,
            }
        ],
        model="llama3-8b-8192",
    )

    # Print the final summary
    print(final_summary.choices[0].message.content)

