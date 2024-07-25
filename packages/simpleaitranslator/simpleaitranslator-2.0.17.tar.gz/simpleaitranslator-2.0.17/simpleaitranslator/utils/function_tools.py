def translate_to_language(translated_text):
    return translated_text


tools_translate = [
    {
        "type": "function",
        "function": {
            "name": "translate_to_language",
            "description": "Returns the translated text",
            "parameters": {
                "type": "object",
                "properties": {
                    "translated_text": {
                        "type": "string",
                        "description": "The text that has been translated",
                    },
                },
                "required": ["translated_text"],
            },
        },
    }
]


def get_from_language(iso639_3):
    iso639_3 = iso639_3.lower()
    return iso639_3


tools_get_text_language = [
    {
        "type": "function",
        "function": {
            "name": "get_from_language",
            "description": "Retrieve the ISO 639-3 code for a given language",
            "parameters": {
                "type": "object",
                "properties": {
                    "iso639_3": {
                        "type": "string",
                        "description": "The ISO 639-3 code for a language, e.g., 'eng' for English",
                    },
                },
                "required": ["iso639_3"],
            },
        },
    }
]


