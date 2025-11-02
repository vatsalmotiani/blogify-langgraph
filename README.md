# Blogify - YouTube to Blog Post Converter

Python application that converts YouTube videos into blog posts using LangGraph.

<img width="1487" height="766" alt="image" src="https://github.com/user-attachments/assets/b1717592-3212-4189-af66-2fc50f549f1e" />

## Overview

1. Extract transcripts from YouTube videos
2. Generate blog post outlines for user review
3. Allow user approval or feedback for outline modifications
4. Generate final blog posts based on approved outlines
5. Support multiple output languages

## Features

- Extract transcripts from YouTube videos using the YouTube Transcript API
- Generate blog post outlines with interactive approval/feedback workflow
- Modify outlines based on user feedback before generating final blog posts
- Generate blog posts in multiple languages
- Automatic language detection for video transcripts
- Markdown-formatted output with proper headings and structure
- Streamlit web UI for easy interaction

## Project Structure

```
blogify-langgraph/
├── app/                   # Core application logic
│   ├── graph.py           # LangGraph workflow definition
│   ├── prompts.py         # LLM prompt templates
│   └── services.py        # Business logic
├── frontend/              # Streamlit web interface
│   └── streamlit_app.py   # Web UI entry point
└── requirements.txt       # Python package dependencies
```

## Architecture

### LangGraph Workflow

1. **Extract Transcript Node**: Fetches the transcript from the YouTube video URL
2. **Generate Outline Node**: Creates a blog post outline from the transcript
3. **Check Approval Node**: Routes based on user approval status
4. **Generate Blog Post Node**: Converts the approved outline into a formatted blog post using Ollama

<img width="408" height="703" alt="blogify-mermaid-v1" src="https://github.com/user-attachments/assets/c640be23-4a1a-41de-b6e1-2d837b40bc7c" />

The workflow supports an interactive feedback loop:

- After generating an outline, users can approve it to proceed with blog post generation
- Users can also reject the outline and provide feedback for modifications
- The outline is regenerated based on user feedback until approved

The state (`AgentState`) tracks:

- YouTube URL
- Extracted transcript
- Transcript language
- Target blog language
- Generated outline
- User feedback for outline modifications
- Approval status
- Generated blog post

### Services

- **Transcript Extraction**: Uses `youtube-transcript-api` to fetch video transcripts with automatic language detection
- **Outline Generation**: Uses Ollama's `llama3` model via LangChain to generate structured blog post outlines, with support for incorporating user feedback
- **Blog Generation**: Uses Ollama's `llama3` model via LangChain to generate structured blog posts based on approved outlines

## Setup

### Prerequisites

- Python 3.12 or higher
- Ollama installed and running locally

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

3. Install and run Ollama (if not already installed):

```bash
# Install Ollama from https://ollama.ai/
# Then pull the llama3 model:
ollama pull llama3
```

4. (Optional) Create a `.env` file in the root directory for any additional environment variables (no API key needed for Ollama):

## Usage

### Streamlit Web Interface

Launch the web interface:

```bash
streamlit run frontend/streamlit_app.py
```

The web interface provides:

- Input field for YouTube URL
- Language selector dropdown
- Generate button to start the blog generation process
- Outline preview with approve/reject options
- Feedback input for outline modifications
- Markdown preview of the generated blog post
- Download button to save the blog post as a `.md` file
- Start over button to reset and begin a new generation

#### Workflow

1. Enter a YouTube URL and select your preferred output language
2. Click "Generate Blog" to extract the transcript and generate an initial outline
3. Review the generated outline and either:
   - **Approve**: Click "Approve" to generate the final blog post from the outline
   - **Reject**: Click "Reject" to provide feedback and modify the outline
4. If rejecting, enter your feedback (e.g., "Add more details about X", "Focus on Y topic") and click "Modify Outline" to regenerate
5. Once approved, the final blog post is generated and displayed
6. Download the blog post as a markdown file or start over to create a new blog post

## Dependencies

- **langchain**: LLM framework and abstractions
- **langgraph**: Workflow orchestration for agentic applications
- **langchain-ollama**: Ollama integration for LangChain
- **youtube-transcript-api**: YouTube transcript extraction
- **streamlit**: Web interface framework
- **python-dotenv**: Environment variable management
