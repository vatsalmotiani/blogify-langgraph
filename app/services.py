import re
from typing import Tuple
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_ollama import ChatOllama

from .prompts import generate_blog_post_prompt, generate_outline_prompt


load_dotenv()


def extract_video_id(url: str) -> str:
    """Extracting Video ID from YouTube URL"""
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})",
        r"youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url


def get_transcript_from_youtube(
    url: str, preferred_languages: list | None = None
) -> Tuple[str, str]:
    """Fetching transcript for a YouTube video. Returns (transcript, language)."""
    if preferred_languages is None:
        preferred_languages = [
            "en",
            "es",
            "fr",
            "de",
            "it",
            "pt",
            "ru",
            "ja",
            "ko",
            "zh",
            "hi",
        ]

    try:
        video_id = extract_video_id(url)
        ytt_api = YouTubeTranscriptApi()

        try:
            fetched_transcript = ytt_api.fetch(video_id, languages=preferred_languages)
            language_code = getattr(
                fetched_transcript, "language_code", preferred_languages[0]
            )
            language = getattr(fetched_transcript, "language", "Unknown")
        except Exception:
            transcript_list = ytt_api.list(video_id)
            available_transcripts = [
                {
                    "language": t.language,
                    "code": t.language_code,
                    "is_generated": t.is_generated,
                }
                for t in transcript_list
            ]
            if not available_transcripts:
                return ("", "No transcript available")

            first_transcript = transcript_list.find_transcript(
                [available_transcripts[0]["code"]]
            )
            fetched_transcript = first_transcript.fetch()
            language_code = available_transcripts[0]["code"]
            language = available_transcripts[0]["language"]

        transcript_parts = [snippet.text for snippet in fetched_transcript]
        transcript = " ".join(transcript_parts)
        return (
            transcript.strip() if transcript else "",
            f"{language} ({language_code})",
        )
    except Exception as e:
        error_message = str(e)
        if ("NoTranscriptFound" in error_message) or (
            "TranscriptsDisabled" in error_message
        ):
            return (
                "",
                "No transcript available. Please ensure the video has subtitles or automatic captions enabled.",
            )
        return ("", f"Error extracting transcript: {error_message}")


def generate_outline(
    transcript: str, blog_language: str, feedback: str | None = None
) -> str:
    """Generating blog post outline"""
    llm = ChatOllama(model="llama3", temperature=0.7, num_predict=1500)
    prompt = generate_outline_prompt(
        transcript=transcript, blog_language=blog_language, feedback=feedback
    )
    return llm.invoke(prompt).content


def generate_blog_post(transcript: str, blog_language: str, outline: str) -> str:
    """Generating blog post"""
    llm = ChatOllama(model="llama3", temperature=0.7, num_predict=2000)
    prompt = generate_blog_post_prompt(
        transcript=transcript, blog_language=blog_language, outline=outline
    )
    return llm.invoke(prompt).content
