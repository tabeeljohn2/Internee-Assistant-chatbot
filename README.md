# Internee Assistant

An automated support chatbot for Internee.pk interns. It answers common questions about task submission, certificates, assigned tasks and support contacts, and it is clear with users that they are talking to an automated assistant, not a person.

## Overview

Internee Assistant combines three layers so that answers are accurate and the bot never invents information:

1. **Dialogflow intents** handle the common, well-defined questions with approved answers.
2. **An honest fallback** replies with a safe message when the question is not understood, instead of guessing.
3. **A restricted LLM fallback** answers other questions using only the facts in `backend/data/knowledge.txt`. Where a fact is not confirmed (for example, fees), the bot says so.

## Features

- Dialogflow agent with 12 intents and a custom fallback
- Flask REST API with a single `/chat` endpoint and per-session conversation IDs
- LLM fallback limited to a curated knowledge file
- Safe, non-committal answer for unconfirmed topics such as fees
- Responsive chat interface (desktop and mobile) with a welcome screen, animated avatar and typing indicator
- Automated test suite
- Secrets kept out of version control

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Conversation engine | Google Dialogflow |
| Fallback model | OpenAI-compatible LLM client |
| Frontend | HTML, CSS, vanilla JavaScript |
| Testing | pytest |

## Project Structure

```
internee-chatbot/
├── backend/
│   ├── app/
│   │   └── main.py            # Flask app and chat logic
│   ├── data/
│   │   └── knowledge.txt      # Approved facts for the LLM fallback
│   ├── tests/
│   │   └── test_api.py        # API tests
│   ├── list_models.py         # Helper to list available models
│   └── requirements.txt
├── frontend/
│   ├── index.html             # Chat interface
│   ├── robot.gif              # Welcome-screen avatar
│   └── bot.gif                # Chat avatar
├── start-backend.bat          # Windows shortcut to run the backend
├── start-frontend.bat         # Windows shortcut to run the frontend
└── .gitignore
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A Google Cloud project with a Dialogflow agent and a service-account key
- An API key for the LLM provider used by the fallback

### 1. Clone the repository

```bash
git clone https://github.com/tabeeljohn2/Internee-Assistant-chatbot.git
cd Internee-Assistant-chatbot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

Create `backend/.env` (this file is git-ignored) and place your Google service-account key inside `backend/secrets/` (also git-ignored).

```
LLM_API_KEY=your-llm-api-key
LLM_BASE_URL=your-llm-base-url
ALLOWED_ORIGINS=http://127.0.0.1:3000
# plus your Dialogflow project ID and the path to your service-account key,
# using the variable names expected in backend/app/main.py
```

**Never commit `.env` or anything in `backend/secrets/`.**

### 4. Run the backend

```bash
cd backend
..\venv\Scripts\python.exe -m flask --app app.main run --port 5000 --debug
```

### 5. Run the frontend

In a second terminal:

```bash
cd frontend
..\venv\Scripts\python.exe -m http.server 3000
```

Open <http://127.0.0.1:3000> in your browser.

## API

### `POST /chat`

**Request**

```json
{
  "message": "How do I submit a task?",
  "session_id": "a-unique-session-id"
}
```

**Response**

```json
{
  "reply": "..."
}
```

## Testing

```bash
cd backend
..\venv\Scripts\python.exe -m pytest -p no:cacheprovider
```

## Deployment

The backend is intended for a Python web host such as Render, and the frontend for any static host. After deploying:

1. Set `API_URL` in `frontend/index.html` to the deployed backend address.
2. Set `ALLOWED_ORIGINS` on the backend to the deployed frontend address.
3. Add `LLM_API_KEY`, `LLM_BASE_URL` and the Dialogflow credentials as private environment settings on the host, never in the repository.

## Security Notes

- Secrets are loaded from environment variables and ignored by Git.
- The assistant identifies itself as automated and directs account issues to the Internee.pk website.
- Answers for unconfirmed topics are deliberately cautious rather than guessed.

## Author

Built by [tabeeljohn2](https://github.com/tabeeljohn2) as part of the Internee.pk internship program.

