def generate_outline_prompt(
    transcript: str, blog_language: str, feedback: str | None = None
) -> str:
    """Generate prompt for creating a blog post outline"""
    base_prompt = f"""Based on the following video transcript, create a detailed outline for a blog post.

IMPORTANT: Generate the outline in {blog_language}.

Requirements:
- Create a structured outline with main headings (##) and subheadings (###)
- Include an introduction section
- Break down the content into logical sections based on the transcript
- List key points and topics that will be covered in each section
- Include a conclusion section
- Use markdown formatting
- Keep it detailed but concise (aim for 5-8 main points)

Transcript:
{transcript}"""

    if feedback:
        base_prompt += f"""

User Feedback/Modifications:
{feedback}

Please update the outline based on the above feedback while ensuring all content can be supported by the transcript."""

    base_prompt += f"\n\nPlease create the blog outline in {blog_language} now:"
    return base_prompt


def generate_blog_post_prompt(transcript: str, blog_language: str, outline: str) -> str:
    return f"""Based on the following video transcript and approved outline, create a well-structured, engaging blog post.

IMPORTANT: Generate the entire blog post in {blog_language}. All content including headings, text, and conclusion must be in {blog_language}.

Requirements:
- Write the ENTIRE blog post in {blog_language}
- Follow the approved outline structure
- Use markdown formatting with clear headings (##) and subheadings (###)
- Create an engaging introduction that hooks the reader
- Organize content into logical sections with headings as per the outline
- Include all key points and insights from the transcript
- Maintain a conversational and engaging tone
- Add a conclusion that summarizes the main takeaways
- Aim for 500-800 words
- Ensure proper grammar and natural flow in {blog_language}

Approved Outline:
{outline}

Transcript:
{transcript}

Please create the blog post in {blog_language} now:"""
