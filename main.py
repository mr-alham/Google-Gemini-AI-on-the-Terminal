#!/bin/env python3
"""This script is to chat with Google Gemini AI"""


import json
import os
import re
import sys

import google.generativeai as genai
from google.api_core import exceptions
import PIL.Image
import pyperclip as clipboard
from colors import ansi


def format_text(text: str) -> str:
    """format the markdown formatted file with ansi codes"""

    # code
    code_pattern = ''

    patterns = {
        # code snippet
        r"```(?P<content>.*?)```": [ansi(["bright_cyan"]), ansi(["white"])],
        # bold_italic
        r"\*\*\*(?P<content>.*?)\*\*\*": [ansi(["bold", "italic"]), ansi(["white"])],
        # bold
        r"\*\*(?P<content>.*?)\*\*": [ansi(["bold", "yellow"]), ansi(["white"])],
        # italic
        r"\*(?P<content>.*?)\*": [ansi(["italic",]), ansi(["white"])],  # used to be cyan
        # headings
        r"^#{1,6}(?P<content>.*)": [ansi(["bold", "underline", "bright_yellow"]), ansi(["white"])],
        # un ordered lists
        r"^\* (?P<content>.*?)": ["\u2022", ""],
        # strikethrough
        r"\~\~(?P<content>.*?)\~\~": [ansi(["strikethrough"]), ansi(["white"])],
        # blockquote
        # r"^\>.?(?P<content>.*)": [ansi(["bright_black", "white_bg"]), ansi(["white"])],  # some problem with blockquote
        # blockquote
        # r"^\>(?P<content>.*?)": [ansi(["black"]), ansi(["white_bg", "reset"])],
        # code
        r"\s\`(?P<content>.*?)\`\s": [" " + ansi(["dim", "bright_green"]), ansi(["white"]) + " "],
    }

    other_patterns = {
        # digits  *something is going wrong with the digits
        # r"\b(\d+)\b": [ansi(["yellow"]),ansi(["reset", "yellow","white"])],
        # url
        r"(https?://\S+|www\.\S+)":
            [ansi(["blue", "underline", "italic"]), ansi(["reset", "white"])],
    }

    for key, value in other_patterns.items():
        matches = re.finditer(key, text, re.MULTILINE)

        for match in matches:
            formatted_text = value[0] + match.group(0) + value[1]
            text = text.replace(match.group(0), formatted_text)

    for key, value in patterns.items():
        matches = re.finditer(key, text, re.MULTILINE)

        for match in matches:
            formatted_text = value[0] + match.group("content") + value[1]
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

    print(ansi(["dim", "bright_yellow", "bold"]))
    print("You are using Text-to-Text(T2T) Model.")
    print("Enter 'Image Mode' to turn to Image/text Model")
    print(ansi(["dim", "bold", "bright_cyan"]), end="")
    print("─" *(os.get_terminal_size().columns - 1), ansi([]))

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
            print(ansi([]))
            print(format_text(response.text) + ansi([]))

        except exceptions.DeadlineExceeded as error:
            print(ansi(["bold", "red"]) + "Deadline exceeded (Internet connection could be lost)")
            print("Or the deadline is shorter:" + ansi(["dim", "red"]))
            print(error.message, "\n")

            continue

        except exceptions.InvalidArgument as error:
            print(ansi(["bold", "red"]) + "Request fails API validation, or you tried to access a model that requires" , end = "")
            print("allowlisting or is disallowed by the organization's policy:" + ansi(["dim", "red"]))
            print(error.message, "\n")

            sys.exit(1)

        except exceptions.PermissionDenied as error:
            print(ansi(["bold", "red"]) + "Client doesn't have sufficient permission to call the API:" + ansi(["dim", "red"]))
            print(error.message, "\n")

            sys.exit(1)

        except exceptions.NotFound as error:
            print(ansi(["bold", "red"]) + "No valid object is found from the designated URL:" + ansi(["dim", "red"]))
            print(error.message, "\n")

            sys.exit(1)

        except exceptions.ResourceExhausted as error:
            print(ansi(["bold", "red"]) + "Depending on the error message, the error could be caused by the following:")
            print("1. API quota over the limit.\n2. Server overload due to shared server capacity." + ansi(["dim", "red"]))
            print(error.message, "\n")

            sys.exit(1)

        except exceptions.Unknown as error:
            print(ansi(["bold", "red"]) + "Server error due to overload or dependency failure:" + ansi(["dim", "red"]))
            print(error.message, "\n")

            sys.exit(1)

        except exceptions.ServiceUnavailable as error:
            print(ansi(["bold", "red"]) + "Service is temporarily unavailable:" + ansi(["dim", "red"]))
            print(error.message, "\n")

            sys.exit(1)

        print(ansi(["bold", "bright_magenta"]) + "─" *
              (os.get_terminal_size().columns - 2), ansi([]))
        # print()


def response_with_images():
    """Input: text/image  ->  output: text"""

    print(ansi(["dim", "bright_yellow", "bold"]), end = "")
    print("You are using MultiModel Model.", end = "")
    print("Enter 'Text Mode' to turn to Text-to-Text Model")
    print(ansi(["dim", "bold", "bright_cyan"]), end = "")
    print("─" *(os.get_terminal_size().columns - 1), ansi([]))

    while True:
        print(ansi(["green", "bold"]) + "The path to the image ", end = "")
        print(ansi(["green", "bold", "dim"]), end = "")
        print("(Enter 'clip' or press 'enter' key to copy from the Clipboard): ", end = "")
        print(ansi(["white"]), end='')

        image_file = input()

        if image_file == "Text Mode":
            print(ansi([]))
            text_to_text()

        if image_file in ("clip", ""):
            image_file = clipboard.paste()

        if os.path.exists(image_file):
            print(ansi(["green", "bold"]) + "Prompt: " + ansi(["white"]), end="")
            query = input()
            model = initialize_genai()

            try:
                response = model.generate_content(
                    [query, PIL.Image.open(image_file)],
                    stream=False, request_options={"timeout": 40})

                print(format_text(response.text), ansi([]))

            except PIL.UnidentifiedImageError:
                print(ansi(["bold", "red"]) + "Cannot identify the image file:", end = " ")
                print(ansi(["dim", "red"]) + image_file + ansi([]), "\n")

                continue

            except exceptions.DeadlineExceeded as error:
                print(ansi(["bold", "red"]) + "Deadline exceeded (Internet connection could be lost)")
                print("Or the deadline is shorter:" + ansi(["dim", "red"]))
                print(error.message, "\n")

                continue

            except exceptions.InvalidArgument as error:
                print(ansi(["bold", "red"]) + "Request fails API validation, or you tried to access a model that requires ", end = "")
                print("allowlisting or is disallowed by the organization's policy:" + ansi(["dim", "red"]))
                print(error.message, "\n")

                sys.exit(1)

            except exceptions.PermissionDenied as error:
                print(ansi(["bold", "red"]) + "Client doesn't have sufficient permission to call the API:" + ansi(["dim", "red"]))
                print(error.message, "\n")

                sys.exit(1)

            except exceptions.NotFound as error:
                print(ansi(["bold", "red"]) + "No valid object is found from the designated URL:" + ansi(["dim", "red"]))
                print(error.message, "\n")

                sys.exit(1)

            except exceptions.ResourceExhausted as error:
                print(ansi(["bold", "red"]) + "Depending on the error message, the error could be caused by the following:")
                print("1. API quota over the limit.\n2. Server overload due to shared server capacity.", end = "")
                print(ansi(["dim", "red"]), error.message, "\n")

                sys.exit(1)

            except exceptions.Unknown as error:
                print(ansi(["bold", "red"]) + "Server error due to overload or dependency failure:" + ansi(["dim", "red"]),
                      error.message, "\n")

                sys.exit(1)

            except exceptions.ServiceUnavailable as error:
                print(ansi(["bold", "red"]) + "Service is temporarily unavailable:" + ansi(["dim", "red"]),
                      error.message, "\n")

                sys.exit(1)

        else:
            print(ansi(["bold", "red"]), end = "")
            print(f"Error: Not a valid file path:{ansi(["dim", "bright_red"])}'{image_file}'.", end = "")
            print(ansi(["bold", "red"]), "\nTry again.\n")

            continue

        print("\n", ansi(["bold", "bright_magenta"]) + "─" *
              (os.get_terminal_size().columns - 1), ansi([]))


def main():
    """main logic of the script is happening here"""

    os.system("clear -x")

    size = os.get_terminal_size()
    phrase = "Gemini-AI on Terminal by ALHAM"
    space = (int(size.columns) - len(phrase))/2

    # print(ansi(["dim", "yellow", "bold"]), "-" * (size.columns - 3), ansi([]))
    print(ansi(["bold", "bright_red"]) + "`" *
          os.get_terminal_size().columns, ansi([]), end="")
    print(" " * int(space) +
          ansi(["bright_cyan", "bold"]) + phrase + "\n", ansi([]))
    print(ansi(["bold", "bright_red"]) + "`" *
          os.get_terminal_size().columns, ansi([]))

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

        print("\n", ansi(["bold", "bright_red"]) + "─" *
              (os.get_terminal_size().columns - 1), ansi([]))

        print(f"{string:^{os.get_terminal_size().columns - 6}}")

        s = int((os.get_terminal_size().columns/2) - 12)

        print(" " * s + r"     .--.  ")
        print(" " * s + r"    |o_o |  ")
        print(" " * s + r"    |:_/ |  ")
        print(" " * s + r"   //   \ \  ")
        print(" " * s + r"  (|     | )  ")
        print(" " * s + r" /'\_   _/`\  ")
        print(" " * s + r" \___)=(___/  ")
        print("\n", ansi(["bold", "bright_red"]) + "─" *
              (os.get_terminal_size().columns - 1), ansi([]))

        print(ansi([]))

        sys.exit(0)
