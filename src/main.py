import os
import logging
import openai

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

openai.organization = "org-7nwdPqlTUuLWkI2mo6By8voi"
openai.api_key = os.getenv("OPENAI_API_KEY")

path = "/Users/mike/Documents/dev/openai/ocr-plus/test"
logger.debug(path)


def get_text_files(path):
    """
    Returns a list of txt files in a folder given a path to that folder.
    """
    logger.debug(f"Fetching all files in: { path }")
    text_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            print("file:", file)
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
    new_file_path = os.path.join(folder, new_filename)
    logger.debug(f"Writing to file_path: { new_file_path }")
    with open(new_file_path, "w") as f:
        f.write(string)

def engineer_prompt(entry):
    """
    Given a journal entry as a string, the function returns a structured prompt.
    """
    return f'''
    You are an OCR note formatter and summarizer. If a word doesn't make sense in the context of a sentence replace it with the most likely word given the context. You format notes as Markdown and fix grammar and spelling. Then you append a 3 bullet summary to the end of the note and 5 hashtags that represent themes for the note.

    Original Journal Entry:"""
    { entry }
    """

    Formatted Journal Entry:
    '''


text_files = get_text_files(path)
print(text_files)
# test_file = list(text_files)[0]
logger.debug(text_files)
for text_file in text_files:
    folder, filename, extension = get_file_parts(text_file)
    entry = read_text_from_file(text_file)
    # logger.debug(f"Entry: { entry }")

# entry = """
# starting to feel better. Not drinking is less of a focus and I can start building again. Last night probably helped because it was relatively busy and ended with a great group call. Bataan earlier than that it was interesting how energised I felt after the call with Ana. I attribute it to leaving work at 4pm so my work day was shorter and I moved into a new environment with some down time on the streetcar. Maybe that's it and maybe I really enjoy helping people and the call itself energised me. Either way it turned out to be a pretty good day. I'm a little bummed about Sasha. We'll have to see how things play out but I got the sense she made the call more out of obligation. I don't know exactly what I want out of this but I would like some sense that da wants to invest in this. I don't particularly want to maintain a friendship where we might see each other once a month. Thats probably the same thing that's upsetting me about Julie. I don't think we can call each other friends if we never actually do anything together outside of work. I know she's got a lot going on with her non, but I'm pretty sore she still has time to see friends. I could ask myself what am I doing to make that happen and I guess to start answer is nothing. So I could also try making plans and see how she responds. Maybe invite her to the book signing.
# So Japan trip coming up. What do I need to be aware of a pot in place to look after myself? Not drinking is definitely one. Staying in touch with friends-Ali, Goldie, Julia. My mom. I think its okay to reach out to them over the course of the trip. Can I reframe it through beginner's eyes? Instead of seeing the people, locations and events as something I've done before, see it fresh. It is wholly different, so treat it that way. A little fearful of whatever is going on in my groin. Its not my appendix. But it doesn't quite feel like muscle pain. I should sort out my healthcare. Cad go to the dentists. Dining is the first step. Woo exercise and diet. Then meditation and mindfulness, Icm doing the meditating so that pot is less of a concern. So where do I want to go for the rest of the ya? Sounds like I'm going to Belgium with Julie. Then Denmark and Sweden with Paul. From there I could go to Spain for November. I tell start quietening down but that's fine. And then, if I'm kicky card I figure out my finances) I could surprise my mom and go to South Africa. If I did go I should probably visit kin and Ali. That's a lot of flights that could add up to a lot of money. Lets plan it out and take it from there. I thi k thats all I've got for now. Im going to have an early start. I am going to setup some fire. and then relax tonight. Because I deserve it.
# """

    prompt = engineer_prompt(entry)
# print(prompt)
    response = openai.Completion.create(
        model="text-davinci-003", prompt=prompt, max_tokens=1600, temperature=0
    )
    # response = "boop"
    logger.debug(f"Response: {response}")
    write_string_to_file(response.choices[0].text, folder, filename, extension)
    # write_string_to_file(response, folder, filename, extension)

# print(response.choices[0].text)
