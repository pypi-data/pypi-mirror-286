# CAN.01 Chatbot

This is a chatbot project developed in Python. The chatbot, named Ming, is a 40-year-old pilot from Hong Kong who speaks Cantonese fluently. Ming loves sharing travel experiences and stories, and is passionate about different cultures and foods.

## Features

- Real-time speech recognition using Google Cloud Speech-to-Text
- Generates responses using OpenAI's GPT-3.5 model
- Converts text responses to Cantonese speech using Google Cloud Text-to-Speech
- Continuous listening and response capabilities

## Requirements

- Python 3.6 or higher
- Google Cloud service account with Speech-to-Text and Text-to-Speech APIs enabled
- OpenAI API key

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/can_01_chatbot.git
    cd can_01_chatbot
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    - Set your OpenAI API key:

        ```python
        openai.api_key = 'your_openai_api_key'
        ```

    - Set the path to your Google Cloud service account key JSON file:

        ```bash
        export GOOGLE_APPLICATION_CREDENTIALS="path/to/SA_Carefirst.json"
        ```

## Usage

1. **Run the chatbot**:

    ```bash
    python can_01_chatbot/can01.py
    ```

2. **Interaction**:

    - The program will start listening for your speech input.
    - Once it recognizes your speech, it will generate a response using the OpenAI GPT-3.5 model.
    - The response will be converted to Cantonese speech and played back.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- **Michelle** - *Initial work* - [YourGitHubProfile](https://github.com/yourusername)

## Acknowledgements

- Special thanks to [Contributor1](https://github.com/contributor1) for their help.

## Additional Information

- **Google Cloud Speech-to-Text**: [Documentation](https://cloud.google.com/speech-to-text/docs)
- **Google Cloud Text-to-Speech**: [Documentation](https://cloud.google.com/text-to-speech/docs)
- **OpenAI GPT-3**: [Documentation](https://beta.openai.com/docs/)

