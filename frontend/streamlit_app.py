import streamlit as st
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.graph import build_graph

load_dotenv()

# import backend graph
app = build_graph()


def main():
    st.set_page_config(page_title="Blogify", layout="centered")

    st.title("Blogify")
    st.caption("Turn any YouTube video into a clean, readable blog post.")

    # Initialize session state
    if "state" not in st.session_state:
        st.session_state.state = None
    if "waiting_for_feedback" not in st.session_state:
        st.session_state.waiting_for_feedback = False
    if "outline_generated" not in st.session_state:
        st.session_state.outline_generated = False
    if "rejected" not in st.session_state:
        st.session_state.rejected = False
    if "blog_post" not in st.session_state:
        st.session_state.blog_post = None

    url = st.text_input("YouTube URL", placeholder="Paste YouTube URL here")
    language = st.selectbox(
        "Select blog language",
        [
            "English",
            "Hindi",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Japanese",
            "Korean",
        ],
        index=0,
    )

    # Handle initial blog generation
    if st.button("Generate Blog") and not st.session_state.waiting_for_feedback:
        with st.spinner("Extracting transcript and generating outline..."):
            initial_state = {
                "youtube_url": url,
                "transcript": "",
                "transcript_language": "",
                "blog_language": language,
                "outline": "",
                "feedback": "",
                "approved": False,
                "blog_post": "",
            }
            # Run graph up to outline generation by streaming
            config = {"recursion_limit": 50}
            events = app.stream(initial_state, config=config, stream_mode="updates")

            current_state = initial_state
            should_stop = False
            for event in events:
                if should_stop:
                    break
                for node_name, node_output in event.items():
                    current_state = node_output
                    # Stop after outline is generated and before check_approval
                    if node_name == "generate_outline" and current_state.get("outline"):
                        # We need to stop here before it goes to check_approval
                        # Save state for feedback
                        st.session_state.state = current_state.copy()
                        st.session_state.waiting_for_feedback = True
                        st.session_state.outline_generated = True
                        should_stop = True
                        st.rerun()
                        break

    # Show outline and feedback options
    if st.session_state.waiting_for_feedback and st.session_state.state:
        state = st.session_state.state
        outline = state.get("outline", "")

        if outline:
            st.markdown("---")
            st.subheader("Generated Outline")
            st.markdown(outline)
            st.markdown("---")

            # Two buttons side by side: Approve and Reject
            col1, col2 = st.columns(2)

            with col1:
                approve_clicked = st.button(
                    "Approve", type="primary", use_container_width=True
                )

            with col2:
                reject_clicked = st.button(
                    "Reject", type="secondary", use_container_width=True
                )

            # Handle Approve button
            if approve_clicked:
                # Set approval and generate blog post
                state["approved"] = True
                state["feedback"] = ""

                with st.spinner("Generating blog post..."):
                    from app.services import generate_blog_post as gen_blog_post

                    blog_md = gen_blog_post(
                        state.get("transcript", ""),
                        state.get("blog_language", "English"),
                        state.get("outline", ""),
                    )

                    st.session_state.blog_post = blog_md
                    st.session_state.rejected = False
                    st.rerun()

            # Handle Reject button
            if reject_clicked:
                st.session_state.rejected = True
                st.rerun()

            # Show feedback input if rejected
            if st.session_state.rejected:
                st.markdown("---")
                feedback = st.text_area(
                    "Provide feedback for modifications:",
                    placeholder="E.g., Add more details about X, focus on Y topic, include Z section...",
                    height=100,
                    key="feedback_input",
                )

                if st.button(
                    "Modify Outline",
                    type="primary",
                    use_container_width=True,
                    disabled=not (feedback and len(feedback.strip()) >= 4),
                ):
                    # Set feedback and regenerate outline
                    state["approved"] = False
                    state["feedback"] = feedback

                    with st.spinner("Regenerating outline based on your feedback..."):
                        from app.services import generate_outline as gen_outline

                        updated_outline = gen_outline(
                            state.get("transcript", ""),
                            state.get("blog_language", "English"),
                            feedback,
                        )
                        state["outline"] = updated_outline
                        state["feedback"] = ""
                        state["approved"] = False

                        st.session_state.state = state.copy()
                        st.session_state.rejected = False
                        st.session_state.blog_post = (
                            None  # Clear blog post when outline is regenerated
                        )
                        st.rerun()

            # Show blog post if it exists (full width, right under feedback section)
            if st.session_state.blog_post:
                st.markdown("---")
                st.subheader("Generated Blog Post")
                st.markdown(st.session_state.blog_post)
                st.download_button(
                    "Download .md",
                    st.session_state.blog_post,
                    "blogify_post.md",
                    "text/markdown",
                )

                # Reset state after showing blog post
                if st.button("Start Over", type="secondary"):
                    st.session_state.waiting_for_feedback = False
                    st.session_state.outline_generated = False
                    st.session_state.state = None
                    st.session_state.rejected = False
                    st.session_state.blog_post = None
                    st.rerun()


if __name__ == "__main__":
    main()
