import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
prompt_file = '/Users/amitthakur/PycharmProjects/BookChat/prompts/conversation-1.txt'

def query_prompt(query_lines):
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    # lines = read_prompt(prompt_file)
    response = chat.send_message(query_lines)
    return response.text

def read_prompt(file_path):
    with open(file_path, 'r') as file:
        # Read all lines into a list
        lines = file.readlines()
        return lines

def main():
    model = genai.GenerativeModel('gemini-1.5-flash')
    chat = model.start_chat(history=[])
    lines = read_prompt(prompt_file)
    response = chat.send_message(lines)
    print(response.text)


if __name__ == '__main__':
    main()
