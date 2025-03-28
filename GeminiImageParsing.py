from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import numpy as np
import pyautogui
import cv2 as cv

load_dotenv()

client = genai.Client(api_key=os.getenv('api_key'))

model_name = "gemini-2.0-flash"

bounding_box_system_instructions = """
    Return bounding boxes as a JSON array with labels. Never return masks or code fencing. Limit to 25 objects.
    If an object is present multiple times, name them according to their unique characteristic (colors, size, position, unique characteristics, etc..).
      """

safety_settings = [
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_ONLY_HIGH",
    ),
]

import google.generativeai as genai
from PIL import Image

import io
import os
import requests
from io import BytesIO

# @title Plotting Util

# Get Noto JP font to display janapese characters
#!apt-get install fonts-source-han-sans-jp # For Source Han Sans (Japanese)

import json
import random
import io
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageColor


additional_colors = [colorname for (colorname, colorcode) in ImageColor.colormap.items()]

def plot_bounding_boxes(im, bounding_boxes):
    """
    Plots bounding boxes on an image with markers for each a name, using PIL, normalized coordinates, and different colors.

    Args:
        img_path: The path to the image file.
        bounding_boxes: A list of bounding boxes containing the name of the object
         and their positions in normalized [y1 x1 y2 x2] format.
    """

    # Load the image
    img = im
    width, height = img.size
    print(img.size)
    # Create a drawing object
    draw = ImageDraw.Draw(img)

    # Define a list of colors
    colors = [
    'red',
    'green',
    'blue',
    'yellow',
    'orange',
    'pink',
    'purple',
    'brown',
    'gray',
    'beige',
    'turquoise',
    'cyan',
    'magenta',
    'lime',
    'navy',
    'maroon',
    'teal',
    'olive',
    'coral',
    'lavender',
    'violet',
    'gold',
    'silver',
    ] + additional_colors

    # Parsing out the markdown fencing
    bounding_boxes = parse_json(bounding_boxes)
    font = ImageFont.truetype("segoeui.ttf", size=14)

    parsed = []

    # Iterate over the bounding boxes
    for i, bounding_box in enumerate(json.loads(bounding_boxes)):
      # Select a color from the list
      color = colors[i % len(colors)]

      # Convert normalized coordinates to absolute coordinates
      abs_y1 = int(bounding_box["box_2d"][0]/1000 * height)
      abs_x1 = int(bounding_box["box_2d"][1]/1000 * width)
      abs_y2 = int(bounding_box["box_2d"][2]/1000 * height)
      abs_x2 = int(bounding_box["box_2d"][3]/1000 * width)

      x_center = (abs_x1 + abs_x2) / 2
      y_center = (abs_y1 + abs_y2) / 2

      x_center = x_center * (1920 / 1024)
      y_center = y_center * (1080 / 576)

      parsed.append({'label':bounding_box["label"], 'x':x_center, 'y':y_center})

      if abs_x1 > abs_x2:
        abs_x1, abs_x2 = abs_x2, abs_x1

      if abs_y1 > abs_y2:
        abs_y1, abs_y2 = abs_y2, abs_y1

      # Draw the bounding box
      draw.rectangle(
          ((abs_x1, abs_y1), (abs_x2, abs_y2)), outline=color, width=4
      )

      # Draw the text
      if "label" in bounding_box:
        draw.text((abs_x1 + 8, abs_y1 + 6), bounding_box["label"], fill=color, font=font)

    return parsed
    # # Display the image
    # img.show()


# @title Parsing JSON output
def parse_json(json_output):
    # Parsing out the markdown fencing
    lines = json_output.splitlines()
    for i, line in enumerate(lines):
        if line == "```json":
            json_output = "\n".join(lines[i+1:])  # Remove everything before "```json"
            json_output = json_output.split("```")[0]  # Remove everything after the closing "```"
            break  # Exit the loop once "```json" is found
    return json_output

def describe_image(target):
    prompt = f"Detect the 2d boxes. {target}"

    screen = pyautogui.screenshot()
    image = np.array(screen)
    # image = cv.cvtColor(image, cv.COLOR_RGB2BGR)  #убрать это реверсит
    image = cv.resize(image, (1280, 720))

    pil_image = Image.fromarray(image)

    pil_image.save('among us detection.png')

    image = "among us detection.png"

    im = Image.open(image)
    im.thumbnail([620,620], Image.Resampling.LANCZOS)


    # Load and resize image
    im = Image.open(BytesIO(open(image, "rb").read()))
    im.thumbnail([1024,1024], Image.Resampling.LANCZOS)

    # Run model to find bounding boxes
    response = client.models.generate_content(
        model=model_name,
        contents=[prompt, im],
        config = types.GenerateContentConfig(
            system_instruction=bounding_box_system_instructions,
            temperature=0.5,
            safety_settings=safety_settings,
        )
    )

    # Check output
    print(response.text)

    parsed = plot_bounding_boxes(im, response.text)
    for coords in parsed:
        pyautogui.moveTo(coords['x'], coords['y'])
    # im.show()

    return parsed, im

def execute(function, *args):
    return function(*args)


if __name__ == '__main__':
    execute(print, '1', '2')
# parsed = describe_image()