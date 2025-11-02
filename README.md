# Blogify - YouTube to Blog Post Converter

Python application that converts YouTube videos into blog posts using LangGraph.

<img width="1487" height="766" alt="image" src="https://github.com/user-attachments/assets/b1717592-3212-4189-af66-2fc50f549f1e" />

## Overview

1. Extract transcripts from YouTube videos
2. Generate blog posts from video content
3. Support multiple output languages

Can be used via both a command-line interface and Streamlit

## Features

- Extract transcripts from YouTube videos using the YouTube Transcript API
- Generate blog posts in multiple languages
- Automatic language detection for video transcripts
- Markdown-formatted output with proper headings and structure
- Two interfaces: CLI and Streamlit web UI

## Project Structure

```
blogify-langgraph/
├── app/                   # Core application logic
│   ├── graph.py           # LangGraph workflow definition
│   ├── main.py            # CLI entry point
│   ├── prompts.py         # LLM prompt templates
│   └── services.py        # Business logic
├── frontend/              # Streamlit web interface
│   └── streamlit_app.py   # Web UI entry point
└── requirements.txt       # Python package dependencies
```

## Architecture

### LangGraph Workflow

1. **Extract Transcript Node**: Fetches the transcript from the YouTube video URL
2. **Generate Blog Post Node**: Converts the transcript into a formatted blog post using OpenAI

The state (`AgentState`) tracks:

- YouTube URL
- Extracted transcript
- Transcript language
- Target blog language
- Generated blog post

### Services

- **Transcript Extraction**: Uses `youtube-transcript-api` to fetch video transcripts with automatic language detection
- **Blog Generation**: Uses OpenAI's `gpt-4o-mini` model via LangChain to generate structured blog posts

## Setup

### Prerequisites

- Python 3.12 or higher
- OpenAI API key

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd blogify-langgraph
```

2. Install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Command Line Interface

Run the CLI application:

```bash
python -m app.main
```

You will be prompted to:

1. Enter a YouTube video URL
2. Select the output language (defaults to English)

The generated blog post will be printed to the console.

### Streamlit Web Interface

Launch the web interface:

```bash
streamlit run frontend/streamlit_app.py
```

The web interface provides:

- Input field for YouTube URL
- Language selector dropdown
- Generate button
- Markdown preview of the generated blog post
- Download button to save the blog post as a `.md` file

## Dependencies

- **langchain**: LLM framework and abstractions
- **langgraph**: Workflow orchestration for agentic applications
- **langchain-openai**: OpenAI integration for LangChain
- **youtube-transcript-api**: YouTube transcript extraction
- **streamlit**: Web interface framework
- **python-dotenv**: Environment variable management
