from llm.gemini import query_prompt
import ast

def query_characters(content):
    query = content + (
        '\nTell me the unique characters, their possible genders, and personality attributes in the above conversation.'
        '\nGive me the response in the following python dictionary schema:\n'
        'Character = {"character_name" : str, "gender": "male/female", "personality": list[str], "dialogues": list[str]}\n'
        'Return: list[Character]\n'
        'where dialogues is a list of dialogues spoken by respective characters.'
        )
    prompt_response = query_prompt(query)
    first_ind = prompt_response.find('[')
    last_ind = prompt_response.rfind(']')
    prompt_response = prompt_response[first_ind:last_ind + 1]
    prompt_response = ast.literal_eval(prompt_response)
    return prompt_response

