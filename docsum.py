import os
from groq import Groq
import argparse
import chardet

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

    # Call split_document_into_chunks on the text
    chunks = split_document_into_chunks(text)

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

