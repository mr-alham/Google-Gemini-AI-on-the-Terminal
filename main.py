#!/bin/env python3
"""This script is to chat with Google Gemini AI"""

import google.generativeai as genai
from json import load
import PIL.Image


def main():
    try:
        with open("keys.json", "r") as f:
            content = load(f)
            GEMINI_API_KEY = content["GEMINI_API_KEY"]
            GEMINI_MODEL = content["GEMINI_MODEL"]
            SAFETY_SETTINGS = content["SAFETY_SETTINGS"]
            GENERATION_CONFIG = content["GENERATION_CONFIG"]

            genai.configure(api_key=GEMINI_API_KEY)

    except Exception as e:  # TODO: handle exceptions thoroughly
        print("an exception occurred as: ", e)

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        safety_settings=SAFETY_SETTINGS,
        generation_config=GENERATION_CONFIG
    )  # TOOLS, TOOL_CONFIG, SYSTEM_INSTRUCTIONS

    # response = model.generate_content(["describe the image",PIL.Image.open("b.jpg")], stream=False)
    # print(response.text)
    # print()

    chat = model.start_chat(history=[])
    while True:
        q = input('what do you need to ask: ')
        response = chat.send_message(q, stream=False)

        try:
            print(response.text)
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
