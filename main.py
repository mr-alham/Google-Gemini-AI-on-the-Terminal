#!/bin/env python3
"""This script is to chat with Google Gemini AI"""


from json import JSONDecodeError, load
from os import path
from sys import argv, exit

import google.generativeai as genai
import PIL.Image
from pyperclip import paste


def initialize_genai():
    """Initialize the generative AI module and configuring it."""

    try:
        script_dir = path.dirname(path.realpath(__file__))
        file = path.join(script_dir, "keys.json")

        with open(file, "r", encoding="utf-8") as f:
            content = load(f)
            gemini_api_key = content["GEMINI_API_KEY"]

            if gemini_api_key == "your gemini api key here":
                print("To use the Gemini API, you'll need an API key.")
                print("If you don't already have one,")
                print("create a key in Google AI Studio.'https://aistudio.google.com/app/apikey'")
                print("save the key to 'keys.json' file.")

                exit(1)

            gemini_model = content["GEMINI_MODEL"]
            safety_settings = content["SAFETY_SETTINGS"]
            generation_config = content["GENERATION_CONFIG"]

            genai.configure(api_key=gemini_api_key)

    except FileNotFoundError:
        print("Could not find the configuration file 'keys.json', Ensure it exists")

        exit(1)

    except JSONDecodeError:
        print(
            "Error: Could not parse the key file 'keys.json'. Please check the file format."
        )

        exit(1)

    except KeyError as e:
        print(f"Error: Missing key '{e.args[0]}' in 'keys.json' file.")

        exit(1)

    except Exception as e:
        print("an exception occurred as: ", e)

        exit(1)

    model = genai.GenerativeModel(
        model_name=gemini_model,
        safety_settings=safety_settings,
        generation_config=generation_config,
    )  # TOOLS, TOOL_CONFIG, SYSTEM_INSTRUCTIONS

    return model


def response_with_images():
    """when need a response with a image"""

    while True:
        image_file = input("The path to the image ('clip' to copy from the clipboard or press 'enter' key): ")

        if image_file == "clip" or image_file == "":
            image_file = paste()

        if path.exists(image_file):
            query = input("Query: ")
            model = initialize_genai()

            response = model.generate_content(
                [query, PIL.Image.open(image_file)], stream=False
            )

            print(response.text)

        else:
            print(f"Error: Couldn't find the image '{image_file}'.")
            print("Try again.\n")

            continue


def main():
    """main logic of the script is happening here"""

    if len(argv) > 1:
        if "--image" in argv:
            response_with_images()
        else:
            print(f"Error: Unknown argument: {argv[1]}")

            exit(1)

    model = initialize_genai()

    chat = model.start_chat(history=[])

    while True:
        query = input("what do you need to ask: ")

        try:
            response = chat.send_message(query, stream=False)
            print(response.text)

        except genai.RequestError as e:
            print(
                f"Error: An error occurred while communicating with the Gemini API. ({e})"
            )

        except ValueError:
            print(response.prompt_feedback)
            print(response.candidates[0].finish_reason)
            print(response.candidates[0].safety_ratings)
            print()

        print("***" * 60)
        print("\n")

    # for chunk in response:
    # print(chunk.text)


if __name__ == "__main__":
    main()
