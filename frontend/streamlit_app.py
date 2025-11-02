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

    url = st.text_input("YouTube URL")
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

    if st.button("Generate Blog"):
        with st.spinner("Processing..."):
            initial_state = {
                "youtube_url": url,
                "transcript": "",
                "transcript_language": "",
                "blog_language": language,
                "blog_post": "",
            }
            result = app.invoke(initial_state)
            blog_md = result["blog_post"]

            st.markdown("---")
            st.markdown(blog_md)
            st.download_button("Download .md", blog_md, "blogify_post.md")


if __name__ == "__main__":
    main()
