import os
from openai import OpenAI
from openai import AzureOpenAI
import json
from simpleaitranslator.exceptions import MissingAPIKeyError, NoneAPIKeyProvidedError, InvalidModelName
from simpleaitranslator.utils.enums import ChatGPTModel
from simpleaitranslator.utils.function_tools import tools_get_text_language, tools_translate

CHATGPT_MODEL = ChatGPTModel.GPT_4o.value
client = None

def set_openai_api_key(api_key):
    if not api_key:
        raise NoneAPIKeyProvidedError()
    global client
    client = OpenAI(api_key=api_key)

def set_azure_openai_api_key(azure_endpoint, api_key, api_version, azure_deployment):
    if not api_key:
        raise NoneAPIKeyProvidedError()
    if not azure_deployment:
        raise ValueError('azure_deployment is required - current value is None')
    if not api_version:
        raise ValueError('api_version is required - current value is None')
    if not azure_endpoint:
        raise ValueError('azure_endpoint is required - current value is None')
    global client
    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
        azure_deployment=azure_deployment
    )

def set_chatgpt_model(chatgpt_model_name):
    """In this function you can change default chatgpt model"""
    def validate_model(model_to_check: str) -> None:
        if model_to_check not in {model.value for model in ChatGPTModel}:
            raise InvalidModelName(invalid_model_name=model_to_check)

    global CHATGPT_MODEL
    if type(chatgpt_model_name) ==ChatGPTModel:
        CHATGPT_MODEL = chatgpt_model_name.value
    elif type(chatgpt_model_name) == str and validate_model(chatgpt_model_name):
        CHATGPT_MODEL = chatgpt_model_name
    else:
        raise ValueError('chatgpt_model name is required - current value is None or have wrong format')



def get_text_language(text):
    global client
    if not client:
        raise MissingAPIKeyError()
    messages = [
        {"role": "system", "content": "You are a language detector. You should return the ISO 639-3 code to the get_from_language function of user text."},
        {"role": "user", "content": text}
    ]

    response = client.chat.completions.create(
        model=CHATGPT_MODEL,
        messages=messages,
        tools=tools_get_text_language,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    if tool_calls:
        #print(tool_calls)
        tool_call = tool_calls[0]
        function_args = json.loads(tool_call.function.arguments)
        return function_args.get("iso639_3")

    return None


def translate(text, to_language):
    global client
    if not client:
        raise MissingAPIKeyError()
    messages = [
        {"role": "system", "content": f"You are a language translator. You should translate the text to the {to_language} language and then put result of the translation to the translate_to_language function"},
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(
        model=CHATGPT_MODEL,
        messages=messages,
        tools=tools_translate,
        tool_choice="auto",
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    #print(tool_calls)
    #print(response_message)
    if tool_calls:
        #print(tool_calls)
        tool_call = tool_calls[0]
        function_args = json.loads(tool_call.function.arguments)
        return function_args.get("translated_text")
    return None








