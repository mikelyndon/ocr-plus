import os
import logging
import openai
import tiktoken
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

path = "/path/to/journal/entries/"
logger.debug(path)

encoding = tiktoken.get_encoding("p50k_base")
encoding = tiktoken.encoding_for_model("text-davinci-003")


def get_text_files(path):
    """
    Returns a list of txt files in a folder given a path to that folder.
    """
    logger.debug(f"Fetching all files in: { path }")
    text_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            text_files.append(os.path.join(path, file))
    return text_files


def read_text_from_file(file_path):
    """
    opens the text file and returns its contents as a raw string.
    """
    logger.debug(f"Reading: { file_path }")
    with open(file_path, "r") as f:
        return f.read()


def get_file_parts(file_path):
    """
    Returns a tuple of the folder, filename, and extension when given the full path to the file.
    """
    folder = os.path.dirname(file_path)
    filename, extension = os.path.splitext(os.path.basename(file_path))
    return folder, filename, extension


def write_string_to_file(string, folder, filename, extension):
    """
    Writes a string to a file with the suffix "gpt" given the folder, filename, and extension.
    """
    new_filename = filename + "-gpt" + extension
    new_file_path = os.path.join(folder, "gpt", new_filename)
    logger.debug(f"Writing to file_path: { new_file_path }")
    with open(new_file_path, "w") as f:
        f.write(string)

# Replace these with your own hashtags
hashtags = [
    "expectations",
    "goals",
    "gym",
    "mindfulness",
    "passion",
    "relationships",
    "travel",
    "work",
    "awareness",
]


def engineer_prompt(entry):
    """
    Given a journal entry as a string, the function returns a structured prompt.
    """
    return f'''You are a note formatter and summarizer. You format notes as Markdown and fix grammar and spelling to match British English.  If a word doesn't make sense in the context of a sentence, replace only that word with another that fits the context of the sentence. Do not change the meaning of the sentence. Then, append a 3 bullet summary to the end of the note and any hashtags that represent themes for the note from the following list: { hashtags }

    Original Journal Entry:"""
    { entry }
    """

    Formatted Journal Entry:
    '''


text_files = get_text_files(path)
logger.debug(text_files)


def process_batch(text_file_batch):
    for text_file in text_file_batch:
        folder, filename, extension = get_file_parts(text_file)
        new_filename = filename + "-gpt" + extension
        new_file_path = os.path.join(folder, "gpt", new_filename)
        if os.path.exists(new_file_path):
            logger.info(f"{filename} has already been processed.")
            continue
        entry = read_text_from_file(text_file)
        entry_tokens = len(encoding.encode(entry))
        logger.debug(f"Current file: { filename }, tokens: { entry_tokens }\n")
        if entry_tokens * 2 + 200 > 4096:
            logger.warning(f"{filename} exceeds the token count")
            continue

        prompt = engineer_prompt(entry)

        retries = 3
        success = False

        while not success and retries > 0:
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    max_tokens=2148,
                    temperature=0,
                )
                success = True
            except TimeoutError:
                retries -= 1
                if retries > 0:
                    logger.info(
                        f"TimeoutError occurred. Retrying... ({retries} retries remaining)"
                    )
                    time.sleep(5)
                else:
                    logger.info(
                        f"TimeoutError occurred. All retries failed. Skipping {filename}."
                    )

        if success:
            write_string_to_file(response.choices[0].text, folder, filename, extension)


batch_size = 10
total_files = len(text_files)
num_batches = (total_files + batch_size - 1) // batch_size

for i in range(num_batches):
    start = i * batch_size
    end = min((i + 1) * batch_size, total_files)
    logger.info(f"Process batch {i+1} of {num_batches}")
    text_files_batch = text_files[start:end]
    process_batch(text_files_batch)
    logger.info(f"Batch {i + 1} complete.")