# Google Gemini-AI Chat Interface on Terminal
Engage with Google's Gemini AI directly from your terminal with vibrant colored outputs. Seamlessly switch between text queries and interactive image inputs for a dynamic AI interaction experience. Perfect for Linux Enthusiasts, developers and AI enthusiasts alike!

## Features
  - **Terminal-Based Interface**  - Interact with Google's Gemini AI directly from the comfort of yor Terminal.
  - **MultiModel Support**  - Ability to Input Images and Text.
  - **Text-to-Text(T2T) Model**  - Engage in conversations by entering text queries and receiving text responses.
  - **ANSI Formatting**  - Enhanced user experience with colorful text outputs.
  - **Dynamic Interactions**  - Seamless switching between text and Image modes for versitile interactions.
  - **Configuration**  - Easily configure settings through 'keys.json' file including API key.

## Prerequisites
### API Key
  - To use the Gemini API, you need an API key. You can easily create a key with one click on Google AI Studio. To read the documentaion visit [ai.google.dev](https://ai.google.dev/gemini-api/docs).
  
  - To get the API key visit [Google AI Studio](https://makersuite.google.com/app/apikey)
  
### Softwares
- Pyhon 3.x
- Pip
  
### Dependencies
  - `google-generativeai` Enables developers to use Google's state-of-the-art generative AI models to build AI-powered features and applications.
     ```bash
     pip install google-generativeai
     ```
     
  - `pillow` Library gives image processing capabilities.
    ```bash
    pip install pillow
    ```
    
  - `pyperclip` Is a cross-platform Python module to interact with clipboard
    ```bash
    pip install pyperclip
    ```

## Installation
```bash
git clone https://github.com/mr-alham/Google-Gemini-AI-on-the-Terminal.git
```
```bash
pip install -r requirements.txt
```

## Configurations (`keys.json`)
- **API key**
  - Locate the `key.json` file in this project's directory.
  - Inside the file, you'll find a line that looks like this:
    ```json
    "GEMINI_API_KEY": "your gemini key here"
    ```
  - Replace "your gemini key here" with the API key you obtained in above step, Be sure to keep the quotation marks around your key.
  - Save the key.json file.
 
- **Gemini Model** *not required
  
  - The Gemini API offers different models that are optimized for specific use cases.
  - Read the [documentation](https://ai.google.dev/gemini-api/docs/models/gemini) and select your preferred one.
  - The Default model is `gemini-1.5-pro-latest`

- **Safety Settings & Generation Configuration** *not required
  - Read the documentaion and edit at your will
  - [Model Parameters Documentaion](https://ai.google.dev/api/python/google/generativeai/GenerativeModel)
  - [Safety Settings Documentaion](https://ai.google.dev/api/python/google/ai/generativelanguage/SafetyRating)
 
## Usage
  Run the script using Python
  ```python
  python3 main.py
  ```

  **Command Line Arguments**
  - `--image` : will start the script in MultiModel mode where you can give a file path and give the prompt.
    

  **Text-to-Text(T2T) Model**
   - If the script didn't get any arguments the script will start with Text-to-Text Model.
   - Using Text-to-Text Model user can develop a conversation with the Gemini.
   - If you need to switch to MultiModel type `Image Mode`

  **MultiMode Model**
   - If the script recieved the argument `--image` then the script will start in MultiMode mode.
   - Or if the query is equla to `Image Mode` on T2T It will redirect to MuliModel.
   - If need to switch to normal mode type `Text Mode` as the file path.

## License
  This project is licensed under the MIT License.

## Contact
  For any inquiries or support, please contact You can contact us at [alham@duck.com](mailto:alham@duck.com).

  Feel free to contribute by submitting pull requests.



