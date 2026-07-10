from services.gemini_service import ask_gemini
from prompts import MEETING_SYSTEM_PROMPT


def analyze_meeting(transcript):

    prompt = f"""
{MEETING_SYSTEM_PROMPT}

Meeting Transcript:

{transcript}
"""

    return ask_gemini(prompt)