#!/bin/env python3
"""This script is to chat with Google Gemini AI"""


import json
import os
import re
import sys

import google.generativeai as genai
import PIL.Image
import pyperclip as clipboard
from colors import ansi


def format_text(text: str) -> str:
    """format the markdown formatted file with ansi codes"""
    patterns = {
        # code
        r"```(?P<content>.*?)```": [ansi(["black_bg"]), ansi(["white"])],
        # bold_italic
        r"\*\*\*(?P<content>.*?)\*\*\*": [ansi(["bold", "italic"]), ansi(["white"])],
        # bold
        r"\*\*(?P<content>.*?)\*\*": [ansi(["bold", "yellow"]), ansi(["white"])],
        # italic
        r"\*(?P<content>.*?)\*": [ansi(["italic", "cyan"]), ansi(["white"])],
        # code
        r"\`(?P<content>.*?)\`": [ansi(["dim", "bright_green"]), ansi(["white"])],
        # blockquote
        r"^\>.?(?P<content>.*)": [ansi(["bright_black", "white_bg"]), ansi(["white"])],
        # headings
        r"^#{1,6}(?P<content>.*)": [ansi(["dim", "bold", "underline", "magenta"]), ansi(["white"])],
        # headings
        # r"#{1,6}(?P<content>.*)": [ansi(["red"]), ansi(["reset", "white"])],
        # blockquote
        r"^\>(?P<content>.*?)": [ansi(["black"]), ansi(["white_bg", "reset"])],
        # un ordered lists
        r"^\* (?P<content>.*?)": ["\u2022", ""],
        # strikethrough
        r"\~\~(?P<content>.*?)\~\~": [ansi(["strikethrough"]), ansi(["white"])],
    }

    other_patterns = {
        # digits  *something is going wrong with the digits
        # r"\b(\d+)\b": [ansi(["yellow"]),ansi(["reset", "yellow","white"])],
        # url
        r"(https?://\S+|www\.\S+)":
            [ansi(["blue", "underline", "italic"]), ansi(["reset", "white"])],
    }

    for pattern in other_patterns.keys():
        matches = re.finditer(pattern, text, re.MULTILINE)

        for match in matches:
            formatted_text = other_patterns[pattern][0] + \
                match.group(0) + other_patterns[pattern][1]
            text = text.replace(match.group(0), formatted_text)

    for pattern in patterns.keys():
        matches = re.finditer(pattern, text, re.MULTILINE)

        for match in matches:
            formatted_text = patterns[pattern][0] + \
                match.group("content") + patterns[pattern][1]
            text = text.replace(match.group(0), formatted_text)

    return text


def initialize_genai():
    """Initialize the generative AI module and configuring it."""

    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(script_dir, "keys.json")

        with open(file, "r", encoding="utf-8") as f:
            content = json.load(f)
            gemini_api_key = content["GEMINI_API_KEY"]

            if gemini_api_key == "your gemini api key here":
                print("To use the Gemini API, you'll need an API key.")
                print("If you don't already have one,")
                print(
                    "create a key in Google AI Studio.'https://aistudio.google.com/app/apikey'")
                print("save the key to 'keys.json' file.")

                sys.exit(1)

            gemini_model = content["GEMINI_MODEL"]
            safety_settings = content["SAFETY_SETTINGS"]
            generation_config = content["GENERATION_CONFIG"]

            genai.configure(api_key=gemini_api_key)

    except FileNotFoundError:
        print("Could not find the configuration file 'keys.json', Ensure it exists")

        sys.exit(1)

    except json.JSONDecodeError:
        print(
            "Error: Could not parse the key file 'keys.json'. Please check the file format.")

        sys.exit(1)

    except KeyError as e:
        print(f"Error: Missing key '{e.args[0]}' in 'keys.json' file.")

        sys.exit(1)

    except Exception as e:
        print("an exception occurred as: ", e)

        sys.exit(1)

    model = genai.GenerativeModel(
        model_name=gemini_model,
        safety_settings=safety_settings,
        generation_config=generation_config,
    )  # TOOLS, TOOL_CONFIG, SYSTEM_INSTRUCTIONS

    return model


def text_to_text():
    """Input: text  ->  output: text"""

    print(ansi(["dim", "bright_yellow", "bold"]),
          "You are using Text-to-Text(T2T) Model.\
            \n Enter 'Image Mode' to turn to Image/text Model", ansi([]))

    model = initialize_genai()

    chat = model.start_chat(history=[])

    while True:
        query = input(ansi(["green", "bold"])+"Ask Me: "+ansi(["white"]))

        if query == "" or query.isspace():
            print(ansi(["dim", "red"]) + "The query is empty.\n")
            continue

        if query == "Image Mode":
            print(ansi([]))
            response_with_images()

        try:
            response = chat.send_message(query, stream=False)
            print(ansi(["green", "bold"]) + "Response: ", ansi(["white"]))
            print(format_text(response.text)+ansi([]))

        except ValueError:
            print(response.prompt_feedback)
            print(response.candidates[0].finish_reason)
            print(response.candidates[0].safety_ratings)
            print()

        print(ansi(["dim", "bold", "blue"])+"_ " *
              int(os.get_terminal_size().columns/2))


def response_with_images():
    """Input: text/image  ->  output: text"""

    print(ansi(["dim", "bright_yellow", "bold"]),
          "You are using MultiModel Model.\
            \n WEnter 'Text Mode' to turn to Text-to-Text Model", ansi([])
          )

    while True:
        print(ansi(["green", "bold"]) + "The path to the image " +
              ansi(["green", "bold", "dim"]) +
              "(Enter 'clip' or press 'enter' key to copy from the Clipboard): " +
              ansi(["white"]), end=''
              )
        image_file = input()

        if image_file == "Text Mode":
            print(ansi([]))
            text_to_text()

        if image_file in ("clip", ""):
            image_file = clipboard.paste()

        if os.path.exists(image_file):
            print(ansi(["green", "bold"]) +
                  "Prompt: " + ansi(["white"]), end="")
            query = input()
            model = initialize_genai()

            response = model.generate_content(
                [query, PIL.Image.open(image_file)],
                stream=False
            )

            print(format_text(response.text), ansi([]))

        else:
            print(f"{ansi(["bold", "red"])}Error: Not a valid file path:{
                  ansi(["dim", "bright_red"])}'{image_file}'."
                  )
            print("Try again.\n")

            continue


def main():
    """main logic of the script is happening here"""

    os.system("clear -x")

    size = os.get_terminal_size()
    phrase = "Gemini-AI on Terminal by ALHAM"
    space = (int(size.columns) - len(phrase))/2

    # print(ansi(["dim", "yellow", "bold"]), "-" * (size.columns - 3), ansi([]))
    print(" " * int(space) + ansi(["bright_cyan", "bold"]) + phrase + ansi([]))

    if len(sys.argv) > 1:
        if "--image" in sys.argv:
            response_with_images()
        else:
            print(f"Error: Unknown argument: {sys.argv[1]}")

            sys.exit(1)

    text_to_text()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:

        string = ansi(["bold", "bright_red"]) + \
            "___ See ya! ___" + ansi(["bold", "bright_white"])

        print(f"{string:^{os.get_terminal_size().columns - 6}}")

        s = int((os.get_terminal_size().columns/2) - 12)

        print(" " * s + r"     .--.  ")
        print(" " * s + r"    |o_o |  ")
        print(" " * s + r"    |:_/ |  ")
        print(" " * s + r"   //   \ \  ")
        print(" " * s + r"  (|     | )  ")
        print(" " * s + r" /'\_   _/`\  ")
        print(" " * s + r" \___)=(___/  ")

        print(ansi([]))

        sys.exit(0)
