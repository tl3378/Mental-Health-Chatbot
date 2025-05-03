# Mental Health Support Chatbot

A supportive AI chatbot designed to provide emotional support and mental health assistance in a safe, anonymous digital space.

## Features

- GPT-4o powered conversational AI
- Beautiful bubble-style chat interface
- Emotion and MBTI analysis
- Content moderation and crisis detection
- Emergency resources integration
- Coreference resolution for better understanding

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd Mental-Health-Chatbot
```

2. Create and activate a conda environment:
```bash
conda create -n mental-health-chatbot python=3.12
conda activate mental-health-chatbot
```

3. Install dependencies:
```bash
conda install streamlit
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
- Copy `conversationchain/model.env.example` to `conversationchain/model.env`
- Add your OpenAI API key to `model.env`

## Usage

Run the chatbot:
```bash
streamlit run app.py
```

## Project Structure

```
Mental-Health-Chatbot/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── conversationchain/      # Core chatbot functionality
│   ├── __init__.py
│   ├── config.py          # Configuration and API setup
│   ├── app_setup.py       # Conversation chain setup
│   ├── chatbot_fn.py      # Main chatbot functions
│   ├── coreference.py     # Coreference resolution
│   ├── moderation.py      # Content moderation
│   └── model.env          # API keys (not in git)
└── README.md              # This file
```

## Important Notes

- This chatbot is not a substitute for professional mental health care
- Always seek professional help in case of emergency
- The chatbot includes crisis detection and emergency resources
- All conversations are anonymous and not stored

## License

[Your License Here]
