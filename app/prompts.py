def generate_blog_post_prompt(transcript: str, blog_language: str) -> str:
    return f"""Based on the following video transcript, create a well-structured, engaging blog post.

IMPORTANT: Generate the entire blog post in {blog_language}. All content including headings, text, and conclusion must be in {blog_language}.

Requirements:
- Write the ENTIRE blog post in {blog_language}
- Use markdown formatting with clear headings (##) and subheadings (###)
- Create an engaging introduction that hooks the reader
- Organize content into logical sections with headings
- Include all key points and insights from the transcript
- Maintain a conversational and engaging tone
- Add a conclusion that summarizes the main takeaways
 - Aim for 500-800 words
 - Ensure proper grammar and natural flow in {blog_language}

Transcript:
{transcript}

Please create the blog post in {blog_language} now:"""
