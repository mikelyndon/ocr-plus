This repository contains a Python script that processes a list of files and sends their text content along with a prompt to the ChatGPT API to generate a response.

The prompt:

> You are a note formatter and summariser. You format notes as Markdown and fix grammar and spelling to match British English. If a word doesn't make sense in the context of a sentence, replace only that word with another that fits the context of the sentence. Do not change the meaning of the sentence. Then, append a 3 bullet summary to the end of the note and any hashtags that represent themes for the note from the following list: [ hashtags ]

Please note that this repository is provided "as is" without any warranty or guarantee of functionality. Use at your own risk. This script is for educational purposes and should be adapted to fit your specific needs.

## Requirements

To use this script, you'll need Python 3.10+, an openai dev account, and the following packages:

- openai
- tiktoken

You can install the required packages using the following command:

```bash
pip install openai tiktoken
```

## Usage

1. Clone this repository:

```bash
git clone https://github.com/mikelyndon/ocr-plus.git
```

2. Change to the repository directory:

```bash
cd ocr-plus
```

3. Export the following variable to set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_ORG="your_org_id_here"
```

4. Run the script:

```bash
python main.py
```

This command will process the text from all files in a given folder, and send the content along with the given prompt to the ChatGPT API. The script will then display the API response on the terminal.
