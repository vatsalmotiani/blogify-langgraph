from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from .services import get_transcript_from_youtube, generate_blog_post


# State definition
class AgentState(TypedDict):
    youtube_url: str
    transcript: str
    transcript_language: str
    blog_language: str
    blog_post: str


# Nodes
def extract_transcript_node(state: AgentState) -> AgentState:
    """Extracting transcript from YouTube URL by calling service function"""
    transcript, transcript_language = get_transcript_from_youtube(state["youtube_url"])
    state["transcript"] = transcript
    state["transcript_language"] = transcript_language
    return state


def generate_blog_post_node(state: AgentState) -> AgentState:
    """Generating blog post by calling service function"""
    blog_language = state.get("blog_language", "English")
    transcript = state.get("transcript", "")
    blog_post = generate_blog_post(transcript, blog_language)
    state["blog_post"] = blog_post
    return state


# Graph
def build_graph():
    """Building the graph"""
    graph = StateGraph(AgentState)

    graph.add_node("extract_transcript", extract_transcript_node)
    graph.add_node("generate_blog_post", generate_blog_post_node)

    graph.add_edge(START, "extract_transcript")
    graph.add_edge("extract_transcript", "generate_blog_post")
    graph.add_edge("generate_blog_post", END)

    return graph.compile()
