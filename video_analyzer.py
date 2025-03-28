# coding=UTF-8
import os
from typing import List
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

os.environ['https_proxy'] = os.getenv('proxy')
client = genai.Client(api_key="AIzaSyAYM2EwkOiTCjJQb709emY9Jnv72pmv0OI")
from IPython.display import Markdown
MODEL_ID = "gemini-1.5-pro"
import pathlib
import time



set_timecodes = types.FunctionDeclaration(
    name="set_timecodes",
    description="Set the timecodes for the video with associated text",
    parameters={
        "type": "OBJECT",
        "properties": {
            "timecodes": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "time": {"type": "STRING"},
                        "text": {"type": "STRING"},
                    },
                    "required": ["time", "text"],
                }
            }
        },
        "required": ["timecodes"]
    }
)

set_timecodes_with_objects = types.FunctionDeclaration(
    name="set_timecodes_with_objects",
    description="Set the timecodes for the video with associated text and object list",
    parameters={
        "type": "OBJECT",
        "properties": {
            "timecodes": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "time": {"type": "STRING"},
                        "text": {"type": "STRING"},
                        "objects": {
                            "type": "ARRAY",
                            "items": {"type": "STRING"},
                        },
                    },
                    "required": ["time", "text", "objects"],
                }
            }
        },
        "required": ["timecodes"],
    }
)

set_timecodes_with_numeric_values = types.FunctionDeclaration(
    name="set_timecodes_with_numeric_values",
    description="Set the timecodes for the video with associated numeric values",
    parameters={
        "type": "OBJECT",
        "properties": {
            "timecodes": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "time": {"type": "STRING"},
                        "value": {"type": "NUMBER"},
                    },
                    "required": ["time", "value"],
                }
            }
        },
        "required": ["timecodes"],
    }
)

set_timecodes_with_descriptions = types.FunctionDeclaration(
    name="set_timecodes_with_descriptions",
    description="Set the timecodes for the video with associated spoken text and visual descriptions",
    parameters={
        "type": "OBJECT",
        "properties": {
            "timecodes": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "time": {"type": "STRING"},
                        "spoken_text": {"type": "STRING"},
                        "visual_description": {"type": "STRING"},
                    },
                    "required": ["time", "spoken_text", "visual_description"],
                }
            }
        },
        "required": ["timecodes"]
    }
)


video_tools = types.Tool(
    function_declarations=[set_timecodes, set_timecodes_with_objects, set_timecodes_with_numeric_values],
)

AnalysisMode = {
            "AV_CAPTIONS": "For each scene in this video, generate captions that "
            "describe the scene along with any spoken text placed in quotation marks. "
            "Place each caption into an object sent to set_timecodes with the timecode of the caption in the video.",

            "PARAGRAPH": "Generate a paragraph that summarizes this video. Keep it to 3 to 5 "
            "sentences. Place each sentence of the summary into an object sent to set_timecodes with the "
            "timecode of the sentence in the video.",


            "AMONG_US": "ПОСМОТРИ ВИДЕО И ОПИШИ КАЖДОЕ ДЕЙСТВИЕ ВСЕХ ИГРОКОВ! ОПИШИ МАКСИМАЛЬНО ТОЧНО И ПОДРОБНО! ДЛЯ КАЖДОЙ СЦЕНЫ В ВИДЕО!"
                        "Generate bullet points for the video. Place each bullet point into an "
                "object sent to set_timecodes with the timecode of the bullet point in the video.",

            "KEY_MOMENTS": "Generate bullet points for the video. Place each bullet point into an "
                "object sent to set_timecodes with the timecode of the bullet point in the video.",

            "TABLE": "Choose 5 key shots from this video and call set_timecodes_with_objects with the "
            "timecode, text description of 10 words or less, and a list of objects visible in the scene "
            "(with representative emojis).",

            "HAIKU": "Generate a haiku for the video. Place each line of the haiku into an object sent "
            "to set_timecodes with the timecode of the line in the video. Make sure to follow the syllable "
            "count rules (5-7-5). СДЕЛАЙ ОЧЕНЬ, ОЧЕНЬ - ОЧЕНЬ ПОДРОБЬНО",

            "CHART": "Generate chart data for this video based on the following instructions: \n"
            "count the number of people. Call set_timecodes_with_numeric_values once with the list "
            "of data values and timecodes.",

            "CUSTOM": "Call set_timecodes once using the following instructions: ",

            "AV_DESCRIPTIONS": "For each scene in this video, generate spoken text and descriptions that "
            "describe the scene along with any spoken text placed in quotation marks. "
            "Place each section into an object sent to set_timecodes_with_descriptions with the timecode of the caption in the video, the spoken text and the visual description. СДЕЛАЙ МАКСИМАЛЬНО ПОДРОБНОЕ ОПИСАНИЕ КАЖДОГО КАДРА!!! МАКСИМАЛЬНО!!! КАЖДОЕ ДЕЙСТВИЕ ПОЛЬЗОВАТЕЛЯ ИЛИ ИГРОКОВ В ИГРЕ!!! ОТВЕТ ДОЛЖЕН БЫТЬ НА РУССКОМ ЯЗЫКЕ! Пример: 'Игрок Саня бежит вверху по направлению к реактору вместе с игроком Кот проходя мимо камер наблюдения около охраны и видит мёртвого зеленого игрока и красного рядом. '"
        }
def set_timecodes_func(timecodes):
    return [{**t, "text": t["text"].replace("\\'", "'")} for t in timecodes]

def set_timecodes_with_objects_func(timecodes):
    return [{**t, "text": t["text"].replace("\\'", "'")} for t in timecodes]

def set_timecodes_with_descriptions_func(timecodes):
    return [{**t, "text": t["spoken_text"].replace("\\'", "'")} for t in timecodes]

video_tools = types.Tool(
    function_declarations=[set_timecodes,
                           set_timecodes_with_objects,
                           set_timecodes_with_numeric_values,
                           set_timecodes_with_descriptions]
)


def process_video(AnalysisModePrompt: AnalysisMode, custom_prompt: str = None):
    global MODEL_ID
    file_upload = client.files.upload(file='videos/video-small.mp4')
    # Prepare the file to be uploaded
    while file_upload.state == "PROCESSING":
        print('Waiting for video to be processed.')
        # time.sleep(0.1)
        file_upload = client.files.get(name=file_upload.name)

    if file_upload.state == "FAILED":
        raise ValueError(file_upload.state)
    print(f'Video processing complete: ' + file_upload.uri)

    print(file_upload.state)

    SYSTEM_PROMPT = "When given a video and a query, call the relevant function only once with the appropriate timecodes and text for the video"
    USER_PROMPT = "For each scene in this video, generate captions that describe the scene along with any spoken text placed in quotation marks. Place each caption into an object sent to set_timecodes with the timecode of the caption in the video."

    response = client.models.generate_content(
    model=MODEL_ID,
    contents=[
        types.Content(
            role="user",
            parts=[
                types.Part.from_uri(
                    file_uri=file_upload.uri,
                    mime_type=file_upload.mime_type),
                ]),
        AnalysisModePrompt,
        ],
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[video_tools],
        temperature=0,
        )
    )
    try:
        uploaded_files = client.files.list()
        for file in uploaded_files:
            client.files.delete(name=file.name)
    except:
        pass

    if response.candidates[0].content.parts[0].function_call.name == "set_timecodes":
        return set_timecodes_func(response.candidates[0].content.parts[0].function_call.args['timecodes'])
    elif response.candidates[0].content.parts[0].function_call.name == "set_timecodes_with_objects":
        return set_timecodes_with_objects_func(response.candidates[0].content.parts[0].function_call.args['timecodes'])
    elif response.candidates[0].content.parts[0].function_call.name == "set_timecodes_with_descriptions":
        return  response.candidates[0].content.parts[0].function_call.args
    else:
        return response

# print(process_video(AnalysisModePrompt=AnalysisMode['HAIKU']))