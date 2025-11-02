from .graph import build_graph


def main():
    url = input("Enter YouTube video URL: ").strip()
    language = input("Enter Output Language: ").strip() or "English"

    app = build_graph()
    initial_state = {
        "youtube_url": url,
        "transcript": "",
        "transcript_language": "",
        "blog_language": language,
        "blog_post": "",
    }

    print("\nGenerating...:\n")
    result = app.invoke(initial_state)
    print("\nGenerated Blog Post:\n")
    print(result["blog_post"])


if __name__ == "__main__":
    main()
