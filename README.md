# AI Meeting Notes Agent

## Overview

An AI-powered Meeting Notes Agent that analyzes meeting transcripts and extracts:

- Meeting Summary
- Key Decisions
- Action Items
- Owner
- Due Date

## Demo

![Application Screenshot](screenshots/results_page.png)

## Prerequisites

- Python 3.10 or above
- Groq API key
- Internet connection

## Features

- Upload `.txt` meeting transcripts
- AI summarization
- Action item extraction
- JSON download
- Streamlit UI

## Tech Stack

- Python
- Streamlit
- Groq API
- JSON

## Project Structure

```
meeting_agent/
├── agents/
│   └── meeting_agent.py
├── data/
│   ├── meeting1.txt
│   ├── meeting2.txt
│   ├── meeting3.txt
│   ├── client_meeting.txt
│   └── scrum_meeting.txt
├── output/
├── screenshots/
├── services/
│   └── groq_service.py
├── streamlit_app.py
├── config.py
├── prompts.py
├── requirements.txt
├── tests/
├── utils.py
├── .env.example
└── .env
```

## Installation

## 1. Clone the repository

```bash
git clone https://github.com/saisanket232/meeting-notes-ai-agent.git
```

## 2. Navigate to the project

```bash
cd meeting-notes-ai-agent
```

## 3. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Create a `.env` file

Create a file named `.env` in the project root and add:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:

https://console.groq.com/keys

## 6. Run the application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## Usage

1. Launch the Streamlit application.
2. Upload a `.txt` meeting transcript.
3. Click **Analyze Meeting**.
4. View the meeting summary, key decisions, and action items.
5. Download the generated JSON report.

## Sample Files

The `data/` folder contains sample meeting transcripts:

- `meeting1.txt`
- `meeting2.txt`
- `meeting3.txt`
- `client_meeting.txt`
- `scrum_meeting.txt`

You can upload any of these files to test the application.
```

## Sample Output

![Home page](screenshots/home_page.png)

![Uploaded transcript](screenshots/uploaded_transcript.png)

![Results page](screenshots/results_page.png)

![JSON download button](screenshots/json_download_button.png)

## Future Improvements

- PDF Support
- DOCX Support
- Email Integration
- Calendar Integration
