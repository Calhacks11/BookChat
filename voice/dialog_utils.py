from voice.deepgram_util import speak


def rotate_character_narration(characters):
    n_dialogs = sum([len(character['dialogues']) for character in characters])
    n_characters = len(characters)
    for i in range(n_dialogs):
        i_character = i % n_characters
        character = characters[i_character]
        jth_dialog = int(i / n_characters)
        speak(character['dialogues'][jth_dialog], character['gender'])
