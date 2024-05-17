#!/bin/env python3
"""This script is to chat with Google Gemini AI"""

import google.generativeai as genai
from json import load, JSONDecodeError
import PIL.Image
from sys import exit, argv
from os import path

def initialize_genai():
    """Initialize the generative AI module and configuring it."""

    try:
        script_dir = path.dirname(path.realpath(__file__))
        file = path.join(script_dir, "keys.json")

        with open(file, "r") as f:
            content = load(f)
            GEMINI_API_KEY = content["GEMINI_API_KEY"]
            GEMINI_MODEL = content["GEMINI_MODEL"]
            SAFETY_SETTINGS = content["SAFETY_SETTINGS"]
            GENERATION_CONFIG = content["GENERATION_CONFIG"]

            genai.configure(api_key=GEMINI_API_KEY)

    except FileNotFoundError:
        print("Could not find the configuration file \'keys.json\', Ensure it exists")

        exit(1)

    except JSONDecodeError:
        print(
            "Error: Could not parse the key file 'keys.json'. Please check the file format.")

        exit(1)

    except KeyError as e:
        print(f"Error: Missing key '{e.args[0]}' in 'keys.json' file.")

        exit(1)

    except Exception as e:
        print("an exception occurred as: ", e)

        exit(1)

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG
    )  # TOOLS, TOOL_CONFIG, SYSTEM_INSTRUCTIONS

    return model


def response_with_images():
    """when need a response with a image"""

    while True:
        image_file = input("The path to the image: ")

        if path.exists(image_file):
            query = input("Query: ")
            model = initialize_genai()

            response = model.generate_content([query, PIL.Image.open(image_file)], stream=False)

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
        q = input('what do you need to ask: ')

        try:
            response = chat.send_message(q, stream=False)
            print(response.text)

        except genai.RequestError as e:
            print(f"Error: An error occurred while communicating with the Gemini API. ({e})")

        except ValueError:
            print(response.prompt_feedback)
            print(response.candidates[0].finish_reason)
            print(response.candidates[0].safety_ratings)
            print()

        print("***" * 60)
        print("\n")

    # for chunk in response:
        # print(chunk.text)


if __name__ == '__main__':
    main()
