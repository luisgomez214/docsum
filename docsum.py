def split_document_into_chunks(text):
    '''
    Split the input text into smaller chunks so that an LLM can process those chunks individually.

    >>> split_document_into_chunks('This is a sentence.\n\nThis is another paragraph.')
    ['This is a sentence.', 'This is another paragraph.']
    >>> split_document_into_chunks('This is a sentence.\n\nThis is another paragraph.\n\nThis is a third paragraph.')
    ['This is a sentence.', 'This is another paragraph.', 'This is a third paragraph.']
    >>> split_document_into_chunks('This is a sentence.')
    ['This is a sentence.']
    >>> split_document_into_chunks('')
    []
    >>> split_document_into_chunks('This is a sentence.\n')
    ['This is a sentence.']
    >>> split_document_into_chunks('This is a sentence.\n\n')
    []
    >>> split_document_into_chunks('This is a sentence.\n\nThis is another paragraph.\n\n')
    ['This is a sentence.', 'This is another paragraph.']
    '''
    return text.split('\n\n')


if __name__ == '__main__':
    import os
    from groq import Groq
    import argparse

    # Parse command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # Initialize the Groq client with the API key from the environment
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    # Read the file
    with open(args.filename) as f:
        text = f.read()

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

