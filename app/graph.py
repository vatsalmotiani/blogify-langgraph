from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal
from .services import get_transcript_from_youtube, generate_blog_post, generate_outline


# State definition
class AgentState(TypedDict):
    youtube_url: str
    transcript: str
    transcript_language: str
    blog_language: str
    outline: str
    feedback: str
    approved: bool
    blog_post: str


# Nodes
def extract_transcript_node(state: AgentState) -> AgentState:
    """Extracting transcript from YouTube URL by calling service function"""
    # Skip if transcript already exists
    if state.get("transcript"):
        return state

    transcript, transcript_language = get_transcript_from_youtube(state["youtube_url"])
    state["transcript"] = transcript
    state["transcript_language"] = transcript_language
    return state


def generate_outline_node(state: AgentState) -> AgentState:
    """Generating outline by calling service function"""
    blog_language = state.get("blog_language", "English")
    transcript = state.get("transcript", "")
    feedback = state.get("feedback", "") or None

    outline = generate_outline(transcript, blog_language, feedback)
    state["outline"] = outline
    # Reset feedback after using it
    state["feedback"] = ""
    return state


def generate_blog_post_node(state: AgentState) -> AgentState:
    """Generating blog post by calling service function"""
    blog_language = state.get("blog_language", "English")
    transcript = state.get("transcript", "")
    outline = state.get("outline", "")
    blog_post = generate_blog_post(transcript, blog_language, outline)
    state["blog_post"] = blog_post
    return state


def check_approval_node(state: AgentState) -> AgentState:
    """Check approval status - passes through state"""
    # Just passes through state, the conditional edge handles routing
    return state


def should_approve(
    state: AgentState,
) -> Literal["generate_blog_post", "generate_outline"]:
    """Check if outline is approved for conditional routing"""
    if state.get("approved", False):
        return "generate_blog_post"
    else:
        return "generate_outline"


# Graph
def build_graph():
    """Building the graph"""
    graph = StateGraph(AgentState)

    graph.add_node("extract_transcript", extract_transcript_node)
    graph.add_node("generate_outline", generate_outline_node)
    graph.add_node("check_approval", check_approval_node)
    graph.add_node("generate_blog_post", generate_blog_post_node)

    graph.add_edge(START, "extract_transcript")
    graph.add_edge("extract_transcript", "generate_outline")
    graph.add_edge("generate_outline", "check_approval")
    graph.add_conditional_edges(
        "check_approval",
        should_approve,
        {
            "generate_blog_post": "generate_blog_post",
            "generate_outline": "generate_outline",
        },
    )
    graph.add_edge("generate_blog_post", END)

    return graph.compile()
