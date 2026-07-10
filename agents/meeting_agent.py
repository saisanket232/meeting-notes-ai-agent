from services.groq_service import ask_groq
from prompts import MEETING_SYSTEM_PROMPT


def analyze_meeting(transcript):

    prompt = f"""
{MEETING_SYSTEM_PROMPT}

Meeting Transcript:

{transcript}
"""

    return ask_groq(prompt)