import openai
import tiktoken
import os
import logging
from typing import List, Tuple
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Instantiate the OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chunk_text(text: str, max_tokens: int = 14000) -> List[str]:
    """
    Split the text into chunks of approximately the specified token size.

    Args:
        text (str): The input text to be chunked.
        max_tokens (int): The approximate number of tokens per chunk.

    Returns:
        List[str]: A list of text chunks.
    """
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    tokens = encoding.encode(text)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
    
    return chunks

def summarize_chunk(chunk: str, model: str = "gpt-4o-mini", max_tokens: int = 4000) -> Tuple[str, str]:
    """
    Summarize a chunk of text using OpenAI's GPT-4o-mini.

    Args:
        chunk (str): The text chunk to summarize.
        model (str): The model to use for summarization.
        max_tokens (int): The maximum number of tokens to generate in the summary.

    Returns:
        Tuple[str, str]: The summary and table of contents.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes and provides a detailed table of contents with consistent timestamps in hh:mm:ss format."},
                {"role": "user", "content": f"Please summarize the following text and provide a table of contents with timestamps in hh:mm:ss format. Return the summary and table of contents separately, divided by '---TOC---':\n\n{chunk}"}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )
        result = response.choices[0].message.content.strip()
        # Check if the separator exists in the response
        if '---TOC---' in result:
            summary, toc = result.split('---TOC---')
        else:
            # If no separator, assume everything is summary
            summary = result
            toc = "No table of contents provided."
        return summary.strip(), toc.strip()

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Error in summarizing text.", "No table of contents due to error."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "Unexpected error in summarizing text.", "No table of contents due to error."

def combine_summaries(summaries: List[str], tocs: List[str]) -> Tuple[str, str]:
    """
    Combine multiple summaries and tables of contents into a single summary and TOC.

    Args:
        summaries (List[str]): List of summaries.
        tocs (List[str]): List of tables of contents.

    Returns:
        Tuple[str, str]: The combined summary and table of contents.
    """
    combined_text = "\n\n".join(summaries) + "\n\n" + "\n\n".join(tocs)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that combines multiple summaries and tables of contents into a single, coherent summary and table of contents."},
                {"role": "user", "content": f"Please combine the following summaries and tables of contents into a single, coherent summary and table of contents. Ensure the table of contents has consistent timestamps in hh:mm:ss format. Return the summary and table of contents separately, divided by '---TOC---':\n\n{combined_text}"}
            ],
            max_tokens=4000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        result = response.choices[0].message.content.strip()
        # Check if the separator exists in the response
        if '---TOC---' in result:
            final_summary, final_toc = result.split('---TOC---')
        else:
            # If no separator, assume everything is summary
            final_summary = result
            final_toc = "No table of contents provided."
        
        return final_summary.strip(), final_toc.strip()

    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Error in combining summaries.", "No table of contents due to error."
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "Unexpected error in combining summaries.", "No table of contents due to error."

def summarize_text(text: str) -> str:
    """
    Summarize the given text, chunking it if necessary.

    Args:
        text (str): The input text to be summarized.

    Returns:
        str: The summarized text with a single summary and table of contents.
    """
    chunks = chunk_text(text)
    summaries = []
    tocs = []

    for idx, chunk in enumerate(chunks):
        # Log the progress of summarizing chunks
        logger.info(f"Summarizing chunk {idx + 1}/{len(chunks)}")
        # summary = summarize_chunk(chunk)
        summary, toc = summarize_chunk(chunk)
        summaries.append(summary)
        if toc != "No table of contents provided.":
            tocs.append(toc)
        # Log the first 500 characters of each summary for inspection
        logger.info(f"Chunk {idx + 1} summary: {summary[:500]}...")

    if len(summaries) > 1:
        logger.info("Combining multiple summaries and tables of contents.")
        final_summary, final_toc = combine_summaries(summaries, tocs)
    else:
        final_summary, final_toc = summaries[0], tocs[0] if tocs else "No table of contents provided."
        
     # Process the final_toc to ensure correct timestamps
    if final_toc != "No table of contents provided.":
        final_toc = process_toc(final_toc)
        
    # Format the output
    output = "Summary:\n" + final_summary.strip()
    if final_toc != "No table of contents provided.":
        output += "\n\nTable of Contents:\n" + final_toc.strip()
        
    return output

def process_toc(toc: str) -> str:
    """
    Process the table of contents to ensure correct timestamps.

    Args:
        toc (str): The original table of contents.

    Returns:
        str: The processed table of contents with correct timestamps.
    """
    lines = toc.split('\n')
    processed_lines = []
    current_hour = 0

    for line in lines:
        if ' - ' in line:
            timestamp, content = line.split(' - ', 1)
            hours, minutes, seconds = map(int, timestamp.split(':'))
            
            # Adjust hours if they reset to 00
            if hours == 0 and current_hour > 0:
                current_hour += 1
            else:
                current_hour = hours

            new_timestamp = f"{current_hour:02d}:{minutes:02d}:{seconds:02d}"
            processed_lines.append(f"{new_timestamp} - {content}")
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)

if __name__ == "__main__":
    # For testing purposes
    test_text = "Your long text here..."
    summary = summarize_text(test_text)
    print(summary)