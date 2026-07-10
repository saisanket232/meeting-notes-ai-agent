# AI Meeting Notes Agent

## Overview

An AI-powered Meeting Notes Agent that analyzes meeting transcripts and extracts:

- Meeting Summary
- Key Decisions
- Action Items
- Owner
- Due Date

## Features

- Upload `.txt` meeting transcripts
- AI summarization
- Action item extraction
- JSON download
- Streamlit UI

## Tech Stack

- Python
- Streamlit
- Gemini API
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
│   └── gemini_service.py
├── streamlit_app.py
├── config.py
├── prompts.py
├── requirements.txt
├── tests/
├── utils.py
└── .env
```

## Installation

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
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
